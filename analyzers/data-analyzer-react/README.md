# CSV Data Analyzer with AI Insights - React TypeScript

A modern, powerful CSV data analysis tool built with React and TypeScript. This analyzer provides comprehensive data insights with beautiful visualizations, interactive features, and AI-powered analysis using Qwen AI.

## ✨ Features

- 📊 **CSV File Upload**: Drag and drop or click to upload CSV files
- 📈 **Interactive Charts**: Beautiful line charts using Chart.js
- 📋 **Data Statistics**: Comprehensive statistical analysis
- 📋 **Data Preview**: Sample data table view
- 🤖 **AI Insights**: Get intelligent analysis and recommendations using Qwen AI
- 📝 **Markdown Support**: AI responses with syntax-highlighted code blocks
- 🎨 **Modern UI**: Clean, responsive design with dark theme
- ⚡ **TypeScript**: Full type safety and better development experience
- 📱 **Responsive**: Works on desktop and mobile devices

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### 🚀 Quick Start

**Easiest Method:** Just **double-click** `start-analyzer.bat` in the data-analyzer-react folder!

This script will automatically:
- ✅ Install all dependencies
- ✅ Start the development server
- ✅ Open http://localhost:3000 in your browser

### Manual Installation

1. Navigate to the project directory:
```bash
cd analyzers/data-analyzer-react
```

2. Install dependencies:
```bash
npm install
# OR double-click: install-analyzer.bat
```

3. Start the development server:
```bash
npm start
# OR double-click: start-analyzer.bat
```

4. Open your browser to `http://localhost:3000`

### Building for Production

```bash
npm run build
```

This will create a `build` folder with the production-ready files.

## Usage

1. **Upload CSV File**: Click the upload area or drag and drop a CSV file
2. **View Statistics**: See comprehensive stats about your data
3. **Explore Visualizations**: Interactive charts show data trends
4. **Preview Data**: Sample table shows the first 5 rows of your data

### 🤖 AI Insights Feature

The analyzer includes powerful AI-powered insights using Qwen AI:

#### **Setting Up AI Analysis**
1. **Install Dependencies**: Run `install-analyzer.bat` or `npm install`
2. **Get API Key**: Visit [Alibaba Cloud DashScope](https://dashscope.aliyuncs.com/) and create a free API key
3. **Configure API**: Enter your API key in the AI Insights section
4. **Generate Analysis**: Click "Generate AI Insights" for comprehensive data analysis

#### **AI Analysis Includes**
- 📊 **Data Quality Assessment**: Missing values, data types, consistency checks
- 📈 **Statistical Analysis**: Key metrics, distributions, outliers detection
- 🔍 **Pattern Recognition**: Trends, correlations, and anomalies
- 💡 **Business Insights**: Actionable recommendations and interpretations
- 📊 **Visualization Suggestions**: Recommended charts and graphs for your data

#### **AI Response Features**
- **Markdown Formatting**: Structured analysis with headers and lists
- **Code Examples**: Syntax-highlighted code blocks (Monokai theme)
- **Data Tables**: Formatted tables for comparisons and summaries
- **Professional Analysis**: Expert-level data science insights

## Project Structure

```
data-analyzer-react/
├── public/
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── App.tsx          # Main application component
│   ├── App.css          # Main application styles
│   ├── index.tsx        # Application entry point
│   ├── index.css        # Global styles
│   └── types/           # TypeScript type definitions
├── package.json         # Dependencies and scripts
├── tsconfig.json        # TypeScript configuration
└── README.md           # This file
```

## Technologies Used

- **React 18**: Modern React with hooks
- **TypeScript**: Type-safe JavaScript
- **Chart.js**: Powerful charting library
- **PapaParse**: Fast CSV parsing
- **React Chart.js 2**: React wrapper for Chart.js
- **React Markdown**: Markdown rendering with GitHub Flavored Markdown support
- **React Syntax Highlighter**: Code syntax highlighting with Monokai theme
- **Qwen AI**: Alibaba Cloud's advanced AI for data analysis

## Features in Detail

### Data Analysis
- Total row and column count
- Numeric column detection
- Percentage of numeric data
- Data type analysis

### Visualization
- Line charts for data trends
- Responsive design
- Dark theme optimized
- Interactive tooltips

### User Experience
- Drag and drop file upload
- Real-time analysis
- Error handling
- Loading states
- Mobile responsive

## Development

### Available Scripts

- `npm start`: Start development server
- `npm test`: Run tests
- `npm run build`: Build for production
- `npm run eject`: Eject from Create React App (irreversible)

### Code Quality

- TypeScript for type safety
- ESLint for code linting
- Prettier for code formatting
- React best practices

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if necessary
5. Submit a pull request

## License

This project is part of the AIE Portfolio and follows the same licensing terms.

## Support

For questions or support, please check the main AIE Portfolio documentation or create an issue in the repository.
