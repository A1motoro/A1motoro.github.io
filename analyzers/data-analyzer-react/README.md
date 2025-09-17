# CSV Data Analyzer - React TypeScript

A modern, powerful CSV data analysis tool built with React and TypeScript. This analyzer provides comprehensive data insights with beautiful visualizations and interactive features.

## Features

- 📊 **CSV File Upload**: Drag and drop or click to upload CSV files
- 📈 **Interactive Charts**: Beautiful line charts using Chart.js
- 📋 **Data Statistics**: Comprehensive statistical analysis
- 📋 **Data Preview**: Sample data table view
- 🎨 **Modern UI**: Clean, responsive design with dark theme
- ⚡ **TypeScript**: Full type safety and better development experience
- 📱 **Responsive**: Works on desktop and mobile devices

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Navigate to the project directory:
```bash
cd analyzers/data-analyzer-react
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
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
