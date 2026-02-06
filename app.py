import streamlit as st
import openai
import csv
import os
import re
from datetime import datetime

# --- 1. CONFIGURATION ÉLITE ---
st.set_page_config(
    page_title="ORACLE", 
    page_icon="✨", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

# --- 2. GESTION DES DONNÉES (EMAILS & HISTORIQUE) ---
def harvest_email(email):
    """Enregistre l'email (sans doublon)"""
    file_path = 'database_oracle.csv'
    email = email.lower().strip()
    existing_emails = []
    if os.path.isfile(file_path):
        with open(file_path, mode='r') as f:
            reader = csv.reader(f)
            existing_emails = [row[0].lower() for row in reader if row]
    if email not in existing_emails:
        with open(file_path, mode='a', newline='') as f:
            writer = csv.writer(f)
            if os.stat(file_path).st_size == 0: writer.writerow(['Email', 'Date'])
            writer.writerow([email, datetime.now().strftime("%Y-%m-%d %H:%M")])

def log_conversation(email, role, message):
    """Archive chaque échange de façon permanente"""
    file_path = 'historique_oracle.csv'
    with open(file_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not os.path.isfile(file_path) or os.stat(file_path).st_size == 0:
            writer.writerow(['Date', 'Utilisateur', 'Role', 'Message'])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), email, role, message])

# --- 3. MÉMOIRE DE SESSION ---
if 'user_verified' not in st.session_state: st.session_state.user_verified = False
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.audace, st.session_state.clarte, st.session_state.autorite = 50, 50, 50

SCENARIOS = {
    "💼 Négociation Salaire": {"system": "Tu es un DRH froid.", "welcome": "Pourquoi vous augmenter ?"},
    "🌹 Premier Rendez-vous": {"system": "Tu es charismatique.", "welcome": "Bonsoir. Surprenez-moi."},
    "🔥 Gestion de Conflit": {"system": "Tu es un client furieux.", "welcome": "C'est inadmissible !"}
}

# --- 4. CSS SUPRÊME (FLÈCHE OR + FIX IPHONE) ---
def get_color(v):
    if v < 40: return "#FF4B4B"
    elif v < 75: return "#FFA500"
    else: return "#00FF87"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@700&display=swap');
    header[data-testid="stHeader"] {{ background: transparent !important; color: #C5A059 !important; }}
    #MainMenu, footer, [data-testid="stAppDeployButton"], .viewerBadge_container__1QSob {{ display: none !important; }}
    
    [data-testid="stSidebarCollapsedControl"] svg {{
        fill: #C5A059 !important;
        width: 45px !important; height: 45px !important;
        filter: drop-shadow(0 0 5px #C5A059);
    }}

    .stApp {{ background-color: #000000 !important; color: #FFFFFF !important; }}

    .main-title {{ 
        font-family: 'Cinzel', serif; font-size: 3.5rem; text-align: center; color: #C5A059; 
        margin-top: -30px; letter-spacing: 0.4em; white-space: nowrap !important;
    }}
    @media (max-width: 600px) {{ .main-title {{ font-size: 8vw !important; letter-spacing: 0.1em !important; margin-top: 10px !important; }} }}

    [data-testid="stSidebar"] {{ background-color: #080808 !important; border-right: 1px solid #C5A059 !important; min-width: 260px !important; }}
    .big-score {{ font-size: 3.5rem; font-weight: bold; color: #C5A059; text-align: center; font-family: 'Inter', sans-serif; }}
    .stButton > button {{ width: 100%; background: transparent !important; color: #C5A059 !important; border: 1px solid #C5A059 !important; font-family: 'Cinzel'; }}
    
    div[data-testid="stSidebar"] .stProgress:nth-of-type(1) div > div > div > div {{ background-color: {get_color(st.session_state.audace)} !important; }}
    div[data-testid="stSidebar"] .stProgress:nth-of-type(2) div > div > div > div {{ background-color: {get_color(st.session_state.clarte)} !important; }}
    div[data-testid="stSidebar"] .stProgress:nth-of-type(3) div > div > div > div {{ background-color: {get_color(st.session_state.autorite)} !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. SIDEBAR AVEC ADMIN EN BAS ---
with st.sidebar:
    st.markdown("<h1 style='color:#C5A059; text-align:center; font-family:Cinzel;'>ORACLE</h1>", unsafe_allow_html=True)
    if st.session_state.user_verified:
        choice = st.selectbox("DÉFI ACTUEL :", list(SCENARIOS.keys()))
        if "cur_scen" not in st.session_state or st.session_state.cur_scen != choice:
            st.session_state.cur_scen = choice
            st.session_state.messages = [{"role": "assistant", "content": SCENARIOS[choice]["welcome"]}]
            st.rerun()
        st.write("---")
        st.write(f"AUDACE: {st.session_state.audace}%"); st.progress(st.session_state.audace / 100)
        st.write(f"CLARTÉ: {st.session_state.clarte}%"); st.progress(st.session_state.clarte / 100)
        st.write(f"AUTORITÉ: {st.session_state.autorite}%"); st.progress(st.session_state.autorite / 100)
        total = int((st.session_state.audace + st.session_state.clarte + st.session_state.autorite) / 3)
        st.markdown(f'<div class="big-score">{total}%</div>', unsafe_allow_html=True)
        if st.button("QUITTER"): st.session_state.user_verified = False; st.rerun()
    else:
        st.warning("Accès verrouillé")

    # --- ADMIN TOUT EN BAS ---
    st.markdown("<div style='height: 150px;'></div>", unsafe_allow_html=True)
    with st.expander("⚙️ ADMINISTRATION"):
        if st.text_input("Code Secret", type="password") == "zzgsIKGnd29456FSQFZAR":
            st.subheader("Emails")
            if os.path.isfile('database_oracle.csv'):
                with open('database_oracle.csv', 'r') as f: st.text(f.read())
            st.subheader("Derniers messages")
            if os.path.isfile('historique_oracle.csv'):
                with open('historique_oracle.csv', 'r') as f: st.text(f.read()[-1000:])

# --- 6. ZONE PRINCIPALE ET ANALYSE ---
if not st.session_state.user_verified:
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">ORACLE</div>', unsafe_allow_html=True)
    st.markdown('<div style="max-width:400px; margin:auto; padding:2rem; border:1px solid #C5A059; border-radius:10px; background:#080808;">', unsafe_allow_html=True)
    email_in = st.text_input("Email", placeholder="votre@email.com")
    if st.button("ACCÉDER À L'ORACLE"):
        if "@" in email_in and "." in email_in:
            harvest_email(email_in)
            st.session_state.user_email = email_in
            st.session_state.user_verified = True; st.rerun()
        else: st.error("Email invalide.")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="main-title">ORACLE AI</div>', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        side = "right" if msg["role"] == "user" else "left"
        border = "border-right: 2px solid #C5A059" if msg["role"] == "user" else "border-left: 2px solid #444"
        st.markdown(f'<div style="text-align:{side}; {border}; padding:15px; margin-bottom:15px;">{msg["content"]}</div>', unsafe_allow_html=True)

    if p := st.chat_input("Exprimez votre intention..."):
        st.session_state.messages.append({"role": "user", "content": p})
        log_conversation(st.session_state.user_email, "USER", p) # ARCHIVAGE USER
        
        client = openai.OpenAI(api_key=st.secrets["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1")
        with st.spinner("Analyse..."):
            # 1. RÉPONSE
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":SCENARIOS[choice]["system"]}] + st.session_state.messages)
            ai_msg = res.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ai_msg})
            log_conversation(st.session_state.user_email, "AI", ai_msg) # ARCHIVAGE AI
            
            # 2. SCORES
            eval_res = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user", "content": f"Note a,c,au de '{p}': n,n,n"}])
            try:
                nums = re.findall(r'\d+', eval_res.choices[0].message.content)
                if len(nums) >= 3: st.session_state.audace, st.session_state.clarte, st.session_state.autorite = int(nums[0]), int(nums[1]), int(nums[2])
            except: pass
        st.rerun()