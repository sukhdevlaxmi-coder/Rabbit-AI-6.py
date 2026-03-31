import streamlit as st
import google.generativeai as genai
import base64
import requests
import json
import os
import math
import time

# --- 1. BRAIN & MEMORY (Laptop Sync) ---
MEMORY_FILE = "rabbit_brain_data.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try: 
                data = json.load(f)
                return data
            except: return {"version": "12.0", "hcs_score": 0, "balance": 5000.75, "logs": []}
    return {"version": "12.0", "hcs_score": 0, "balance": 5000.75, "logs": ["Brain Initialized"]}

def save_brain(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'brain' not in st.session_state:
    st.session_state.brain = load_brain()

# --- 2. GITHUB PUSH ENGINE (Fixed Repo Name) ---
def push_to_github(new_code, git_token):
    repo = "sukhdevlaxmi-coder/Rabbit-AI-6.py" # Verified: A + chota 'l'
    url = f"https://api.github.com/repos/{repo}/contents/app.py"
    headers = {"Authorization": f"token {git_token}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        sha = r.json()['sha']
        res = requests.put(url, headers=headers, json={
            "message": "Neural Evolution Update",
            "content": base64.b64encode(new_code.encode()).decode(),
            "sha": sha
        })
        return res.status_code
    return r.status_code

# --- 3. UI STYLE & SIDEBAR ---
st.set_page_config(page_title="RABBIT 12.0 SUPER CODER", layout="wide")
st.markdown("<style>.main { background-color: #000; color: #00FFCC; }</style>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🐰 RABBIT MASTER CONSOLE")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    st.divider()
    st.write(f"System Version: **{st.session_state.brain.get('version', '12.0')}**")
    if st.button("💾 Sync to Laptop Memory"):
        save_brain(st.session_state.brain)
        st.success("Memory Locked!")

# --- 4. MAIN INTERFACE TABS ---
st.title("🛡️ SUPREME CODER - RABBIT 12.0")
tabs = st.tabs(["🧬 Evolution Engine", "🎬 Multimedia", "🎮 Gaming", "🔐 Guardian"])

# TAB 0: EVOLUTION (Thinking/Rewriting Fix)
with tabs[0]:
    st.header("Neural Expansion & Auto-Coding")
    instruction = st.text_area("Next Evolution Command (Hinglish):")
    if st.button("🚀 EXECUTE EVOLUTION"):
        if instruction and gem_key and git_key:
            with st.status("Rabbit is Thinking & Rewriting Itself...") as s:
                genai.configure(api_key=gem_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"Task: {instruction}. Return ONLY raw Python code for this Streamlit app."
                response = model.generate_content(prompt)
                if response.text:
                    new_code = response.text.strip().replace("```python", "").replace("```", "")
                    status = push_to_github(new_code, git_key)
                    if status in [200, 201]:
                        st.balloons()
                        s.update(label="Evolution Complete! Refresh Now.", state="complete")

# TAB 1: MULTIMEDIA (Asli Logic from app-2.py)
with tabs[1]:
    st.header("360° Media Processor")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Load 360 Panoramic View"):
            st.info("Rendering Spherical Projection...")
            st.code("| [UP] | [CENTER] | [DOWN] |")
    with col2:
        st.file_uploader("Upload Image/Video", type=['jpg','mp4'])

# TAB 2: GAMING (Angry Birds Physics from app-2.py)
with tabs[2]:
    st.header("Physics Simulation: Angry Birds")
    v = st.slider("Velocity (m/s)", 10, 100, 60)
    a = st.slider("Angle", 0, 90, 45)
    if st.button("🚀 Launch Bird"):
        dist = (v**2 * math.sin(math.radians(2*a))) / 9.81
        st.write(f"Bird landed at: {dist:.2f} meters")
        if abs(dist - 250) <= 15: st.success("🎯 TARGET HIT!")

# TAB 3: GUARDIAN (Security from app-2.py)
with tabs[3]:
    st.header("Guardian Bank & Security")
    st.metric("Secured Balance", f"${st.session_state.brain['balance']}")
    if st.button("Simulate Face Recognition Scan"):
        with st.spinner("Scanning..."):
            time.sleep(2)
            st.success("Authorized: Sukhi Ram (Alpha-007)")
