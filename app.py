import streamlit as st
import google.generativeai as genai
import base64
import requests
import json
import os
import cv2
import numpy as np
from PIL import Image

# --- 1. SMART MEMORY (Laptop Storage) ---
MEMORY_FILE = "rabbit_brain_data.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try: 
                data = json.load(f)
                return data
            except: return {"version": "12.0", "history": [], "balance": 5000}
    return {"version": "12.0", "history": ["System Live"], "balance": 5000}

def save_brain(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'brain' not in st.session_state:
    st.session_state.brain = load_brain()

# --- 2. STABLE MODEL PICKER (Fixes 404/NotFound) ---
def get_working_model(api_key):
    try:
        genai.configure(api_key=api_key)
        # Seedha stable model call
        return genai.GenerativeModel('gemini-1.5-flash')
    except: return None

# --- 3. UI STYLE ---
st.set_page_config(page_title="RABBIT 12.0 - SUPER CODER", layout="wide")
st.markdown("<style>.main { background-color: #000; color: #FFD700; }</style>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🐰 RABBIT MASTER CONSOLE")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    st.divider()
    
    # SAFETY FIX: Using .get() to prevent 'version' error
    current_ver = st.session_state.brain.get('version', '12.0')
    st.write(f"System Version: **{current_ver}**")
    
    if st.button("💾 Sync to Laptop Memory"):
        save_brain(st.session_state.brain)
        st.success("Memory Locked!")

# --- 4. MAIN INTERFACE ---
st.title("🛡️ SUPREME CODER - RABBIT 12.0")
tabs = st.tabs(["🧬 Evolution Engine", "🎬 3D/360 Media Lab", "🧠 Neural Logs"])

# TAB 0: EVOLUTION
with tabs[0]:
    st.header("Neural Expansion & Auto-Coding")
    instruction = st.text_area("Order Rabbit (Hinglish):", placeholder="Rabbit, 3D photo effects ko aur advance karo...")
    
    if st.button("🚀 EXECUTE EVOLUTION"):
        if instruction and gem_key and git_key:
            with st.status("Rabbit is Rewriting Neural Pathways...") as s:
                model = get_working_model(gem_key)
                if model:
                    try:
                        # Rabbit ko "Best Coder" banane wala prompt
                        prompt = f"You are a Supreme Coder. Task: {instruction}. Rewrite app.py to include this. Use local memory logic. Return ONLY raw Python code."
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
                                st.session_state.brain["history"].append(f"Evolved: {instruction[:15]}")
                                save_brain(st.session_state.brain)
                                st.balloons()
                                s.update(label="Evolution Complete! Refresh in 1 min.", state="complete")
                    except Exception as e: st.error(f"Logic Error: {e}")

# TAB 1: MULTIMEDIA (3D Rendering)
with tabs[1]:
    st.header("Technical Multimedia Processor")
    up = st.file_uploader("Upload Image", type=['jpg','png','jpeg'])
    if up:
        img = Image.open(up)
        st.image(img, caption="Original", use_container_width=True)
        if st.button("🔥 Render 3D Depth Map"):
            img_np = np.array(img.convert('RGB'))
            shift = 15
            three_d = np.zeros_like(img_np)
            three_d[:, shift:, 0] = img_np[:, :-shift, 0] 
            three_d[:, :-shift, 1:] = img_np[:, shift:, 1:] 
            st.image(Image.fromarray(three_d), caption="3D Technical Render")

with tabs[2]:
    st.header("System Brain History")
    for log in reversed(st.session_state.brain.get('history', [])):
        st.caption(f"🧠 {log}")
