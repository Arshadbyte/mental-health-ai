from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def whatsapp_webhook():
    """
    Webhook to handle incoming WhatsApp messages via Twilio.
    """
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')
    
    # Create a Twilio response object
    resp = MessagingResponse()
    msg = resp.message()
    
    # Simple response logic (can be enhanced with AI integration)
    if 'hello' in incoming_msg or 'hi' in incoming_msg:
        response_text = "Hello! I'm your AI Mental Health Companion. How are you feeling today?"
    elif 'mood' in incoming_msg:
        response_text = "I'd love to help you track your mood. On a scale of 1-10, how would you rate your current mood?"
    elif 'help' in incoming_msg:
        response_text = "I'm here to support your mental health journey. You can:\n• Share how you're feeling\n• Ask for mood tracking\n• Request breathing exercises\n• Get mental health tips"
    elif 'breathing' in incoming_msg or 'breathe' in incoming_msg:
        response_text = "Let's do a quick breathing exercise:\n1. Inhale for 4 seconds\n2. Hold for 7 seconds\n3. Exhale for 8 seconds\nRepeat this 3 times. You've got this! 🌟"
    elif any(word in incoming_msg for word in ['sad', 'depressed', 'down', 'anxious', 'worried']):
        response_text = "I hear that you're going through a tough time. Remember, it's okay to feel this way. Would you like to try a breathing exercise or talk about what's on your mind?"
    elif any(word in incoming_msg for word in ['happy', 'good', 'great', 'excellent']):
        response_text = "That's wonderful to hear! I'm so glad you're feeling good. What's contributing to your positive mood today?"
    else:
        response_text = "Thank you for sharing that with me. I'm here to listen and support you. Is there anything specific I can help you with today?"
    
    msg.body(response_text)
    
    return str(resp)

@app.route("/", methods=['GET'])
def home():
    return "WhatsApp Mental Health Bot is running!"

if __name__ == "__main__":
    # Note: In production, you would need to:
    # 1. Set up a Twilio account
    # 2. Configure WhatsApp Business API
    # 3. Set up webhook URL (using ngrok for local testing)
    # 4. Add proper environment variables for Twilio credentials
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

