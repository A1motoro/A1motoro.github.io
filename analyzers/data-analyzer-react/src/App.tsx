import React, { useState, useRef } from 'react';
import Papa from 'papaparse';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import './App.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface DataRow {
  [key: string]: string | number;
}

interface FileData {
  data: DataRow[];
  errors: any[];
  meta: {
    delimiter: string;
    linebreak: string;
    aborted: boolean;
    truncated: boolean;
    cursor: number;
  };
}

const App: React.FC = () => {
  const [csvData, setCsvData] = useState<DataRow[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [isDragOver, setIsDragOver] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = (file: File) => {
    if (!file || file.type !== 'text/csv') {
      setError('Please select a valid CSV file.');
      return;
    }

    setIsLoading(true);
    setError('');

    Papa.parse(file, {
      header: true,
      complete: (results: FileData) => {
        setCsvData(results.data);
        setIsLoading(false);
      },
      error: (error) => {
        console.error('Error parsing CSV:', error);
        setError('Error parsing CSV file. Please check the file format.');
        setIsLoading(false);
      }
    });
  };

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragOver(false);

    const files = event.dataTransfer.files;
    if (files.length > 0 && files[0].type === 'text/csv') {
      handleFileUpload(files[0]);
    } else {
      setError('Please drop a valid CSV file.');
    }
  };

  const calculateStats = () => {
    if (csvData.length === 0) return null;

    const columns = Object.keys(csvData[0]);
    const totalRows = csvData.length;
    const numericColumns = columns.filter(col => {
      return csvData.some(row => !isNaN(parseFloat(String(row[col]))) && isFinite(Number(row[col])));
    });

    return {
      totalRows,
      totalColumns: columns.length,
      numericColumns: numericColumns.length,
      numericPercentage: Math.round((numericColumns.length / columns.length) * 100)
    };
  };

  const renderChart = () => {
    if (csvData.length === 0) return null;

    const columns = Object.keys(csvData[0]);
    const numericColumns = columns.filter(col => {
      return csvData.some(row => !isNaN(parseFloat(String(row[col]))) && isFinite(Number(row[col])));
    });

    const sampleData = csvData.slice(0, 10).map((row, index) => ({
      x: index,
      y: numericColumns.length > 0 ? parseFloat(String(row[numericColumns[0]])) || 0 : Math.random() * 100
    }));

    const data = {
      datasets: [{
        label: 'Data Trend',
        data: sampleData,
        borderColor: '#a6e22e',
        backgroundColor: 'rgba(166, 226, 46, 0.1)',
        tension: 0.4
      }]
    };

    const options = {
      responsive: true,
      plugins: {
        legend: {
          labels: {
            color: '#f8f8f2'
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: '#f8f8f2'
          },
          grid: {
            color: '#49483e'
          }
        },
        y: {
          ticks: {
            color: '#f8f8f2'
          },
          grid: {
            color: '#49483e'
          }
        }
      }
    };

    return <Line data={data} options={options} />;
  };

  const renderDataTable = () => {
    if (csvData.length === 0) return null;

    const columns = Object.keys(csvData[0]);
    const sampleData = csvData.slice(0, 5);

    return (
      <div className="data-table">
        <h4>Sample Data (First 5 Rows)</h4>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                {columns.map(col => (
                  <th key={col}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {sampleData.map((row, index) => (
                <tr key={index}>
                  {columns.map(col => (
                    <td key={col}>{row[col] || '-'}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  const stats = calculateStats();

  return (
    <div className="app">
      <header className="app-header">
        <h1>📊 CSV Data Analyzer</h1>
        <p>Upload your CSV files and get instant insights with beautiful visualizations</p>
      </header>

      <main className="app-main">
        <div
          className={`upload-area ${isDragOver ? 'dragover' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <div className="upload-icon">📁</div>
          <h3>Upload Your CSV File</h3>
          <p>Drag and drop your CSV file here or click to browse</p>
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />
          <button className="upload-button" onClick={(e) => {
            e.stopPropagation();
            fileInputRef.current?.click();
          }}>
            Choose File
          </button>
        </div>

        {error && (
          <div className="error-message">
            ❌ {error}
          </div>
        )}

        {isLoading && (
          <div className="loading">
            📊 Analyzing your data...
          </div>
        )}

        {csvData.length > 0 && stats && (
          <div className="analysis-results">
            <h3>Analysis Results</h3>

            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-value">{stats.totalRows}</div>
                <div className="stat-label">Total Rows</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{stats.totalColumns}</div>
                <div className="stat-label">Columns</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{stats.numericColumns}</div>
                <div className="stat-label">Numeric Columns</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{stats.numericPercentage}%</div>
                <div className="stat-label">Numeric Data</div>
              </div>
            </div>

            <div className="chart-container">
              {renderChart()}
            </div>

            {renderDataTable()}
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
