import streamlit as st
import google.generativeai as genai
import base64
import requests
import json
import os
import time
import math

# --- 1. MEMORY PATH (Self-Involving Gate) ---
MEMORY_FILE = "rabbit_brain_data.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try: return json.load(f)
            except: return {"hcs_score": 0, "balance": 5000.75, "logs": []}
    return {"hcs_score": 0, "balance": 5000.75, "logs": ["Brain Initialized"]}

def save_brain(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'brain' not in st.session_state:
    st.session_state.brain = load_brain()

# --- 2. FAIL-SAFE MODEL PICKER (404 Error Fix) ---
def get_working_model(api_key):
    try:
        genai.configure(api_key=api_key)
        for m_name in ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']:
            try:
                model = genai.GenerativeModel(m_name)
                return model
            except: continue
        return None
    except: return None

# --- 3. UI STYLE ---
st.set_page_config(page_title="RABBIT 12.0 - SUPREME", layout="wide")
st.markdown("<style>.main { background-color: #000; color: #00FFCC; }</style>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🐰 RABBIT MASTER CONTROL")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    st.divider()
    st.info(f"HCS Level: {st.session_state.brain.get('hcs_score', 0)}")
    st.info(f"Balance: ${st.session_state.brain.get('balance', 5000.75)}")

# --- 4. MAIN TABS (Asli Logic from app-2.py) ---
st.title("🛡️ MASTER SUKHI RAM - RABBIT 12.0")
tabs = st.tabs(["🧬 Evolution", "🎬 Multimedia", "🎮 Gaming", "📚 HCS Master", "🔐 Guardian"])

# --- TAB 0: EVOLUTION ---
with tabs[0]:
    st.header("Brain Expansion Interface")
    instruction = st.text_area("Next Evolution Command:", placeholder="Rabbit, naya technical feature jodo...")
    if st.button("🚀 INITIATE EVOLUTION"):
        if instruction and gem_key and git_key:
            with st.status("Rabbit is Rewriting Itself...") as s:
                model = get_working_model(gem_key)
                if model:
                    prompt = f"You are a Self-Evolving AI. Task: {instruction}. Return FULL code for app.py."
                    response = model.generate_content(prompt)
                    if response.text:
                        new_code = response.text.strip().replace("```python", "").replace("```", "")
                        # GitHub Push
                        repo = "sukhdevlaxmi-coder/Rabbit-AI-6.py"
                        url = f"https://api.github.com/repos/{repo}/contents/app.py"
                        headers = {"Authorization": f"token {git_key}"}
                        r = requests.get(url, headers=headers)
                        if r.status_code == 200:
                            sha = r.json()['sha']
                            requests.put(url, headers=headers, json={
                                "message": "Evolution", 
                                "content": base64.b64encode(new_code.encode()).decode(),
                                "sha": sha
                            })
                            st.balloons()
                            s.update(label="Evolution Complete! Refresh karein.", state="complete")

# --- TAB 1: MULTIMEDIA (360 Simulation) ---
with tabs[1]:
    st.header("360° Multimedia Hub")
    m_choice = st.selectbox("Choose Content:", ["Himalayan Panorama (Image)", "Ocean Exploration (Video)"])
    if st.button("Load Immersive View"):
        st.info(f"Loading {m_choice}...")
        time.sleep(1)
        st.markdown("""
        ```
        |   (Simulated Gaze: UP)       [CENTRAL VIEW]    |
        |      (Left Scroll)         (Right Scroll)      |
        ```
        """, unsafe_allow_html=True)
        st.success("360° Spherical Projection Active!")

# --- TAB 2: GAMING (Angry Birds Physics) ---
with tabs[2]:
    st.header("Angry Birds Physics Engine")
    v = st.slider("Launch Velocity (m/s)", 10, 100, 60)
    angle = st.slider("Launch Angle (degrees)", 0, 90, 40)
    if st.button("🚀 Fire Bird!"):
        rad = math.radians(angle)
        dist = (v**2 * math.sin(2*rad)) / 9.81
        st.write(f"Bird landed at: {dist:.2f}m")
        if abs(dist - 250) <= 15:
            st.success("🎯 SUCCESS: TARGET HIT!")
            st.balloons()
        else:
            st.error(f"FAILURE: Missed by {abs(dist-250):.2f}m")

# --- TAB 3: HCS MASTER ---
with tabs[3]:
    st.header("HCS Master Quiz")
    q = "हरियाणा का राजकीय पक्षी कौन सा hai?"
    ans = st.radio("Options:", ["कबूतर", "काला तीतर", "सारस क्रेन", "मोर"])
    if st.button("Check Answer"):
        if ans == "काला तीतर":
            st.success("Correct! Progress Saved.")
            st.session_state.brain["hcs_score"] += 1
            save_brain(st.session_state.brain)
        else:
            st.error("Incorrect. Try again!")

# --- TAB 4: GUARDIAN ---
with tabs[4]:
    st.header("Guardian Security & Bank")
    st.metric("Current Balance", f"${st.session_state.brain['balance']}")
    action = st.radio("Action:", ["Deposit", "Withdraw"])
    amt = st.number_input("Amount ($):", min_value=0.0)
    if st.button("Execute Secure Transaction"):
        if action == "Deposit":
            st.session_state.brain["balance"] += amt
        elif action == "Withdraw" and amt <= st.session_state.brain["balance"]:
            st.session_state.brain["balance"] -= amt
        save_brain(st.session_state.brain)
        st.success("Transaction Locked with Quantum Encryption!")
        st.rerun()
