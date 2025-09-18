import React, { useState, useEffect, useRef } from 'react';
import './App.css';

// Types
interface Message {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
}

interface ApiConfig {
  key: string;
  endpoint: string;
}

interface ChatStats {
  messages: number;
  sessionTime: string;
  status: 'Ready' | 'Thinking...' | 'Error';
}

const App: React.FC = () => {
  // State management
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'ai',
      content: "Hello! I'm Qwen, your AI assistant. How can I help you today? Feel free to ask me questions about programming, mathematics, creative ideas, or anything else you're curious about!",
      timestamp: new Date()
    }
  ]);

  const [apiConfig, setApiConfig] = useState<ApiConfig>({
    key: '',
    endpoint: 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
  });

  
  const [chatStats, setChatStats] = useState<ChatStats>({
    messages: 1,
    sessionTime: '00:00',
    status: 'Ready'
  });

  const [currentMessage, setCurrentMessage] = useState<string>('');
  const [isTyping, setIsTyping] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [sessionStart] = useState<Date>(new Date());

  // Refs
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatInputRef = useRef<HTMLTextAreaElement>(null);

  // Load API config from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('qwen-api-config');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setApiConfig(parsed);
      } catch (error) {
        console.error('Error parsing saved API config:', error);
      }
    }

    // Load environment config (if available)
    loadEnvironmentConfig();
  }, []);

  // Update session time every second
  useEffect(() => {
    const interval = setInterval(updateSessionTime, 1000);
    return () => clearInterval(interval);
  }, [sessionStart]);

  // Auto-scroll to bottom when new messages are added
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadEnvironmentConfig = async () => {
    try {
      // Try to load .env file (only works locally with a server)
      const response = await fetch('./.env');
      if (response.ok) {
        const envText = await response.text();
        const envVars = parseEnvFile(envText);

        if (envVars.QWEN_API_KEY && envVars.QWEN_API_KEY !== 'your_qwen_api_key_here') {
          setApiConfig((prev: ApiConfig) => ({ ...prev, key: envVars.QWEN_API_KEY }));
        }

        if (envVars.QWEN_API_ENDPOINT) {
          setApiConfig((prev: ApiConfig) => ({ ...prev, endpoint: envVars.QWEN_API_ENDPOINT }));
        }

        console.log('Environment configuration loaded from .env file');
      }
    } catch (error) {
      console.log('No .env file found, using manual configuration');
    }
  };

  const parseEnvFile = (envText: string): Record<string, string> => {
    const envVars: Record<string, string> = {};
    const lines = envText.split('\n');

    for (const line of lines) {
      const trimmedLine = line.trim();
      if (trimmedLine && !trimmedLine.startsWith('#')) {
        const [key, ...valueParts] = trimmedLine.split('=');
        if (key && valueParts.length > 0) {
          envVars[key.trim()] = valueParts.join('=').trim();
        }
      }
    }

    return envVars;
  };

  const updateSessionTime = () => {
    const elapsed = Math.floor((Date.now() - sessionStart.getTime()) / 1000);
    const minutes = Math.floor(elapsed / 60);
    const seconds = elapsed % 60;
    const formattedTime = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

    setChatStats((prev: ChatStats) => ({ ...prev, sessionTime: formattedTime }));
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const saveApiConfig = () => {
    localStorage.setItem('qwen-api-config', JSON.stringify(apiConfig));

    // Visual feedback (you could enhance this with a toast notification)
    console.log('API configuration saved successfully');
  };

  const handleApiConfigChange = (field: keyof ApiConfig, value: string) => {
    setApiConfig((prev: ApiConfig) => ({ ...prev, [field]: value }));
  };

  const addMessage = (type: 'user' | 'ai', content: string) => {
    const newMessage: Message = {
      id: Date.now().toString() + Math.random().toString(36).substring(2, 11),
      type,
      content,
      timestamp: new Date()
    };

    setMessages((prev: Message[]) => [...prev, newMessage]);
    setChatStats((prev: ChatStats) => ({ ...prev, messages: prev.messages + 1 }));
  };

  const clearChat = () => {
    if (window.confirm('Are you sure you want to clear all messages?')) {
      setMessages([
        {
          id: '1',
          type: 'ai',
          content: "Chat cleared! How can I help you today?",
          timestamp: new Date()
        }
      ]);
      setChatStats((prev: ChatStats) => ({ ...prev, messages: 1, status: 'Ready' }));
      setError('');
    }
  };

  const showError = (message: string) => {
    setError(message);
    setTimeout(() => setError(''), 5000);
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
                content: 'You are Qwen, a helpful and intelligent AI assistant. Provide clear, accurate, and engaging responses.'
              },
              {
                role: 'user',
                content: message
              }
            ]
          },
          parameters: {
            max_tokens: 1000,
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
                content: 'You are Qwen, a helpful and intelligent AI assistant. Provide clear, accurate, and engaging responses.'
              },
              {
                role: 'user',
                content: message
              }
            ],
            max_tokens: 1000,
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

  const sendMessage = async () => {
    const message = currentMessage.trim();
    if (!message) return;

    if (!apiConfig.key) {
      showError('Please configure your Qwen API key first!');
      return;
    }

    // Add user message
    addMessage('user', message);
    setCurrentMessage('');

    // Show typing indicator
    setIsTyping(true);
    setChatStats((prev: ChatStats) => ({ ...prev, status: 'Thinking...' }));

    try {
      const response = await callQwenAPI(message);
      addMessage('ai', response);
      setChatStats((prev: ChatStats) => ({ ...prev, status: 'Ready' }));
    } catch (error) {
      console.error('API Error:', error);
      showError('Failed to get response from Qwen API. Please check your API key and try again.');
      setChatStats((prev: ChatStats) => ({ ...prev, status: 'Error' }));
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="ai-talk-container">
      <div className="chat-header">
        <h1 className="chat-title">AI Talk - Qwen Assistant</h1>
        <p className="chat-subtitle">
          Have intelligent conversations with Qwen AI. Ask questions, get coding help, and explore creative ideas.
        </p>
      </div>

      <div className="chat-layout">
        {/* Sidebar */}
        <div className="chat-sidebar">
          <div className="api-config">
            <h3><i className="fas fa-key"></i> API Configuration</h3>
            <div className="api-input-group">
              <label className="api-label" htmlFor="api-key">Qwen API Key:</label>
              <input
                type="password"
                id="api-key"
                className="api-input"
                placeholder="Enter your Qwen API key here..."
                value={apiConfig.key}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleApiConfigChange('key', e.target.value)}
              />
            </div>
            <div className="api-input-group">
              <label className="api-label" htmlFor="api-endpoint">API Endpoint:</label>
              <input
                type="text"
                id="api-endpoint"
                className="api-input"
                placeholder="API endpoint URL"
                value={apiConfig.endpoint}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleApiConfigChange('endpoint', e.target.value)}
              />
            </div>
            <button className="api-save-btn" onClick={saveApiConfig}>
              <i className="fas fa-save"></i> Save Configuration
            </button>
          </div>

          <div className="chat-stats">
            <div className="stat-item">
              <span>Messages:</span>
              <span className="stat-value">{chatStats.messages}</span>
            </div>
            <div className="stat-item">
              <span>Session:</span>
              <span className="stat-value">{chatStats.sessionTime}</span>
            </div>
            <div className="stat-item">
              <span>Status:</span>
              <span className="stat-value">{chatStats.status}</span>
            </div>
          </div>

          <button className="clear-chat-btn" onClick={clearChat}>
            <i className="fas fa-trash"></i> Clear Chat
          </button>
        </div>

        {/* Main Chat Area */}
        <div className="chat-main">
          <div className="chat-messages">
            {messages.map((message: Message) => (
              <div key={message.id} className={`message ${message.type}`}>
                <div className="message-header">
                  <i className={`fas ${message.type === 'user' ? 'fa-user' : 'fa-robot'}`}></i>
                  {message.type === 'user' ? 'You' : 'Qwen AI'}
                </div>
                <div className="message-content">{message.content}</div>
              </div>
            ))}

            {isTyping && (
              <div className="typing-indicator">
                <i className="fas fa-circle-notch fa-spin"></i> Qwen is thinking...
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {error && (
            <div className="error-message">
              ❌ {error}
            </div>
          )}

          <div className="chat-input-area">
            <textarea
              ref={chatInputRef}
              className="chat-input"
              placeholder="Type your message here... (Press Enter to send, Shift+Enter for new line)"
              rows={3}
              value={currentMessage}
              onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setCurrentMessage(e.target.value)}
              onKeyPress={handleKeyPress}
            />
            <button
              className="send-btn"
              onClick={sendMessage}
              disabled={!currentMessage.trim() || isTyping}
            >
              <i className="fas fa-paper-plane"></i> Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
