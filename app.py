import streamlit as st
import google.generativeai as genai
import base64
import requests
import json
import os
import cv2
import numpy as np
from PIL import Image

# --- 1. NEURAL MEMORY (Laptop Storage) ---
MEMORY_FILE = "rabbit_brain_data.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try: return json.load(f)
            except: return {"version": "12.0", "history": [], "dev_mode": True}
    return {"version": "12.0", "history": ["System Live"], "dev_mode": True}

def save_brain(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'brain' not in st.session_state:
    st.session_state.brain = load_brain()

# --- 2. FAIL-SAFE MODEL PICKER (404 Error Fix) ---
def get_working_model(api_key):
    try:
        genai.configure(api_key=api_key)
        # 404 Fix: Stable model call
        return genai.GenerativeModel('gemini-1.5-flash')
    except: return None

# --- 3. UI STYLE & CONFIG ---
st.set_page_config(page_title="RABBIT 12.0 - CODER", layout="wide")
st.markdown("<style>.main { background-color: #000; color: #FFD700; }</style>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🐰 RABBIT MASTER CONSOLE")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    st.divider()
    st.write(f"System Version: {st.session_state.brain['version']}")
    if st.button("💾 Sync to Laptop Memory"):
        save_brain(st.session_state.brain)
        st.success("Memory Locked!")

# --- 4. MAIN INTERFACE ---
st.title("🛡️ SUPREME CODER - RABBIT 12.0")
tabs = st.tabs(["🧬 Self-Evolution Engine", "🎬 3D/360 Media Lab", "🧠 Neural Logs"])

# TAB 0: EVOLUTION (The Coding Brain)
with tabs[0]:
    st.header("Neural Expansion & Auto-Coding")
    instruction = st.text_area("Next Evolution Command (Hinglish):", placeholder="Rabbit, ek naya tab banao jisme meri family photos ka 3D album ho...")
    
    if st.button("🚀 EXECUTE EVOLUTION"):
        if instruction and gem_key and git_key:
            with st.status("Rabbit is Thinking & Rewriting Neural Pathways...") as s:
                model = get_working_model(gem_key)
                if model:
                    try:
                        # Rabbit ko "Best Coder" banane wala prompt
                        prompt = f"You are Rabbit AI, a Supreme Coder. Task: {instruction}. Rewrite the entire app.py to include this. Use high-end libraries. No HCS/Exams. Return ONLY raw Python code."
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
                                encoded = base64.b64encode(new_code.encode()).decode()
                                requests.put(url, headers=headers, json={"message": "Evolution", "content": encoded, "sha": sha})
                                st.session_state.brain["history"].append(f"Evolved: {instruction[:20]}")
                                save_brain(st.session_state.brain)
                                st.balloons()
                                s.update(label="Evolution Complete! Refresh in 1 min.", state="complete")
                    except Exception as e: st.error(f"Logic Error: {e}")

# TAB 1: MULTIMEDIA (360/3D Asli Logic)
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
            three_d[:, shift:, 0] = img_np[:, :-shift, 0] # Red Shift
            three_d[:, :-shift, 1:] = img_np[:, shift:, 1:] # Cyan Shift
            st.image(Image.fromarray(three_d), caption="3D Technical Render")

with tabs[2]:
    st.header("System Brain History")
    for log in reversed(st.session_state.brain.get("history", [])):
        st.caption(f"🧠 {log}")
