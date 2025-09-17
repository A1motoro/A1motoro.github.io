# AI Talk - Qwen Chat Assistant

A modern, responsive AI chat interface powered by Qwen AI, featuring a beautiful Monokai-themed design.

## 📁 Folder Structure

```
ai-talk/
├── index.html          # Main chat interface
├── .env               # Environment configuration (local development)
└── README.md          # This documentation
```

## 🚀 Features

- **Real-time AI Chat** with Qwen AI assistant
- **Monokai Theme** integration with your site's design
- **Responsive Design** for desktop, tablet, and mobile
- **Session Statistics** and chat management
- **Environment Configuration** for easy setup
- **Local Storage** for API key persistence

## 🔧 Configuration

### Environment Variables (.env)

For local development, create a `.env` file in this folder:

```env
# AI Talk Configuration
# Qwen API Configuration for local development
QWEN_API_KEY=your_qwen_api_key_here
QWEN_API_ENDPOINT=https://api.qwen.ai/v1/chat/completions

# UI Configuration
MAX_TOKENS=1000
TEMPERATURE=0.7
MODEL=qwen-turbo

# Development settings
DEBUG=false
```

### Manual Configuration

In production (GitHub Pages), configure the API key manually:
1. Visit `your-site.com/ai-talk/`
2. Enter your Qwen API key in the sidebar
3. Click "Save Configuration"

## 🛠️ Usage

### Local Development
1. Start a local server: `python -m http.server 8000`
2. Visit: `http://localhost:8000/ai-talk/`
3. The .env file will be automatically loaded

### Production (GitHub Pages)
1. Visit: `https://yourusername.github.io/ai-talk/`
2. Manually enter your API key

## 🔑 API Key Setup

1. Get your Qwen API key from [Qwen Platform](https://qwen.ai/)
2. Add it to the `.env` file (local) or enter manually (production)
3. The interface supports both methods seamlessly

## 🎨 Customization

The chat interface uses your existing Monokai theme and integrates with your site's core framework. All styling is contained within the HTML file for easy customization.

## 📱 Responsive Design

- **Desktop**: Full sidebar with statistics
- **Tablet**: Condensed layout
- **Mobile**: Single-column layout with collapsible elements

## 🔒 Security Note

The API key is stored locally in the browser's localStorage. Never commit API keys to version control.
