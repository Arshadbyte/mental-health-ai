
import streamlit as st
import openai, datetime, pandas as pd, os
from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer
import numpy as np
from mood_detector import detect_mood_from_image
from audio_utils import recognize_speech_from_mic, text_to_speech

# ── Models & DB ────────────────────────────────────────────────────
# Note: sentence-transformers and torch installation is problematic in this environment.
# For now, we will proceed with the existing code, but this needs to be addressed for full functionality.
embedder = SentenceTransformer("all-MiniLM-L6-v2")

openai.api_base = "http://localhost:1234/v1"   # LM Studio server
openai.api_key  = "not-needed"

engine = create_engine(
    "mysql+pymysql://DbYbZAnbhjP7LZB.root:PMo7rCUvUA5Kv9Id@"
    "gateway01.us-west-2.prod.aws.tidbcloud.com:4000/test?ssl_ca=/home/ubuntu/mental_health_ai/mental_health/isrgrootx1.pem"
)

LOG_FILE = "mood_logs.csv"

# --- Streamlit App --- #
st.set_page_config(page_title=\'AI Mental Health Companion\', layout=\'wide\')
st.title(\'🧠 AI Mental Health Companion\')

# Sidebar for navigation
st.sidebar.title(\'Navigation\')
page = st.sidebar.radio(\'Go to\', [\'Chat\', \'Mood Tracker\', \'Journal\', \'Settings\'])

if page == \'Chat\':
    st.header(\'💬 Chat with your Companion\')
    user_input = st.text_input("How are you feeling today?", placeholder="e.g., I\'m feeling anxious about exams")

    if st.button("Speak"): # Voice input button
        st.info("Listening...")
        speech_input = recognize_speech_from_mic()
        st.write(f"You said: {speech_input}")
        user_input = speech_input # Use speech as input

    if user_input:
        # 1️⃣  LM Studio reply (completion endpoint = plain text)
        try:
            res = openai.Completion.create(
                model="mistral-7b-instruct-v0.2",
                prompt=f"You are a kind mental‑health assistant.\nUser: {user_input}\nAI:",
                max_tokens=150,
                temperature=0.7,
            )
            ai_reply = res["choices"][0]["text"].strip()
        except Exception as e:
            ai_reply = f"(LM Studio error: {e})"

        # 2️⃣  Best tip from TiDB
        topic = tip_text = ""
        tip_score = 0.0
        try:
            u_vec = embedder.encode(user_input)
            with engine.connect() as conn:
                rows = conn.execute(text("SELECT topic, tip_text, embedding FROM mental_health_tips"))
                best_sim = -1
                for tpc, txt, emb in rows:
                    v = np.frombuffer(emb, dtype=np.float32)
                    sim = np.dot(u_vec, v) / (np.linalg.norm(u_vec) * np.linalg.norm(v))
                    if sim > best_sim:
                        best_sim, topic, tip_text = sim, tpc, txt
                tip_score = best_sim
        except Exception as e:
            tip_text = f"(Tip error: {e})"

        # 3️⃣  Show results
        st.write(f"\n🤖 AI: {ai_reply}")
        if tip_text:
            st.write(f"💡 Tip ({topic}, {tip_score:.2f}): {tip_text}\n")
        else:
            st.write("💡 No tip found.\n")

        # Text to speech for AI reply
        text_to_speech(ai_reply)

        # 4️⃣  Log to CSV
        log_row = {
            "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
            "mood": "",                 # mood tracking will be added later
            "user_input": user_input,
            "ai_reply": ai_reply,
            "tip_topic": topic,
            "tip_text": tip_text,
            "tip_score": round(tip_score, 3),
        }
        df = pd.DataFrame([log_row])
        header_needed = not os.path.isfile(LOG_FILE)
        df.to_csv(LOG_FILE, mode="a", index=False, header=header_needed)

elif page == \'Mood Tracker\':
    st.header(\'😊 Mood Tracker\')
    st.write(\'Upload a selfie to detect your mood:\')
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Save the uploaded file temporarily
        with open(os.path.join("temp_image.jpg"), "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.image(uploaded_file, caption=\'Uploaded Image.\', use_column_width=True)
        st.write("Detecting mood...")
        mood_result = detect_mood_from_image("temp_image.jpg")
        
        if "error" in mood_result:
            st.error(f"Error detecting mood: {mood_result[\"error\"]}")
        else:
            st.write("Detected Emotions:")
            for emotion, score in mood_result.items():
                st.write(f"- {emotion}: {score:.2f}%")
            # You can add logic here to update mood logs in TiDB

elif page == \'Journal\':
    st.header(\'✍️ Daily Journal\')
    st.write(\'Journaling functionality coming soon!\')

elif page == \'Settings\':
    st.header(\'⚙️ Settings\')
    st.write(\'Settings functionality coming soon!\')



