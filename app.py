
import streamlit as st
import os
from dotenv import load_dotenv
import pymysql
from datetime import datetime

# Load environment variables
load_dotenv()

# Database connection (using TiDB Cloud credentials)
def get_db_connection():
    return pymysql.connect(
        host=os.getenv('TIDB_HOST'),
        user=os.getenv('TIDB_USER'),
        password=os.getenv('TIDB_PASSWORD'),
        database=os.getenv('TIDB_DATABASE'),
        port=int(os.getenv('TIDB_PORT', 4000)),
        ssl_verify_identity=True,
        ssl_ca=os.getenv('TIDB_CA_PATH') # Path to your CA certificate
    )

# --- Streamlit App --- #
st.set_page_config(page_title='AI Mental Health Companion', layout='wide')
st.title('🧠 AI Mental Health Companion')

# Sidebar for navigation
st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', ['Chat', 'Mood Tracker', 'Journal', 'Settings'])

if page == 'Chat':
    st.header('💬 Chat with your Companion')
    # Chatbot interface will go here
    st.write('Chat functionality coming soon!')

elif page == 'Mood Tracker':
    st.header('😊 Mood Tracker')
    # Mood tracking interface will go here
    st.write('Mood tracking functionality coming soon!')

elif page == 'Journal':
    st.header('✍️ Daily Journal')
    # Journaling interface will go here
    st.write('Journaling functionality coming soon!')

elif page == 'Settings':
    st.header('⚙️ Settings')
    st.write('Settings functionality coming soon!')



