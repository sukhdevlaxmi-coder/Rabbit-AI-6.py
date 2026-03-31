import streamlit as st
import google.generativeai as genai
import base64
import requests
import json
import os
import cv2
import numpy as np
from PIL import Image

# --- 1. MEMORY GATE (Local Laptop Brain) ---
MEMORY_FILE = "rabbit_brain_data.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try: return json.load(f)
            except: return {"history": [], "version": "12.0"}
    return {"history": ["Neural Core Active"], "version": "12.0"}

def save_brain(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'brain' not in st.session_state:
    st.session_state.brain = load_brain()

# --- 2. UNIVERSAL MODEL PICKER (No More 404) ---
def get_rabbit_brain(api_key):
    try:
        genai.configure(api_key=api_key)
        # Stable models ki list check karega
        for m_name in ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']:
            try:
                model = genai.GenerativeModel(m_name)
                return model
            except: continue
        return None
    except: return None

# --- 3. UI STYLE ---
st.set_page_config(page_title="RABBIT 12.0 - NEURAL", layout="wide")
st.markdown("<style>.main { background-color: #050505; color: #00FFCC; }</style>", unsafe_allow_html=True)

st.title("🛡️ SUPREME COMMANDER - RABBIT 12.0")

with st.sidebar:
    st.header("⚙️ MASTER KEYS")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    st.divider()
    if st.button("💾 Sync Laptop Memory"):
        save_brain(st.session_state.brain)
        st.success("Memory Locked!")

# --- 4. CORE MODULES ---
tabs = st.tabs(["🧬 Self-Evolution", "🎬 3D/360 Multimedia", "🧠 System Logs"])

with tabs[0]:
    st.header("Neural Evolution Engine")
    cmd = st.text_area("Order Rabbit (Hinglish):", placeholder="Rabbit, 3D render ko advance karo...")
    
    if st.button("🚀 INITIATE EVOLUTION"):
        if gem_key and git_key and cmd:
            with st.status("Rabbit is Evolving...") as s:
                model = get_rabbit_brain(gem_key)
                if model:
                    try:
                        # Rabbit ko batana ki wo sirf evolution aur media par focus kare
                        prompt = f"You are a Self-Evolving AI named Rabbit. Task: {cmd}. Focus on 3D/360 media and local memory. Return ONLY raw Python code for app.py. No HCS."
                        response = model.generate_content(prompt)
                        if response.text:
                            new_code = response.text.strip().replace("```python", "").replace("```", "")
                            # GitHub Push Logic
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
                                st.session_state.brain["history"].append(f"Evolved: {cmd[:15]}")
                                save_brain(st.session_state.brain)
                                st.balloons()
                                s.update(label="Evolution Complete! Refresh karein.", state="complete")
                    except Exception as e: st.error(f"Logic Error: {e}")
                else: st.error("Connection Failed. Check API Key.")

with tabs[1]:
    st.header("Technical Multimedia Suite")
    up = st.file_uploader("Upload Image", type=['jpg','png'])
    if up:
        img = Image.open(up)
        st.image(img, caption="Original", use_container_width=True)
        if st.button("🔥 Apply 3D Render"):
            img_np = np.array(img.convert('RGB'))
            shift = 15
            three_d = np.zeros_like(img_np)
            three_d[:, shift:, 0] = img_np[:, :-shift, 0] # Red Shift
            three_d[:, :-shift, 1:] = img_np[:, shift:, 1:] # Cyan Shift
            st.image(Image.fromarray(three_d), caption="3D Rendered Output")

with tabs[2]:
    st.header("Brain History")
    for log in reversed(st.session_state.brain.get("history", [])):
        st.caption(f"🧠 {log}")
