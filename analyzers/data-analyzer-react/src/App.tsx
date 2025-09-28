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
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import remarkGfm from 'remark-gfm';
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

interface ApiConfig {
  key: string;
  endpoint: string;
}

interface AiInsights {
  content: string;
  isGenerating: boolean;
  error: string;
}

const App: React.FC = () => {
  const [csvData, setCsvData] = useState<DataRow[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [isDragOver, setIsDragOver] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // AI Insights state
  const [apiConfig, setApiConfig] = useState<ApiConfig>({
    key: '',
    endpoint: 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
  });
  const [aiInsights, setAiInsights] = useState<AiInsights>({
    content: '',
    isGenerating: false,
    error: ''
  });

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

  // Custom components for markdown rendering
  const CodeBlock = ({ node, inline, className, children, ...props }: any) => {
    const match = /language-(\w+)/.exec(className || '');
    const language = match ? match[1] : '';

    return !inline && language ? (
      <div style={{ maxWidth: '100%', overflow: 'hidden' }}>
        <SyntaxHighlighter
          style={oneDark}
          language={language}
          PreTag="div"
          showLineNumbers={true}
          wrapLines={false}
          customStyle={{
            margin: 0,
            borderRadius: '8px',
            maxWidth: '100%',
            overflowX: 'auto',
            fontSize: '0.9em'
          }}
          {...props}
        >
          {String(children).replace(/\n$/, '')}
        </SyntaxHighlighter>
      </div>
    ) : (
      <code className={className} style={{ wordBreak: 'break-all', overflowWrap: 'break-word' }} {...props}>
        {children}
      </code>
    );
  };

  const generateAiInsights = async () => {
    if (csvData.length === 0) return;
    if (!apiConfig.key) {
      setAiInsights(prev => ({ ...prev, error: 'Please configure your Qwen API key first!' }));
      return;
    }

    setAiInsights(prev => ({ ...prev, isGenerating: true, error: '' }));

    try {
      const stats = calculateStats();
      const columns = Object.keys(csvData[0]);
      const sampleData = csvData.slice(0, 10);

      // Prepare data summary for AI analysis
      const dataSummary = {
        totalRows: stats?.totalRows || 0,
        totalColumns: stats?.totalColumns || 0,
        numericColumns: stats?.numericColumns || 0,
        columns: columns,
        sampleData: sampleData
      };

      const prompt = `You are a data analyst AI. Analyze this CSV dataset and provide insights. Here's the data summary:

Dataset Overview:
- Total Rows: ${dataSummary.totalRows}
- Total Columns: ${dataSummary.totalColumns}
- Numeric Columns: ${dataSummary.numericColumns}
- Column Names: ${dataSummary.columns.join(', ')}

Sample Data (first 10 rows):
${JSON.stringify(dataSummary.sampleData, null, 2)}

Please provide a comprehensive analysis including:
1. **Data Quality Assessment** - Check for missing values, data types, consistency
2. **Statistical Summary** - Key metrics, distributions, outliers
3. **Patterns & Trends** - Any visible patterns, correlations, or trends
4. **Insights & Recommendations** - Business insights, potential issues, suggestions for improvement
5. **Data Visualization Ideas** - What charts/graphs would be most effective

Format your response with proper markdown, including headers, lists, and code blocks where appropriate. Be specific and actionable.`;

      const response = await callQwenAPI(prompt);
      setAiInsights(prev => ({ ...prev, content: response, isGenerating: false }));
    } catch (error) {
      console.error('AI Insights Error:', error);
      setAiInsights(prev => ({
        ...prev,
        error: 'Failed to generate AI insights. Please check your API key and try again.',
        isGenerating: false
      }));
    }
  };

  const callQwenAPI = async (message: string): Promise<string> => {
    // Try the DashScope native API first
    try {
      const response = await fetch('https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiConfig.key}`,
          'X-DashScope-SSE': 'disable'
        },
        body: JSON.stringify({
          model: 'qwen-turbo',
          input: {
            messages: [
              {
                role: 'system',
                content: 'You are a data analyst AI. Provide clear, accurate, and actionable insights about datasets. Use markdown formatting for better readability.'
              },
              {
                role: 'user',
                content: message
              }
            ]
          },
          parameters: {
            max_tokens: 1500,
            temperature: 0.7
          }
        })
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('DashScope API Error:', errorText);
        throw new Error(`API request failed: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log('DashScope API Response:', data);

      // DashScope native format
      if (data.output && data.output.text) {
        return data.output.text;
      } else {
        throw new Error('Invalid DashScope response format');
      }
    } catch (dashScopeError) {
      console.warn('DashScope API failed, trying OpenAI-compatible endpoint:', dashScopeError);

      // Fallback to OpenAI-compatible endpoint
      try {
        const response = await fetch('https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiConfig.key}`,
            'X-DashScope-SSE': 'disable'
          },
          body: JSON.stringify({
            model: 'qwen-turbo',
            messages: [
              {
                role: 'system',
                content: 'You are a data analyst AI. Provide clear, accurate, and actionable insights about datasets. Use markdown formatting for better readability.'
              },
              {
                role: 'user',
                content: message
              }
            ],
            max_tokens: 1500,
            temperature: 0.7,
            stream: false
          })
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`OpenAI-compatible API failed: ${response.status} - ${errorText}`);
        }

        const data = await response.json();
        console.log('OpenAI-compatible API Response:', data);

        // OpenAI-compatible format
        if (data.choices && data.choices[0] && data.choices[0].message) {
          return data.choices[0].message.content;
        } else {
          throw new Error('Invalid OpenAI-compatible response format');
        }
      } catch (openAIError) {
        console.error('Both API endpoints failed:', openAIError);
        throw new Error('Failed to connect to Qwen API. Please check your API key and internet connection.');
      }
    }
  };

  const renderAiInsights = () => {
    if (csvData.length === 0) return null;

    return (
      <div className="ai-insights-section">
        <h3>🤖 AI Insights</h3>

        {!apiConfig.key && (
          <div className="api-config-section">
            <h4>Configure Qwen API</h4>
            <div className="api-input-group">
              <label htmlFor="api-key">Qwen API Key:</label>
              <input
                type="password"
                id="api-key"
                placeholder="Enter your Qwen API key here..."
                value={apiConfig.key}
                onChange={(e) => setApiConfig(prev => ({ ...prev, key: e.target.value }))}
              />
            </div>
            <p className="api-help">
              Get your free API key from <a href="https://dashscope.aliyuncs.com/" target="_blank" rel="noopener noreferrer">DashScope Console</a>
            </p>
          </div>
        )}

        <div className="insights-actions">
          <button
            className="generate-insights-btn"
            onClick={generateAiInsights}
            disabled={aiInsights.isGenerating || !apiConfig.key}
          >
            {aiInsights.isGenerating ? '🔄 Generating Insights...' : '🧠 Generate AI Insights'}
          </button>
        </div>

        {aiInsights.error && (
          <div className="error-message">
            ❌ {aiInsights.error}
          </div>
        )}

        {aiInsights.isGenerating && (
          <div className="loading">
            🧠 Analyzing your data with AI...
          </div>
        )}

        {aiInsights.content && (
          <div className="insights-content">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                code: CodeBlock,
              }}
            >
              {aiInsights.content}
            </ReactMarkdown>
          </div>
        )}
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

            {renderAiInsights()}
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
