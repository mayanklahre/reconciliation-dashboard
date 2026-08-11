import React from 'react';

const ResultsTable = ({ data }) => {
  return (
    <div className="mt-8 bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="bg-gray-50 border-b border-gray-200 text-gray-700 font-semibold">
            <tr>
              <th className="px-6 py-4">CSV Series</th>
              <th className="px-6 py-4">Matched Online Series</th>
              <th className="px-6 py-4">Your Date</th>
              <th className="px-6 py-4 text-blue-600">Live Website Date</th>
              <th className="px-6 py-4 text-right">CSV Amount</th>
              <th className="px-6 py-4 text-right text-blue-600">Live Amount</th>
              <th className="px-6 py-4 text-right">Variance</th>
              <th className="px-6 py-4 text-center">Status</th>
              <th className="px-6 py-4 text-center">Source</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {data.map((row, index) => (
              <tr key={index} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 font-medium text-gray-900">{row.series_name}</td>
                <td className="px-6 py-4 text-gray-600">{row.matched_series}</td>
                <td className="px-6 py-4 text-gray-600">{row.csv_date}</td>
                
                {/* Highlight if the website has a newer date than the CSV */}
                <td className="px-6 py-4 font-medium text-gray-900 bg-blue-50/30">
                  {row.system_date}
                </td>
                
                <td className="px-6 py-4 text-right text-gray-600">₹{row.csv_amount.toFixed(2)}</td>
                <td className="px-6 py-4 text-right font-medium text-gray-900 bg-blue-50/30">
                  ₹{row.system_amount.toFixed(2)}
                </td>
                
                <td className={`px-6 py-4 text-right font-semibold ${
                  row.variance === 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  ₹{row.variance.toFixed(2)}
                </td>
                
                <td className="px-6 py-4 text-center">
                  <span className={`inline-flex px-3 py-1 rounded-full text-xs font-bold ${
                    row.status === 'Matched' ? 'bg-green-100 text-green-700' : 
                    row.status === 'Missing' ? 'bg-gray-100 text-gray-700' : 
                    'bg-red-100 text-red-700'
                  }`}>
                    {row.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-center">
                  {row.pdf_link !== "#" ? (
                    <a href={row.pdf_link} target="_blank" rel="noreferrer" className="text-blue-600 hover:text-blue-800 hover:underline">
                      View PDF
                    </a>
                  ) : (
                    <span className="text-gray-400">-</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ResultsTable;