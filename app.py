import streamlit as st
import google.generativeai as genai
import base64
import requests
import json
import os
import time
import cv2
import numpy as np
from PIL import Image

# --- 1. NEURAL MEMORY GATE (Jo Rabbit kabhi nahi bhulega) ---
MEMORY_FILE = "rabbit_brain_data.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try: return json.load(f)
            except: return {"history": [], "balance": 5000, "version": "12.0"}
    return {"history": ["Brain Core Initialized"], "balance": 5000, "version": "12.0"}

def save_brain(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'brain' not in st.session_state:
    st.session_state.brain = load_brain()

# --- 2. FAIL-SAFE MODEL PICKER (NotFound Error Solution) ---
def get_stable_model(api_key):
    try:
        genai.configure(api_key=api_key)
        # 404 Fix: Sabse stable rasta call karein
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        return None

# --- 3. UI STYLE & CONFIG ---
st.set_page_config(page_title="RABBIT 12.0 - NEURAL CORE", layout="wide")
st.markdown("<style>.main { background-color: #000; color: #00FFCC; }</style>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🐰 RABBIT MASTER CONTROL")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    st.divider()
    st.subheader("⚙️ System Status")
    st.info(f"Neural Version: {st.session_state.brain.get('version')}")
    st.info(f"Guardian Funds: ${st.session_state.brain.get('balance')}")

# --- 4. GITHUB AUTO-PUSH ENGINE ---
def push_to_github(new_code):
    repo = "sukhdevlaxmi-coder/Rabbit-AI-6.py"
    url = f"https://api.github.com/repos/{repo}/contents/app.py"
    headers = {"Authorization": f"token {git_key}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        sha = r.json()['sha']
        requests.put(url, headers=headers, json={
            "message": "Self-Evolution Update",
            "content": base64.b64encode(new_code.encode()).decode(),
            "sha": sha
        })
        return True
    return False

# --- 5. MASTER INTERFACE (Evolution & Multimedia Focus) ---
st.title("🛡️ SUPREME COMMANDER - RABBIT 12.0")
tabs = st.tabs(["🧬 Neural Evolution", "🎬 Multimedia 3D/360", "🔐 Guardian & Brain"])

# TAB 0: EVOLUTION (The Thinking Part)
with tabs[0]:
    st.header("Brain Expansion & Self-Learning")
    st.write("Sukhi Ram ji, Rabbit ko naye 'Technical Concepts' sikhaiye.")
    instruction = st.text_area("Next Evolution Command:", placeholder="Rabbit, 3D photo editor ko aur technical banao...")
    
    if st.button("🚀 INITIATE EVOLUTION"):
        if instruction and gem_key and git_key:
            with st.status("Rabbit is Thinking & Rewriting Neural Pathways...") as s:
                model = get_stable_model(gem_key)
                if model:
                    prompt = f"You are a Self-Evolving AI. Task: {instruction}. Return ONLY raw Python code for app.py. No HCS or exam content."
                    response = model.generate_content(prompt)
                    if response.text:
                        clean_code = response.text.strip().replace("```python", "").replace("```", "")
                        if push_to_github(clean_code):
                            st.balloons()
                            st.session_state.brain["history"].append(f"Evolved: {instruction[:20]}")
                            save_brain(st.session_state.brain)
                            s.update(label="Evolution Successful! Refresh in 1 min.", state="complete")

# TAB 1: MULTIMEDIA (Advanced 3D/360)
with tabs[1]:
    st.header("Technical 3D & 360° Media Processor")
    up = st.file_uploader("Upload Image for AI Processing", type=['jpg','png','jpeg'])
    
    if up:
        img = Image.open(up)
        st.image(img, caption="Original View", use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔥 Generate 3D Depth Map"):
                # Technical Depth Logic
                img_np = np.array(img.convert('RGB'))
                shift = 15
                three_d = np.zeros_like(img_np)
                three_d[:, shift:, 0] = img_np[:, :-shift, 0] # Red Shift
                three_d[:, :-shift, 1:] = img_np[:, shift:, 1:] # Cyan Shift
                st.image(Image.fromarray(three_d), caption="3D Technical Render")
        with col2:
            if st.button("🔄 Project 360° Sphere"):
                st.info("Spherical Mapping Active...")
                st.code(" [Visualizer: Panoramic 360 Console Active] ")

# TAB 2: GUARDIAN & MEMORY
with tabs[2]:
    st.header("Brain Memory & Security")
    st.metric("Secured Family Funds", f"${st.session_state.brain['balance']}")
    
    st.subheader("Neural Logs")
    for log in reversed(st.session_state.brain.get("history", [])[-5:]):
        st.caption(f"🧠 {log}")
    
    if st.button("Lock Memory & Save"):
        save_brain(st.session_state.brain)
        st.success("Memory Locked Successfully!")
