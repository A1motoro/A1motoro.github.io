# Data Analysis Tools

This directory contains data analysis tools and utilities for processing and visualizing data.

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

## Future Enhancements
- Support for additional file formats (Excel, JSON)
- More advanced statistical functions
- Machine learning insights
- Real-time collaboration features
