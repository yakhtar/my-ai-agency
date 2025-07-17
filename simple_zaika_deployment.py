#!/usr/bin/env python3
"""
🚀 Simple Zaika AI Agent Deployment
Quick deployment script to get your Zaika bot live for client demos

This creates a simple Flask web interface that showcases your AI agent
capabilities to potential clients.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

try:
    from flask import Flask, request, jsonify, render_template_string
    from zaika_bot import ZaikaAIAgent
except ImportError as e:
    print(f"⚠️ Missing required packages. Please install:")
    print("pip install flask")
    print("Make sure zaika_bot.py is in the same directory")
    sys.exit(1)

app = Flask(__name__)

# Initialize Zaika AI Agent
try:
    zaika_agent = ZaikaAIAgent()
    print("✅ Zaika AI Agent initialized successfully!")
except Exception as e:
    print(f"❌ Error initializing Zaika agent: {e}")
    sys.exit(1)

# Simple HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zaika BBQ Grill - AI Assistant Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 90%;
            max-width: 800px;
            height: 600px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #d4481f 0%, #ff6b35 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2rem;
            margin-bottom: 5px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1rem;
        }
        
        .chat-container {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8f9fa;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .message {
            max-width: 80%;
            padding: 15px;
            border-radius: 15px;
            animation: fadeIn 0.3s ease-in;
        }
        
        .user-message {
            background: #007bff;
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 5px;
        }
        
        .bot-message {
            background: white;
            color: #333;
            border: 1px solid #e9ecef;
            margin-right: auto;
            border-bottom-left-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .input-section {
            padding: 20px;
            background: white;
            border-top: 1px solid #e9ecef;
            display: flex;
            gap: 10px;
        }
        
        .input-section input {
            flex: 1;
            padding: 15px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s ease;
        }
        
        .input-section input:focus {
            border-color: #d4481f;
        }
        
        .input-section button {
            padding: 15px 30px;
            background: linear-gradient(135deg, #d4481f 0%, #ff6b35 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: transform 0.2s ease;
        }
        
        .input-section button:hover {
            transform: translateY(-2px);
        }
        
        .footer {
            text-align: center;
            padding: 10px;
            font-size: 0.9rem;
            color: #666;
            background: #f8f9fa;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 10px;
            color: #666;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .demo-badge {
            position: absolute;
            top: 20px;
            right: 20px;
            background: #ff6b35;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        @media (max-width: 768px) {
            .container {
                width: 95%;
                height: 90vh;
            }
            
            .header h1 {
                font-size: 1.5rem;
            }
            
            .message {
                max-width: 95%;
            }
        }
    </style>
</head>
<body>
    <div class="demo-badge">🚀 LIVE AI DEMO</div>
    
    <div class="container">
        <div class="header">
            <h1>🍢 Zaika BBQ Grill</h1>
            <p>AI-Powered Culinary Concierge</p>
        </div>
        
        <div class="chat-container" id="chat-container">
            <div class="message bot-message">
                <strong>Zaika Assistant:</strong> Welcome to Zaika BBQ Grill! I'm your AI culinary concierge, ready to help you discover our amazing Pakistani cuisine. What would you like to know about our menu today?
            </div>
        </div>
        
        <div class="loading" id="loading">
            <em>Zaika Assistant is thinking...</em>
        </div>
        
        <div class="input-section">
            <input type="text" id="user-input" placeholder="Ask me about our menu, recommendations, or anything else..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Send</button>
        </div>
        
        <div class="footer">
            <p>📍 1199 Amboy Ave, Edison, NJ 08837 | 📞 (732) 709-3700 | 🌐 zaikabbqgrill.com</p>
            <p><em>Powered by Yasser Akhtar AI Agency</em></p>
        </div>
    </div>
    
    <script>
        const chatContainer = document.getElementById('chat-container');
        const userInput = document.getElementById('user-input');
        const loading = document.getElementById('loading');
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;
            
            // Add user message
            addMessage(message, 'user');
            userInput.value = '';
            
            // Show loading
            loading.style.display = 'block';
            
            // Send to AI
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({message: message})
            })
            .then(response => response.json())
            .then(data => {
                loading.style.display = 'none';
                if (data.response) {
                    addMessage(data.response, 'bot');
                } else {
                    addMessage('Sorry, I encountered an error. Please try again.', 'bot');
                }
            })
            .catch(error => {
                loading.style.display = 'none';
                addMessage('Sorry, I encountered an error. Please try again.', 'bot');
                console.error('Error:', error);
            });
        }
        
        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            
            if (sender === 'user') {
                messageDiv.innerHTML = text;
            } else {
                messageDiv.innerHTML = `<strong>Zaika Assistant:</strong> ${text}`;
            }
            
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        // Auto-focus on input
        userInput.focus();
        
        // Demo suggestions
        const suggestions = [
            "What's your most popular dish?",
            "I'm vegetarian, what do you recommend?",
            "What's good for someone who doesn't like spicy food?",
            "Tell me about your lamb chops",
            "What are your hours?",
            "Do you have delivery?",
            "I'm planning a party for 10 people"
        ];
        
        // Show a suggestion every 30 seconds if no activity
        let inactivityTimer;
        
        function resetInactivityTimer() {
            clearTimeout(inactivityTimer);
            inactivityTimer = setTimeout(() => {
                const randomSuggestion = suggestions[Math.floor(Math.random() * suggestions.length)];
                userInput.placeholder = `Try: "${randomSuggestion}"`;
                setTimeout(() => {
                    userInput.placeholder = "Ask me about our menu, recommendations, or anything else...";
                }, 5000);
            }, 30000);
        }
        
        userInput.addEventListener('input', resetInactivityTimer);
        userInput.addEventListener('keypress', resetInactivityTimer);
        
        resetInactivityTimer();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Main chat interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_message = data['message']
        
        # Process with Zaika agent
        response = zaika_agent.generate_sophisticated_response(user_message)
        
        return jsonify({
            'response': response,
            'timestamp': '2024-01-01T12:00:00Z'
        })
        
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'agent': 'zaika_ai_agent',
        'version': '1.0.0',
        'powered_by': 'Yasser Akhtar AI Agency'
    })

if __name__ == '__main__':
    print("🚀 Starting Zaika AI Agent Demo Server...")
    print("📱 Open your browser to: http://localhost:5000")
    print("🎯 Perfect for client demonstrations!")
    print("💼 Built by Yasser Akhtar AI Agency")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)