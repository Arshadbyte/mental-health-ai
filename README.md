# 🧠 AI Mental Health Companion

An advanced AI-powered mental health companion application built with Streamlit, featuring mood tracking, journaling, voice interaction, image-based emotion detection, and comprehensive wellness coaching.

## 🌟 Features

### Core Functionality
- **AI Chat Companion**: Intelligent conversational AI for mental health support
- **Mood Tracking**: Visual mood logging with intensity tracking and analytics
- **Daily Journaling**: Secure personal journaling with prompts and insights
- **Voice Interaction**: Speech-to-text input and text-to-speech responses
- **Emotion Detection**: Facial emotion analysis from uploaded photos
- **Wellness Coach**: Guided breathing exercises and sleep tracking

### Advanced Features
- **WhatsApp Integration**: Mental health support via WhatsApp messaging
- **REST API**: Complete API for external integrations
- **User Authentication**: Secure JWT-based authentication system
- **Data Export**: Export all personal data in CSV format
- **Analytics Dashboard**: Comprehensive insights and trend analysis
- **Notification System**: Customizable reminders and wellness alerts

## 🏗️ Architecture

### Technology Stack
- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Flask with CORS support
- **Database**: TiDB Cloud (MySQL-compatible)
- **AI/ML**: 
  - Local LLM integration (LM Studio + Mistral/Phi-3)
  - Sentence Transformers for embeddings (when available)
  - DeepFace for emotion detection
- **Authentication**: JWT tokens with secure password hashing
- **Voice Processing**: SpeechRecognition + pyttsx3
- **Messaging**: Twilio for WhatsApp integration

### Project Structure
```
mental_health_ai/
├── streamlit_app.py              # Main Streamlit application
├── api_server.py                 # REST API server
├── auth_system.py                # Authentication system
├── whatsapp_integration.py       # WhatsApp bot integration
├── mood_detector.py              # Facial emotion detection
├── audio_utils.py                # Voice input/output utilities
├── data_exporter.py              # Data export functionality
├── notification_system.py        # Reminder and notification system
├── wellness_coach.py             # Breathing exercises and sleep tracking
├── test_suite.py                 # Comprehensive test suite
├── requirements.txt              # Python dependencies
├── README.md                     # This documentation
└── mental_health/                # Original project files
    ├── full_mental_health_bot.py # Original console-based bot
    ├── isrgrootx1.pem            # TiDB SSL certificate
    └── ...                       # Other original files
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- TiDB Cloud account (for database)
- LM Studio (for local LLM)
- Twilio account (for WhatsApp integration, optional)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd mental_health_ai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file with:
   ```env
   # TiDB Configuration
   TIDB_HOST=gateway01.us-west-2.prod.aws.tidbcloud.com
   TIDB_USER=DbYbZAnbhjP7LZB.root
   TIDB_PASSWORD=PMo7rCUvUA5Kv9Id
   TIDB_DATABASE=test
   TIDB_PORT=4000
   TIDB_CA_PATH=mental_health/isrgrootx1.pem
   
   # Authentication
   SECRET_KEY=your-secret-key-change-in-production
   JWT_SECRET=jwt-secret-key-change-in-production
   
   # Twilio (Optional)
   TWILIO_ACCOUNT_SID=your-twilio-account-sid
   TWILIO_AUTH_TOKEN=your-twilio-auth-token
   ```

4. **Set up LM Studio:**
   - Download and install LM Studio
   - Load a model (Mistral 7B or Phi-3 recommended)
   - Start the local server on `http://localhost:1234`

### Running the Application

#### Option 1: Streamlit Web App (Recommended)
```bash
streamlit run streamlit_app.py
```
Access at: `http://localhost:8501`

#### Option 2: API Server
```bash
python api_server.py
```
API available at: `http://localhost:5001`

#### Option 3: WhatsApp Bot
```bash
python whatsapp_integration.py
```
Webhook available at: `http://localhost:5000`

#### Option 4: Authentication Server
```bash
python auth_system.py
```
Auth API available at: `http://localhost:5002`

## 📱 Usage Guide

### Web Application
1. **Dashboard**: Overview of your mental health journey
2. **Chat**: Interact with the AI companion
3. **Mood Tracker**: Log daily moods and view trends
4. **Journal**: Write and review personal entries
5. **Wellness Coach**: Access breathing exercises and sleep tracking
6. **Analytics**: View detailed insights and export data
7. **Settings**: Customize notifications and privacy settings

### API Endpoints

#### Chat API
```bash
POST /api/chat
{
  "message": "How are you feeling today?"
}
```

#### Mood Tracking
```bash
POST /api/mood
{
  "mood": "happy",
  "intensity": 8,
  "notes": "Great day at work!"
}
```

#### Journal Entries
```bash
POST /api/journal
{
  "title": "Daily Reflection",
  "content": "Today I learned..."
}
```

#### Analytics
```bash
GET /api/analytics
```

### Authentication
```bash
# Register
POST /api/auth/register
{
  "username": "user123",
  "email": "user@example.com",
  "password": "securepassword"
}

# Login
POST /api/auth/login
{
  "username": "user123",
  "password": "securepassword"
}
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_suite.py
```

The test suite covers:
- Data export functionality
- Notification system
- Wellness coach features
- API endpoints
- Authentication system
- Integration testing

## 🔧 Configuration

### Database Setup
1. Create a TiDB Cloud cluster
2. Create the following tables:
   ```sql
   CREATE TABLE mental_health_tips (
       id INT AUTO_INCREMENT PRIMARY KEY,
       topic VARCHAR(255),
       tip_text TEXT,
       embedding BLOB
   );
   
   CREATE TABLE mood_logs (
       id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT,
       timestamp DATETIME,
       mood VARCHAR(50),
       intensity INT,
       notes TEXT
   );
   
   CREATE TABLE chat_history (
       id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT,
       timestamp DATETIME,
       user_input TEXT,
       ai_response TEXT
   );
   ```

### LM Studio Configuration
1. Download a compatible model (Mistral 7B Instruct recommended)
2. Load the model in LM Studio
3. Start the server with default settings
4. Ensure the server is accessible at `http://localhost:1234`

### WhatsApp Integration
1. Set up a Twilio account
2. Configure WhatsApp Business API
3. Set up webhook URL (use ngrok for local testing)
4. Update environment variables with Twilio credentials

## 🚀 Deployment

### Local Development
The application is ready to run locally with all features enabled.

### Production Deployment
For production deployment:

1. **Environment Variables**: Set all required environment variables
2. **Database**: Ensure TiDB Cloud is properly configured
3. **SSL/TLS**: Configure HTTPS for secure communication
4. **Load Balancing**: Use a reverse proxy (nginx) for multiple instances
5. **Monitoring**: Set up logging and monitoring systems

### Docker Deployment (Optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.address", "0.0.0.0"]
```

## 🔒 Security Considerations

- **Authentication**: JWT tokens with expiration
- **Password Security**: Bcrypt hashing for passwords
- **Database Security**: SSL connections to TiDB
- **API Security**: CORS configuration and input validation
- **Data Privacy**: Local data storage options available

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the documentation above
- Run the test suite to diagnose issues
- Review error logs for debugging information

## 🔮 Future Enhancements

- **Mobile App**: React Native or Flutter mobile application
- **Advanced Analytics**: Machine learning insights and predictions
- **Group Therapy**: Multi-user session support
- **Integration**: Calendar, fitness trackers, and other health apps
- **Multilingual Support**: Multiple language options
- **Professional Dashboard**: Tools for therapists and counselors

## 📊 Performance Notes

- **Embedding Models**: Large models (sentence-transformers) may require significant resources
- **Voice Processing**: Real-time voice features require microphone access
- **Image Processing**: Emotion detection requires camera access or image uploads
- **Database**: TiDB Cloud provides scalable database performance

---

**Built with ❤️ for mental health and wellbeing**

