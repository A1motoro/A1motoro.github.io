# AI Talk - React TypeScript

A modern, intelligent chat interface for Qwen AI assistant built with React and TypeScript. This application provides a seamless conversational experience with advanced AI capabilities.

## Features

- 🤖 **Qwen AI Integration**: Chat with Qwen AI assistant for intelligent conversations
- 💬 **Real-time Chat**: Instant messaging with typing indicators
- ⚙️ **API Configuration**: Easy setup of API keys and endpoints
- 📊 **Session Statistics**: Track messages, session time, and connection status
- 🗂️ **Local Storage**: Persistent API configuration
- 🎨 **Modern UI**: Clean, responsive design with dark theme
- ⌨️ **Keyboard Shortcuts**: Enter to send, Shift+Enter for new lines
- 📱 **Mobile Responsive**: Works perfectly on all devices
- ⚡ **TypeScript**: Full type safety and better development experience

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Alibaba Cloud DashScope API key (for Qwen AI)

### Getting Your API Key

1. **Sign up for Alibaba Cloud**: Visit [Alibaba Cloud](https://www.alibabacloud.com/)
2. **Access DashScope**: Go to [DashScope Console](https://dashscope.aliyuncs.com/)
3. **Create API Key**: Navigate to API Keys section and create a new key
4. **Copy Your Key**: Save your API key securely

**Note**: The API key should start with `sk-` and will be used for authentication.

## 🚀 Quick Start Options

### **Option 1: One-Click Setup (Easiest)**
```bash
# Just double-click this file:
setup-and-run.bat
```
This will install everything and start the development server automatically.

### **Option 2: Quick Start (If already installed)**
```bash
# Just double-click this file:
quick-start.bat
```
This checks for existing installation and starts the server.

### **Option 3: Manual Installation**

1. Navigate to the project directory:
```bash
cd analyzers/ai-talk-react
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

## 🛠️ Troubleshooting

If you encounter issues, run the troubleshooting script:
```bash
# Just double-click this file:
troubleshoot.bat
```

This will:
- ✅ Check Node.js and npm installation
- ✅ Verify dependencies are installed
- ✅ Test React and TypeScript imports
- ✅ Provide specific error solutions

### Building for Production

```bash
npm run build
```

This will create a `build` folder with the production-ready files.

## Usage

### Setting Up API Configuration

1. **Get Qwen API Key**: Obtain your API key from the Qwen platform
2. **Configure Endpoint**: Set your API endpoint (default is usually correct)
3. **Save Configuration**: Click "Save Configuration" to store settings locally

### Chatting with AI

1. **Type Your Message**: Enter your message in the text area
2. **Send Message**: Press Enter or click the Send button
3. **View Responses**: AI responses appear in real-time
4. **Track Statistics**: Monitor your conversation stats in the sidebar

### Features Overview

#### API Configuration
- Secure API key storage in localStorage
- Customizable API endpoints
- Environment variable support (.env files)

#### Chat Interface
- Message history with timestamps
- User and AI message differentiation
- Auto-scrolling to latest messages
- Typing indicators during AI responses

#### Statistics & Monitoring
- Message count tracking
- Session time monitoring
- Connection status indicators
- Error handling and feedback

#### User Experience
- Responsive design for all screen sizes
- Keyboard navigation support
- Error messages and loading states
- Clean, accessible interface

## Project Structure

```
ai-talk-react/
├── public/
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── App.tsx          # Main application component
│   ├── App.css          # Main application styles
│   ├── index.tsx        # React entry point
│   └── index.css        # Global styles
├── package.json         # Dependencies and scripts
├── tsconfig.json        # TypeScript configuration
└── README.md           # This file
```

## Technologies Used

- **React 18**: Modern React with hooks and concurrent features
- **TypeScript**: Type-safe JavaScript with interfaces and type checking
- **CSS Grid & Flexbox**: Responsive layout system
- **Local Storage API**: Persistent data storage
- **Fetch API**: Modern HTTP client for API communication

## Key Components

### App.tsx
The main application component containing:
- State management for messages, API config, and statistics
- Chat functionality with Qwen AI integration
- UI rendering and event handling
- Local storage integration

### Features in Detail

#### Message Management
- Unique message IDs with timestamps
- Message type differentiation (user vs AI)
- Auto-scrolling message container
- Message persistence during session

#### API Integration
- RESTful API communication with Qwen
- Error handling and retry logic
- Configurable API parameters
- Secure API key management

#### Responsive Design
- Mobile-first approach
- Flexible grid layouts
- Touch-friendly interface
- Adaptive typography

#### Performance Optimizations
- Efficient state updates
- Optimized re-renders
- Lazy loading where applicable
- Memory leak prevention

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

### Environment Variables

Create a `.env` file in the root directory for environment-specific configuration:

```
QWEN_API_KEY=your_api_key_here
QWEN_API_ENDPOINT=https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper TypeScript types
4. Test thoroughly
5. Submit a pull request

## API Reference

### Qwen AI API

The application integrates with Qwen's chat completion API:

- **Endpoint**: Configurable (default: https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions)
- **Model**: qwen-turbo
- **Parameters**:
  - max_tokens: 1000
  - temperature: 0.7

### Local Storage

Configuration is stored locally:
- Key: `qwen-api-config`
- Format: JSON with `key` and `endpoint` properties

## Troubleshooting

### Common Issues

1. **API Key Not Working**
   - Verify your API key is correct and starts with `sk-`
   - Check API endpoint URL (should be DashScope endpoint)
   - Ensure API has proper permissions in Alibaba Cloud
   - Check your account balance/credits in DashScope

2. **"Failed to load resource: net::ERR_NAME_NOT_RESOLVED"**
   - This means the API endpoint domain cannot be resolved
   - Verify you're using the correct DashScope endpoint: `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
   - Check your internet connection
   - Try refreshing the page or clearing browser cache

3. **"Failed to load resource: the server responded with a status of 404" for .env**
   - This is normal - the .env file is optional
   - Configure your API key directly in the application interface instead
   - The app will work without the .env file

4. **Messages Not Sending**
   - Check internet connection
   - Verify API configuration is saved
   - Look for error messages in browser console
   - Ensure your API key has sufficient credits

5. **UI Not Loading**
   - Clear browser cache and cookies
   - Check Node.js version (should be v16+)
   - Reinstall dependencies: `npm install`
   - Try a different browser

6. **CORS Errors**
   - If you see CORS-related errors, try using a different browser or disable CORS temporarily for testing
   - The production build should work better with CORS

### API Error Messages

**"API request failed: 401"**: Invalid API key
- Double-check your API key from DashScope console
- Ensure the key starts with `sk-`

**"API request failed: 429"**: Rate limit exceeded
- Wait a few minutes before trying again
- Check your API usage limits in DashScope

**"API request failed: 402"**: Insufficient credits
- Add credits to your Alibaba Cloud account
- Check your billing status in DashScope console

### Debug Mode

Enable debug logging by opening browser developer tools and checking the console for detailed error messages.

## Security Considerations

- API keys are stored in localStorage (client-side only)
- No sensitive data is transmitted except to the configured API endpoint
- All communication uses HTTPS
- Input validation prevents malicious content

## Performance

- Optimized bundle size
- Efficient state management
- Minimal re-renders
- Lazy loading for better initial load times

## Future Enhancements

- Message history export
- Multiple conversation threads
- Voice input/output
- File upload capabilities
- Advanced formatting options
- Conversation themes
- Offline mode support

## License

This project is part of the AIE Portfolio and follows the same licensing terms.

## Support

For questions or support, please check the main AIE Portfolio documentation or create an issue in the repository.
