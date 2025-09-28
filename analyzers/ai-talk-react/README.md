# AI Talk - React TypeScript Chat Application

A modern, intelligent chat interface for Qwen AI assistant built with React and TypeScript. This application provides a seamless conversational experience with advanced AI capabilities through Alibaba Cloud DashScope integration.

## ✨ Features

- 🤖 **Qwen AI Integration**: Chat with Qwen AI assistant for intelligent conversations
- 💬 **Real-time Chat**: Instant messaging with typing indicators
- 📝 **Markdown Support**: Full markdown rendering with syntax highlighting
- 🖥️ **Code Blocks**: Monokai-themed syntax highlighting for code snippets
- ⚙️ **API Configuration**: Easy setup of API keys and endpoints with DashScope
- 📊 **Session Statistics**: Track messages, session time, and connection status
- 🗂️ **Local Storage**: Persistent API configuration
- 🎨 **Modern UI**: Clean, responsive design with dark theme
- ⌨️ **Keyboard Shortcuts**: Enter to send, Shift+Enter for new lines
- 📱 **Mobile Responsive**: Works perfectly on all devices
- ⚡ **TypeScript**: Full type safety and better development experience

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v16 or higher)
- **npm** or yarn
- **Alibaba Cloud DashScope API key** (for Qwen AI)

### Getting Your API Key

1. **Sign up for Alibaba Cloud**: Visit [Alibaba Cloud](https://www.alibabacloud.com/)
2. **Access DashScope**: Go to [DashScope Console](https://dashscope.aliyuncs.com/)
3. **Create API Key**: Navigate to API Keys section and create a new key
4. **Copy Your Key**: Save your API key securely (starts with `sk-`)

### Installation & Setup

#### **🚀 Quick Start (Easiest)**
Just **double-click** one of these files in your ai-talk-react folder:

- **`start-local.bat`** - Windows Batch file (recommended)
- **`Start-Local.ps1`** - PowerShell script (alternative)

These will automatically:
- ✅ Navigate to the correct directory
- ✅ Start the development server
- ✅ Open http://localhost:3000 in your browser

#### **Manual Setup**
If you prefer manual control:

1. **Navigate to the project directory**:
```bash
cd analyzers/ai-talk-react
```


2. **Install dependencies** (if not already done):
```bash
npm install
```

3. **Start the development server**:
```bash
npm start
```

4. **Open your browser** to `http://localhost:3000`

### Installing Markdown Features

If you want the full markdown support with syntax highlighting:

```bash
# Double-click this file:
install-markdown.bat
```

Or manually install:
```bash
npm install react-markdown react-syntax-highlighter remark-gfm
```

### Building for Production

```bash
npm run build
```

This creates a `build` folder with production-ready files.

## 🔧 Usage

### Setting Up API Configuration

1. **Get Qwen API Key**: Obtain your API key from DashScope console
2. **Configure Endpoint**: Default endpoint is pre-configured
3. **Save Configuration**: Click "Save Configuration" to store settings locally

### Chatting with AI

1. **Type Your Message**: Enter your message in the text area
2. **Send Message**: Press Enter or click the Send button
3. **View Responses**: AI responses appear in real-time with full markdown formatting
4. **Track Statistics**: Monitor conversation stats in the sidebar

### Markdown Features

The AI responses support full markdown rendering:

- **Headers**: `# ## ###` with proper styling
- **Code Blocks**: ````language` with Monokai syntax highlighting
- **Inline Code**: `code` with pink highlighting
- **Lists**: Ordered and unordered lists
- **Links**: Clickable links with blue styling
- **Blockquotes**: Styled quote blocks
- **Tables**: Full table support with alternating row colors
- **GitHub Flavored Markdown**: Tables, strikethrough, task lists

**Supported Languages**: JavaScript, Python, HTML, CSS, TypeScript, Java, C++, Go, Rust, PHP, Ruby, Swift, Kotlin, and many more!

### Responsive Design Features

- **Mobile-Optimized**: Code blocks and tables adapt to small screens
- **Horizontal Scrolling**: Long code lines scroll horizontally instead of breaking layout
- **Word Wrapping**: Long URLs and text wrap properly
- **Overflow Protection**: Prevents content from breaking the page layout

## 🏗️ Project Structure

```
ai-talk-react/
├── public/
│   ├── index.html          # HTML template
│   └── manifest.json       # Web app manifest
├── src/
│   ├── App.tsx             # Main application component
│   ├── App.css             # Main application styles
│   ├── index.tsx           # React entry point
│   └── index.css           # Global styles
├── package.json            # Dependencies and scripts
├── tsconfig.json           # TypeScript configuration
└── README.md              # This documentation
```

## 🛠️ API Integration

### DashScope Endpoints

The application supports two API endpoint formats for maximum compatibility:

#### **Primary Endpoint (DashScope Native)**:
```
https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
```

#### **Fallback Endpoint (OpenAI Compatible)**:
```
https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
```

### API Configuration

- **Model**: `qwen-turbo`
- **Authentication**: Bearer token (`Bearer sk-your-key`)
- **Parameters**:
  - `max_tokens`: 1000
  - `temperature`: 0.7

### API Response Formats

#### DashScope Native Format:
```json
{
  "output": {
    "text": "Hello! How can I help you today?"
  },
  "usage": {
    "input_tokens": 10,
    "output_tokens": 8
  }
}
```

#### OpenAI Compatible Format:
```json
{
  "choices": [
    {
      "message": {
        "content": "Hello! How can I help you today?"
      }
    }
  ],
  "usage": {
    "total_tokens": 18
  }
}
```

## 🔧 Troubleshooting

### Common Issues & Solutions

#### **401 Unauthorized Error**
```
{"error": "Unauthorized"}
```
**Solution**: Check your API key format - must start with `sk-`

#### **402 Payment Required**
```
{"error": "Insufficient balance"}
```
**Solution**: Add credits to your Alibaba Cloud account

#### **429 Too Many Requests**
```
{"error": "Rate limit exceeded"}
```
**Solution**: Wait a few minutes and try again

#### **Network Resolution Errors**
```
Failed to fetch / ERR_NAME_NOT_RESOLVED
```
**Solution**:
- Check internet connection
- Verify DashScope endpoint URLs
- Try refreshing the page

#### **Messages Not Sending**
**Solutions**:
- Verify API configuration is saved
- Check browser console for errors
- Ensure sufficient API credits
- Confirm internet connectivity

#### **UI Not Loading Properly**
**Solutions**:
- Clear browser cache and cookies
- Verify Node.js version (v16+)
- Reinstall dependencies: `npm install`
- Try a different browser

#### **CORS Errors**
**Solutions**:
- Try a different browser
- The production build handles CORS better
- Disable CORS extensions temporarily for testing

### API Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 401 | Invalid API key | Check key format (must start with `sk-`) |
| 402 | Insufficient credits | Add credits to Alibaba Cloud account |
| 429 | Rate limit exceeded | Wait and retry |
| 400 | Bad request | Check request format |

## 🛠️ Development

### Available Scripts

- `npm start` - Start development server
- `npm test` - Run test suite
- `npm run build` - Build for production
- `npm run eject` - Eject from Create React App (irreversible)

### Environment Variables

Create a `.env` file in the root directory:

```env
QWEN_API_KEY=your_api_key_here
QWEN_API_ENDPOINT=https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
```

### Code Quality

- **TypeScript**: Full type safety with interfaces
- **ESLint**: Code linting and style enforcement
- **React Best Practices**: Modern React patterns and hooks

## 🏗️ Architecture

### Key Components

#### **App.tsx** - Main Component
- State management for messages, API config, and statistics
- Chat functionality with dual API endpoint support
- UI rendering with responsive design
- Local storage integration for persistence

#### **State Management**
- Messages with unique IDs and timestamps
- API configuration (key and endpoint)
- Session statistics tracking
- Error handling and loading states

#### **API Integration Layer**
- Automatic fallback between API formats
- Error handling and retry logic
- Secure API key management
- Request/response parsing

### Technologies Used

- **React 18**: Modern React with hooks and concurrent features
- **TypeScript**: Type-safe JavaScript development
- **CSS Grid & Flexbox**: Responsive layout system
- **Local Storage API**: Client-side data persistence
- **Fetch API**: Modern HTTP client for API communication

## 🔒 Security Considerations

- API keys stored in localStorage (client-side only)
- HTTPS communication with DashScope API
- Input validation and sanitization
- No sensitive data logging

## 📊 Performance Features

- Optimized bundle size
- Efficient state management
- Minimal re-renders with React best practices
- Lazy loading for better initial load times

## 🚀 Future Enhancements

- Message history export functionality
- Multiple conversation thread support
- Voice input/output capabilities
- File upload and processing
- Advanced message formatting options
- Conversation themes and customization
- Offline mode with local AI processing

## 📞 Support

For questions or support:
1. Check browser developer console (F12) for error details
2. Verify API key format and DashScope account status
3. Ensure sufficient credits in Alibaba Cloud account
4. Test API connection through the application interface

## 📄 License

This project is part of the AIE Portfolio and follows the same licensing terms.
