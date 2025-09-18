@echo off
echo Testing Qwen API Connection...
echo.

REM Navigate to the correct Node.js directory
set NODE_PATH=..\..\nodejs\node-v18.19.0-win-x64

echo This script will help you test your Qwen API connection.
echo.
echo 1. Make sure you have an API key from Alibaba Cloud DashScope
echo 2. Configure your API key in the AI Talk application
echo 3. Try sending a test message like "Hello, how are you?"
echo.
echo If you still get errors, check:
echo - Your API key is correct and starts with 'sk-'
echo - You have credits in your DashScope account
echo - Your internet connection is working
echo - The endpoint URL is: https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
echo.
echo Common error solutions:
echo - ERR_NAME_NOT_RESOLVED: Check internet connection
echo - 401 Unauthorized: Check API key
echo - 402 Payment Required: Add credits to account
echo - 429 Too Many Requests: Wait and try again
echo.
pause
