import React, { useState } from 'react';

export default function Dashboard({ onUpload, isLoading, error }) {
  const [file, setFile] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) onUpload(file);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <form onSubmit={handleSubmit} className="flex items-end gap-4">
        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Upload CSV/Excel (Must contain: Series Name, Date, Amount)
          </label>
          <input 
            type="file" 
            accept=".csv, .xlsx"
            onChange={(e) => setFile(e.target.files[0])}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
        </div>
        <button 
          type="submit" 
          disabled={!file || isLoading}
          className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {isLoading ? 'Reconciling...' : 'Run Reconciliation'}
        </button>
      </form>
      {error && <p className="text-red-600 text-sm mt-4">{error}</p>}
    </div>
  );
}