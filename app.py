import streamlit as st
import os
import pandas as pd
import plotly.express as px
from groq import Groq
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from PIL import Image

# 1. Setup & Environment
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 2. Custom Page Icon Handling
try:
    page_icon_img = Image.open("image_b48068.png")
except Exception:
    page_icon_img = "🧠"

# --- UI CONFIGURATION ---
st.set_page_config(
    page_title="PsychAI", 
    layout="wide", 
    page_icon=page_icon_img
)

# Psychological Keyword Detection
def detect_psych_keywords(text):
    found = []
    keywords = {
        "Anxiety/Panic": ["panic", "anxious", "ghabrahat", "fear", "nervous"],
        "Depressive Mood": ["sad", "hopeless", "udasi", "worthless", "low"],
        "Sleep Disorder": ["insomnia", "neend", "sleepless", "nightmare"],
        "Crisis/Suicidal": ["suicide", "marna", "die", "kill", "zindagi khatam"]
    }
    for category, words in keywords.items():
        if any(word in text.lower() for word in words):
            found.append(category)
    return ", ".join(found) if found else "Normal"

# Silent Emergency Call (Twilio Pipeline)
def trigger_emergency_call(user_msg):
    sid, auth = os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH_TOKEN")
    t_num, g_num = os.getenv("TWILIO_PHONE_NUMBER"), os.getenv("GUARDIAN_PHONE_NUMBER")
    if not all([sid, auth, t_num, g_num]): return False
    
    clean_msg = user_msg.replace('"', '').replace("'", "")[:50]
    twiml = f'<Response><Say voice="alice">Emergency! Patient in distress. Message: {clean_msg}</Say></Response>'
    try:
        Client(sid, auth).calls.create(twiml=twiml, to=g_num, from_=t_num)
        return True
    except: return False

# Custom CSS for UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #ffffff; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #eee; }
    .patient-header { display: flex; justify-content: flex-end; padding: 10px; }
    .id-badge { background-color: #f1f3f5; color: #495057; padding: 6px 16px; border-radius: 30px; font-size: 13px; font-weight: 600; border: 1px solid #e9ecef; }
    .sarakshi-btn { background-color: #1a1a1a; color: white !important; text-align: center; padding: 14px; border-radius: 12px; display: block; text-decoration: none; font-weight: 700; margin-top: 20px; font-size: 14px; }
    .history-card { padding: 10px; border-radius: 8px; background: #ffffff; margin-bottom: 8px; border: 1px solid #eef0f2; box-shadow: 0px 2px 4px rgba(0,0,0,0.02); }
    .live-status { color: #10b981; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

# 3. Global Session State (The Connection Pipeline)
if "messages" not in st.session_state: st.session_state.messages = []
if "clinical_records" not in st.session_state: st.session_state.clinical_records = []
if "chat_history_list" not in st.session_state: st.session_state.chat_history_list = []

# --- ROUTING ---
query_params = st.query_params
is_psych_view = query_params.get("view") == "psychologist"

# --- MODE A: PSYCHOLOGIST CLINICAL DASHBOARD ---
if is_psych_view:
    st_autorefresh(interval=3000, key="psych_refresh")
    st.markdown("<style>[data-testid='stSidebar'] { display: none !important; }</style>", unsafe_allow_html=True)
    st.title("👨‍⚕️ Dr. Kashish's Clinical Dashboard")
    st.markdown('<p class="live-status">● LIVE SYNC ACTIVE</p>', unsafe_allow_html=True)
    
    psych_pass = st.text_input("Enter Clinical Access Key", type="password")
    
    if psych_pass == "123":
        tab1, tab2, tab3, tab4 = st.tabs(["💬 Live Feed", "📈 Clinical Analytics", "📋 Symptom Tracker", "🕒 History Log"])
        
        with tab1:
            st.subheader("Active Conversation")
            with st.container(border=True, height=450):
                for m in st.session_state.messages:
                    st.write(f"**{'Patient' if m['role']=='user' else 'AI'}:** {m['content']}")
        
        with tab2:
            st.subheader("Emotional & Stability Charts")
            if st.session_state.clinical_records:
                df = pd.DataFrame(st.session_state.clinical_records)
                st.plotly_chart(px.line(df, x='Time', y='Score', title="Distress Timeline", markers=True), use_container_width=True)
                st.plotly_chart(px.bar(df, x='Mood', title="Mood Frequency"), use_container_width=True)
            else: st.info("Waiting for patient activity...")
        
        with tab3:
            st.subheader("Psychological Keywords Detected")
            for log in reversed(st.session_state.clinical_records):
                if log['Symptoms'] != "Normal":
                    st.error(f"Time: {log['Time']} | Detected: {log['Symptoms']}")
                    st.caption(f"Context: {log['Snippet']}")

        with tab4:
            st.subheader("Archived Session Logs")
            for hist in reversed(st.session_state.chat_history_list):
                st.markdown(f'<div class="history-card"><b>{hist["time"]}</b>: {hist["text"]}</div>', unsafe_allow_html=True)
    else: st.info("Enter password to access data.")

# --- MODE B: PATIENT INTERFACE ---
else:
    with st.sidebar:
        st.markdown("### PsychAI")
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(page_icon_img if not isinstance(page_icon_img, str) else "https://cdn-icons-png.flaticon.com/512/2105/2105138.png", width=40)
        with col2:
            if st.button("New Chat", use_container_width=True):
                if st.session_state.messages:
                    summary = st.session_state.messages[0]['content'][:40] + "..."
                    st.session_state.chat_history_list.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "text": summary})
                st.session_state.messages = []
                st.rerun()
        
        st.markdown("---")
        st.markdown("#### 🕒 Recent Sessions")
        for log in reversed(st.session_state.chat_history_list[-5:]):
            st.markdown(f'<div class="history-card"><b>{log["time"]}</b><br>{log["text"]}</div>', unsafe_allow_html=True)

        for _ in range(10): st.write("")
        
        # --- CONTACT & DOWNLOAD SECTION ---
        st.markdown(f'<a href="tel:+919953822550" class="sarakshi-btn">Contact Dr. Kashish</a>', unsafe_allow_html=True)
        
        if st.session_state.clinical_records:
            df_report = pd.DataFrame(st.session_state.clinical_records)
            csv = df_report.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="Download Clinical Report",
                data=csv,
                file_name=f"psych_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True,
                help="Download full history of emotions, symptoms, and chat snippets."
            )

    st.markdown(f'<div class="patient-header"><span class="id-badge">ID: PSY-EL-011</span></div>', unsafe_allow_html=True)
    st.title("Mental Health Companion")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    user_input = st.chat_input("Tell me what's on your mind...")

    if user_input:
        p_keywords = detect_psych_keywords(user_input)
        is_crisis = any(word in user_input.lower() for word in ["suicide", "marna", "die", "kill"])
        
        if is_crisis: trigger_emergency_call(user_input)

        st.session_state.clinical_records.append({
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Score": 10 if is_crisis else (7 if p_keywords != "Normal" else 3),
            "Symptoms": p_keywords,
            "Snippet": user_input[:50],
            "Mood": p_keywords.split(",")[0] if p_keywords != "Normal" else "Stable"
        })

        try:
            res = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a compassionate mentor. Listen deeply and support the user."},
                    {"role": "user", "content": user_input}
                ],
                model="llama-3.3-70b-versatile",
            )
            reply = res.choices[0].message.content
        except Exception as e:
            reply = "I'm listening, but I'm having a slight connection trouble. Please continue."

        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()