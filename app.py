import streamlit as st
import google.generativeai as genai
import base64
import requests
import json
import os
import math
import time

# --- 1. MEMORY & BRAIN INITIALIZATION ---
MEMORY_FILE = "rabbit_brain_data.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try: return json.load(f)
            except: return {"hcs_score": 0, "balance": 5000.75, "history": []}
    return {"hcs_score": 0, "balance": 5000.75, "history": ["Brain Initialized"]}

def save_brain(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'brain' not in st.session_state:
    st.session_state.brain = load_brain()

# --- 2. THE ULTIMATE MODEL FIX (No More 404 Error) ---
def get_stable_model(api_key):
    try:
        genai.configure(api_key=api_key)
        # 404 Fix: Sabse stable rasta
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        return None

# --- 3. UI STYLE CONFIG ---
st.set_page_config(page_title="RABBIT 12.0 - SUPREME", layout="wide")
st.markdown("<style>.main { background-color: #000; color: #00FFCC; }</style>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🐰 MASTER CONTROL")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    st.divider()
    st.info(f"HCS Level: {st.session_state.brain.get('hcs_score', 0)}")
    st.info(f"Funds: ${st.session_state.brain.get('balance', 5000.75)}")

# --- 4. MAIN INTERFACE (Your Real Logic) ---
st.title("🛡️ MASTER SUKHI RAM - RABBIT 12.0")
tabs = st.tabs(["🧬 Self-Evolve", "🎬 Multimedia", "🎮 Gaming", "📚 HCS Master", "🔐 Guardian"])

# TAB 0: EVOLUTION
with tabs[0]:
    st.header("Neural Evolution Engine")
    instruction = st.text_area("Order Rabbit (Hinglish):", placeholder="Rabbit, naya tab banao...")
    if st.button("🚀 INITIATE EVOLUTION"):
        if instruction and gem_key and git_key:
            with st.status("Rabbit is Rewriting Itself...") as s:
                model = get_stable_model(gem_key)
                if model:
                    try:
                        prompt = f"You are Rabbit AI. Task: {instruction}. Return FULL code for app.py. No markdown."
                        response = model.generate_content(prompt)
                        if response.text:
                            new_code = response.text.strip().replace("```python", "").replace("```", "")
                            # GitHub Push
                            repo = "sukhdevlaxmi-coder/Rabbit-Al-6.py"
                            url = f"https://api.github.com/repos/{repo}/contents/app.py"
                            headers = {"Authorization": f"token {git_key}"}
                            r = requests.get(url, headers=headers)
                            if r.status_code == 200:
                                sha = r.json()['sha']
                                requests.put(url, headers=headers, json={
                                    "message": "Evolution Update", 
                                    "content": base64.b64encode(new_code.encode()).decode(),
                                    "sha": sha
                                })
                                st.balloons()
                                s.update(label="Evolution Complete! Refresh in 1 min.", state="complete")
                    except Exception as e: st.error(f"Error: {e}")

# TAB 1: MULTIMEDIA (app-2.py logic)
with tabs[1]:
    st.header("360° Multimedia Hub")
    choice = st.selectbox("Load Content:", ["Himalayan 360 Image", "Deep Ocean 360 Video"])
    if st.button("Activate Immersive Mode"):
        st.info(f"Rendering {choice} in 360 environment...")
        st.code(" [Visualizer: Panoramic Console Output Active] ")

# TAB 2: GAMING (Angry Birds logic)
with tabs[2]:
    st.header("Angry Birds Physics Engine")
    v = st.slider("Launch Velocity (m/s)", 10, 100, 60)
    angle = st.slider("Launch Angle", 0, 90, 40)
    if st.button("🚀 Fire!"):
        dist = (v**2 * math.sin(math.radians(2*angle))) / 9.81
        st.write(f"Bird landed at: {dist:.2f}m")
        if abs(dist - 250) <= 15:
            st.success("🎯 TARGET HIT!")
            st.balloons()
        else: st.error("MISSED!")

# TAB 3: HCS MASTER
with tabs[3]:
    st.header("HCS Prep Hub")
    st.write(f"Current Knowledge Level: {st.session_state.brain['hcs_score']}")
    if st.button("Save Study Progress"):
        st.session_state.brain["hcs_score"] += 1
        save_brain(st.session_state.brain)
        st.rerun()

# TAB 4: GUARDIAN
with tabs[4]:
    st.header("Guardian Bank Security")
    st.metric("Secure Balance", f"${st.session_state.brain['balance']}")
    if st.button("Secure Deposit $100"):
        st.session_state.brain["balance"] += 100
        save_brain(st.session_state.brain)
        st.rerun()
