import pandas as pd
import openpyxl
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pdfplumber
import io
import re
import asyncio
from datetime import datetime
from pathlib import Path
import json
from rapidfuzz import fuzz


AUDIT_LOG_DIR = Path(__file__).resolve().parent / "audit_logs"


# ── FILE READER: handles CSV (with junk header rows) and Excel ────────────────
def read_input_file(file_path):
    if file_path.endswith(('.xlsx', '.xls')):
        return pd.read_excel(file_path)

    # CSV: try reading normally first, then skip rows if a junk header exists
    for skiprows in [0, 1, 2]:
        try:
            df = pd.read_csv(file_path, sep=None, engine='python', skiprows=skiprows)
            # Valid if first column looks like a header, not "Table 1" etc.
            cols = [str(c).lower().strip() for c in df.columns]
            if any(k in cols for k in ['series', 'series name', 'name', 'date', 'amount']):
                return df
        except Exception:
            continue
    raise ValueError("Could not read the file. Please ensure it is a valid CSV or Excel format.")


# ── DATE PARSER: handles "12th May 2026", "12th May, 2026", "12th April 2026" ─
def parse_date(date_str):
    if not date_str:
        return None
    # Remove ordinal suffixes and commas
    clean = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', str(date_str).strip())
    clean = clean.replace(',', '')               # "May, 2026" → "May 2026"
    clean = re.sub(r'\s+', ' ', clean).strip()
    for fmt in ('%d %B %Y', '%d %b %Y'):
        try:
            return datetime.strptime(clean, fmt)
        except ValueError:
            continue
    return None


# ── SERIES LETTER EXTRACTOR: handles "eqar f", "EQAR Series F", "car e" ──────
def get_series_letter(csv_series):
    """Extract the single identifying letter from any series name format."""
    s = str(csv_series).strip().upper()
    # Match last standalone letter or letter at end
    match = re.search(r'\b([A-Z])\s*$', s)
    if match:
        return match.group(1)
    # Fallback: last character
    return s[-1] if s else None


def is_car_series(csv_series):
    return bool(re.search(r'\bcar\b', str(csv_series).lower()))


# ── PDF PARSER: reads ALL pages and returns (datetime, amount) history ────────
def _extract_valuations_from_text(full_text):
    """Extract valuation dates and amounts from text collected from a report."""
    results = []
    chunks = re.split(r'Valuation\s+as\s+(?:of|on)\s+', full_text, flags=re.IGNORECASE)

    for chunk in chunks[1:]:
        date_match = re.match(r'([\d\w\s,]{5,30}?202\s*\d)', chunk)
        if not date_match:
            continue
        raw_date = re.sub(r'\s+', ' ', date_match.group(1)).strip().replace("202 ", "202")
        dt = parse_date(raw_date)
        if dt is None:
            continue

        ine_idx = chunk.find('INE')
        if ine_idx == -1:
            continue

        scan = chunk[ine_idx:ine_idx+800]
        decimals = re.findall(r'(?<![\d,])\d{1,5}\.\d{1,4}(?!\d)', scan)
        valid = [float(d) for d in decimals if 0 < float(d) < 10000]
        if valid:
            results.append((dt, valid[0]))

    return results


def extract_all_valuations(pdf_bytes):
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        return _extract_valuations_from_text(full_text)

    except Exception as e:
        print(f"   PDF Parse Error: {e}")
        return []


# ── SCRAPE ALL PDF LINKS FROM SITE ────────────────────────────────────────────
async def scrape_all_links(page):
    print("🌐 Scraping all PDF links from Alt Alpha...")
    await page.goto("https://fin.alt-alpha.com/valuations/", wait_until="domcontentloaded")
    await page.wait_for_timeout(2000)
    soup  = BeautifulSoup(await page.content(), 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        text = a.get_text(strip=True)
        if 'Valuation Report' in text or href.lower().endswith('.pdf'):
            if not href.startswith('http'):
                href = "https://fin.alt-alpha.com" + href
            filename = href.split('/')[-1].replace('.pdf', '')
            links.append({"url": href, "filename": filename, "fn_upper": filename.upper()})
    print(f"   Found {len(links)} PDFs: {[l['filename'] for l in links]}")
    return links


# ── FIND PDF LINK FOR A SERIES ────────────────────────────────────────────────
def find_series_link(all_links, csv_series):
    is_car = is_car_series(csv_series)
    letter = get_series_letter(csv_series)
    if not letter:
        return None

    for link in all_links:
        fn = link['fn_upper']
        fn_is_car = "CAR" in fn
        if is_car != fn_is_car:
            continue
        if is_car:
            if re.match(rf'^CAR[-_]{letter}[_\-]', fn):
                return link
        else:
            if fn.endswith(f'_{letter}') or fn.endswith(f'-{letter}'):
                return link

    # Some source files use slightly different separators or labels.  Keep the
    # car/non-car boundary strict, then accept only a high-confidence match.
    expected = f"CAR {letter}" if is_car else f"SERIES {letter}"
    candidates = [
        link for link in all_links
        if ("CAR" in link['fn_upper']) == is_car
        and re.search(rf'\b{re.escape(letter)}\b', link['fn_upper'].replace('_', ' ').replace('-', ' '))
    ]
    if candidates:
        def score(link):
            normalized = link['fn_upper'].replace('_', ' ').replace('-', ' ')
            compact = re.sub(r'\b(SERIES|REPORT|VALUATION|PDF)\b', '', normalized)
            compact = re.sub(r'\s+', ' ', compact).strip()
            return max(
                fuzz.partial_ratio(expected, normalized),
                fuzz.ratio(expected, compact),
            )

        best = max(candidates, key=score)
        if score(best) >= 85:
            return best
    return None


def persist_audit_log(results):
    """Write an immutable, timestamped record for one reconciliation run."""
    AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().astimezone().strftime('%Y%m%dT%H%M%S%f%z')
    path = AUDIT_LOG_DIR / f"reconciliation_{timestamp}.json"
    rows = [
        {
            "series_name": row["series_name"],
            "matched_pdf_filename": row["matched_series"],
            "csv_date": row["csv_date"],
            "csv_amount": row["csv_amount"],
            "system_date": row["system_date"],
            "system_amount": row["system_amount"],
            "variance": row["variance"],
            "status": row["status"],
        }
        for row in results
    ]
    path.write_text(json.dumps({"run_timestamp": datetime.now().astimezone().isoformat(), "rows": rows}, indent=2), encoding="utf-8")
    print(f"🧾 Audit log saved: {path}")
    return path


# ── MAIN RECONCILIATION ENGINE ────────────────────────────────────────────────
async def process_reconciliation(file_path):
    print("\n🚀 Starting Reconciliation Engine (Full History Mode)...")

    try:
        df = read_input_file(file_path)
    except Exception as e:
        raise ValueError(str(e))

    df.columns = df.columns.astype(str).str.lower().str.strip()
    # Drop completely empty columns
    df = df.dropna(axis=1, how='all')

    df.rename(columns={
        'series name': 'Series Name', 'series': 'Series Name', 'name': 'Series Name',
        'date': 'Date', 'valuation date': 'Date',
        'amount': 'Amount', 'valuation': 'Amount', 'price': 'Amount'
    }, inplace=True)

    missing = [c for c in ['Series Name', 'Date', 'Amount'] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}. Found: {', '.join(df.columns)}")

    # Drop empty rows
    df = df.dropna(subset=['Series Name', 'Date', 'Amount'])
    df = df[df['Series Name'].astype(str).str.strip() != '']

    print(f"✅ Validation Passed! Processing {len(df)} rows...")
    results  = []
    pdf_cache = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page    = await context.new_page()

        all_links = await scrape_all_links(page)

        for _, row in df.iterrows():
            csv_series = str(row['Series Name']).strip()
            csv_amount = float(row['Amount'])
            csv_date   = str(row['Date']).strip()

            print(f"\n📅 {csv_series} | {csv_date} | ₹{csv_amount}")

            csv_dt = parse_date(csv_date)
            if csv_dt is None:
                print(f"   ✗ Could not parse date: '{csv_date}'")
                results.append({
                    "series_name": csv_series, "matched_series": "Date Parse Failed",
                    "csv_date": csv_date, "system_date": "N/A",
                    "csv_amount": csv_amount, "system_amount": 0.0,
                    "variance": csv_amount, "status": "Error", "pdf_link": "#"
                })
                continue

            link = find_series_link(all_links, csv_series)
            if link is None:
                print(f"   ✗ No PDF found for '{csv_series}' (letter: {get_series_letter(csv_series)})")
                results.append({
                    "series_name": csv_series, "matched_series": "Not Found Online",
                    "csv_date": csv_date, "system_date": "N/A",
                    "csv_amount": csv_amount, "system_amount": 0.0,
                    "variance": csv_amount, "status": "Missing", "pdf_link": "#"
                })
                continue

            if link['filename'] not in pdf_cache:
                print(f"   ⬇️  Downloading: {link['filename']}")
                try:
                    resp      = await context.request.get(link['url'])
                    pdf_bytes = await resp.body()
                    history   = await asyncio.to_thread(extract_all_valuations, pdf_bytes)
                    pdf_cache[link['filename']] = history
                    print(f"   📖 {len(history)} valuation entries found in PDF")
                except Exception as e:
                    print(f"   ✗ Download error: {e}")
                    results.append({
                        "series_name": csv_series, "matched_series": "Download Failed",
                        "csv_date": csv_date, "system_date": "N/A",
                        "csv_amount": csv_amount, "system_amount": 0.0,
                        "variance": csv_amount, "status": "Error", "pdf_link": link['url']
                    })
                    continue
            else:
                print(f"   ♻️  Using cached: {link['filename']}")

            history = pdf_cache[link['filename']]
            if not history:
                results.append({
                    "series_name": csv_series, "matched_series": link['filename'],
                    "csv_date": csv_date, "system_date": "N/A",
                    "csv_amount": csv_amount, "system_amount": 0.0,
                    "variance": csv_amount, "status": "Error", "pdf_link": link['url']
                })
                continue

            # Find exact date match in history
            exact = next(((dt, amt) for dt, amt in history if dt.date() == csv_dt.date()), None)

            if exact:
                pdf_dt, pdf_amount = exact
                date_matched = True
                print(f"   ✅ Exact match: {pdf_dt.strftime('%d %b %Y')} → ₹{pdf_amount}")
            else:
                pdf_dt, pdf_amount = max(history, key=lambda x: x[0])
                date_matched = False
                print(f"   ⚠️  No entry for {csv_date}. Using latest: {pdf_dt.strftime('%d %b %Y')} → ₹{pdf_amount}")

            variance = round(csv_amount - pdf_amount, 2)
            if not date_matched:
                status = "Date Mismatch (Latest Used)"
            elif variance == 0:
                status = "Matched"
            else:
                status = "Amount Mismatch"

            print(f"   → {status} | Variance: ₹{variance}")

            results.append({
                "series_name":    csv_series,
                "matched_series": link['filename'],
                "csv_date":       csv_date,
                "system_date":    pdf_dt.strftime('%d %b %Y'),
                "csv_amount":     csv_amount,
                "system_amount":  pdf_amount,
                "variance":       variance,
                "status":         status,
                "pdf_link":       link['url']
            })

        await browser.close()

    persist_audit_log(results)
    return results
