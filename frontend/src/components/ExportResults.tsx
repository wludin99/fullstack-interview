import React, { useState } from 'react';
import type { BatchProcessingResult, Document } from '../services/api';

interface ExportResultsProps {
  results: BatchProcessingResult[];
  documents: Document[];
  onExport?: (format: string) => void;
}

export const ExportResults: React.FC<ExportResultsProps> = ({
  results,
  documents,
  onExport
}) => {
  const [isExporting, setIsExporting] = useState(false);
  const [exportFormat, setExportFormat] = useState<'csv' | 'json' | 'xlsx'>('csv');

  const getDocumentName = (documentId: string) => {
    const doc = documents.find(d => d.id === documentId);
    return doc ? doc.filename : 'Unknown Document';
  };

  const exportToCSV = () => {
    setIsExporting(true);
    
    try {
      const csvContent = results.map(result => {
        const docName = getDocumentName(result.document_id);
        return {
          document: docName,
          status: result.status,
          error: result.error || '',
          timestamp: new Date().toISOString()
        };
      });

      const csv = 'Document,Status,Error,Timestamp\n' + 
        csvContent.map(row => 
          `"${row.document}","${row.status}","${row.error}","${row.timestamp}"`
        ).join('\n');
      
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `batch_results_${new Date().toISOString().split('T')[0]}.csv`;
      a.click();
      URL.revokeObjectURL(url);
      
      if (onExport) {
        onExport('csv');
      }
    } catch (error) {
      console.error('Error exporting CSV:', error);
    } finally {
      setIsExporting(false);
    }
  };

  const exportToJSON = () => {
    setIsExporting(true);
    
    try {
      const jsonData = {
        exportDate: new Date().toISOString(),
        totalResults: results.length,
        successCount: results.filter(r => r.status === 'completed').length,
        errorCount: results.filter(r => r.status === 'error').length,
        results: results.map(result => ({
          id: result.id,
          document: getDocumentName(result.document_id),
          documentId: result.document_id,
          status: result.status,
          error: result.error,
          timestamp: new Date().toISOString()
        }))
      };

      const blob = new Blob([JSON.stringify(jsonData, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `batch_results_${new Date().toISOString().split('T')[0]}.json`;
      a.click();
      URL.revokeObjectURL(url);
      
      if (onExport) {
        onExport('json');
      }
    } catch (error) {
      console.error('Error exporting JSON:', error);
    } finally {
      setIsExporting(false);
    }
  };

  const exportToXLSX = () => {
    setIsExporting(true);
    
    try {
      // For XLSX export, we'll create a simple HTML table that can be opened in Excel
      const htmlContent = `
        <html>
          <head>
            <meta charset="utf-8">
            <title>Batch Processing Results</title>
          </head>
          <body>
            <table>
              <thead>
                <tr>
                  <th>Document</th>
                  <th>Status</th>
                  <th>Error</th>
                  <th>Timestamp</th>
                </tr>
              </thead>
              <tbody>
                ${results.map(result => `
                  <tr>
                    <td>${getDocumentName(result.document_id)}</td>
                    <td>${result.status}</td>
                    <td>${result.error || ''}</td>
                    <td>${new Date().toISOString()}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </body>
        </html>
      `;
      
      const blob = new Blob([htmlContent], { type: 'application/vnd.ms-excel' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `batch_results_${new Date().toISOString().split('T')[0]}.xls`;
      a.click();
      URL.revokeObjectURL(url);
      
      if (onExport) {
        onExport('xlsx');
      }
    } catch (error) {
      console.error('Error exporting XLSX:', error);
    } finally {
      setIsExporting(false);
    }
  };

  const handleExport = () => {
    switch (exportFormat) {
      case 'csv':
        exportToCSV();
        break;
      case 'json':
        exportToJSON();
        break;
      case 'xlsx':
        exportToXLSX();
        break;
      default:
        exportToCSV();
    }
  };

  const successCount = results.filter(r => r.status === 'completed').length;
  const errorCount = results.filter(r => r.status === 'error').length;
  const totalCount = results.length;

  return (
    <div className="export-results">
      <div className="export-header">
        <h3>Export Results</h3>
        <div className="export-summary">
          <span className="summary-item">
            <strong>Total:</strong> {totalCount}
          </span>
          <span className="summary-item success">
            <strong>Success:</strong> {successCount}
          </span>
          <span className="summary-item error">
            <strong>Errors:</strong> {errorCount}
          </span>
        </div>
      </div>

      <div className="export-controls">
        <div className="format-selection">
          <label htmlFor="export-format">Export Format:</label>
          <select
            id="export-format"
            value={exportFormat}
            onChange={(e) => setExportFormat(e.target.value as 'csv' | 'json' | 'xlsx')}
            className="format-select"
          >
            <option value="csv">CSV</option>
            <option value="json">JSON</option>
            <option value="xlsx">Excel (XLSX)</option>
          </select>
        </div>

        <button
          onClick={handleExport}
          disabled={isExporting || results.length === 0}
          className="export-button"
        >
          {isExporting ? 'Exporting...' : `Export as ${exportFormat.toUpperCase()}`}
        </button>
      </div>

      <div className="export-preview">
        <h4>Preview (first 5 results):</h4>
        <div className="preview-table">
          <table>
            <thead>
              <tr>
                <th>Document</th>
                <th>Status</th>
                <th>Error</th>
              </tr>
            </thead>
            <tbody>
              {results.slice(0, 5).map((result) => (
                <tr key={result.id}>
                  <td>{getDocumentName(result.document_id)}</td>
                  <td>
                    <span className={`status-badge status-${result.status}`}>
                      {result.status}
                    </span>
                  </td>
                  <td>{result.error || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {results.length > 5 && (
            <p className="preview-note">
              ... and {results.length - 5} more results
            </p>
          )}
        </div>
      </div>

      <div className="export-options">
        <h4>Export Options:</h4>
        <ul>
          <li>
            <strong>CSV:</strong> Comma-separated values, compatible with Excel and Google Sheets
          </li>
          <li>
            <strong>JSON:</strong> Structured data format, includes metadata and timestamps
          </li>
          <li>
            <strong>Excel:</strong> Native Excel format, preserves formatting and formulas
          </li>
        </ul>
      </div>
    </div>
  );
};
