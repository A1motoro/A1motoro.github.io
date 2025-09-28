# AIE Analyzers - AI & Data Analysis Tools

A collection of modern web applications for AI interaction and data analysis, built with React and TypeScript. This repository contains both legacy vanilla JavaScript tools and modern React applications with AI integration.

## 🌐 Live Deployments

### [🤖 AI Talk - Qwen Chat](https://a1motoro.github.io/analyzers/ai-talk/)
Modern React application with intelligent conversational AI powered by Alibaba Cloud's Qwen model. Features markdown rendering and syntax highlighting.

### [📊 CSV Data Analyzer (React)](https://a1motoro.github.io/analyzers/data-analyzer/)
Advanced React-based CSV analysis with AI-powered insights, interactive Chart.js visualizations, and comprehensive statistical reporting.

### [🏠 Main Portal](https://a1motoro.github.io/analyzers/)
Homepage featuring all available tools and applications with modern UI.

### Legacy Tools
- **`csv-analyzer.html`** - Original vanilla JavaScript CSV analyzer
- **`csv-analyzer-js.html`** - Alternative JavaScript implementation

## CSV Data Analyzer

A powerful web-based CSV data analysis tool that provides:

### Features
- **File Upload**: Drag and drop or click to upload CSV files
- **Statistical Analysis**: Comprehensive statistics including mean, median, mode, standard deviation
- **Data Quality Assessment**: Missing values detection and duplicate row identification
- **Visualizations**: Multiple chart types including:
  - Data quality overview (doughnut chart)
  - Distribution charts (bar charts)
  - Correlation matrix
  - Scatter plots
  - Data types distribution
  - Missing values by column
- **Advanced Analysis**: AI-powered insights and recommendations
- **Export Options**: Export analysis reports, processed data, and charts

### Usage
1. Open `csv-analyzer.html` in your web browser
2. Upload a CSV file using the upload interface
3. View the automatic analysis and visualizations
4. Export results as needed

### Technical Details
- Built with vanilla JavaScript
- Uses Chart.js for visualizations
- PapaParse for CSV parsing
- Responsive design with modern dark theme
- No server required - runs entirely in the browser

### Browser Compatibility
- Chrome/Edge (recommended)
- Firefox
- Safari
- Mobile browsers

## File Structure
```
data-analysis/
├── csv-analyzer.html    # Main CSV analysis tool
├── css/                 # Styling files
│   └── monokai-theme.css
└── README.md           # This file
```

## 🚀 Deployment & Development

### GitHub Pages Deployment
This project uses automated deployment via GitHub Actions:

- **AI Talk App**: Deploys to `/analyzers/ai-talk/` when `ai-talk-react/` files change
- **Data Analyzer**: Deploys to `/analyzers/data-analyzer/` when `data-analyzer-react/` files change
- **Main Portal**: Served from `/analyzers/index.html`

### Local Development

#### AI Talk App:
```bash
cd ai-talk-react
npm install
npm start
```

#### Data Analyzer:
```bash
cd data-analyzer-react
npm install
npm start
```

#### Manual Deployment:
```bash
# From each React app directory
npm run deploy
```

### Technologies Used

#### Modern React Applications:
- **React 18** with hooks and concurrent features
- **TypeScript** for type safety
- **Chart.js** for data visualizations
- **PapaParse** for CSV processing
- **React Markdown** for markdown rendering
- **React Syntax Highlighter** for code highlighting
- **Qwen AI** for intelligent analysis

#### Legacy Tools:
- **Vanilla JavaScript** for browser-based analysis
- **Chart.js** for visualizations
- **PapaParse** for CSV parsing

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Use TypeScript for all new React components
- Follow existing code style and naming conventions
- Add proper error handling and loading states
- Test applications in multiple browsers
- Update documentation for new features

## 📄 License

This project is part of the AIE Portfolio. See individual application READMEs for specific licensing information.

## 🔮 Future Enhancements

### React Applications:
- Support for additional file formats (Excel, JSON, XML)
- Advanced AI analysis with multiple models
- Real-time collaboration features
- Custom dashboard creation
- Data export in multiple formats

### Legacy Tools:
- Migration to React/TypeScript
- Enhanced visualizations
- Machine learning integrations
- Performance optimizations
