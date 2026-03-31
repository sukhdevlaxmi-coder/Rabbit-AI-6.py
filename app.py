import streamlit as st
import google.generativeai as genai
import base64
import requests
import json
import os
import cv2
import numpy as np
from PIL import Image

# --- 1. MEMORY GATE (Laptop/Local Storage) ---
MEMORY_FILE = "rabbit_brain_data.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try: return json.load(f)
            except: return {"history": [], "version": "12.0"}
    return {"history": ["Brain Initialized"], "version": "12.0"}

def save_brain(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'brain' not in st.session_state:
    st.session_state.brain = load_brain()

# --- 2. CONNECTION FIX (Model Picker) ---
def get_working_model(api_key):
    try:
        genai.configure(api_key=api_key)
        # 404/NotFound Error Fix: Direct stable model call
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception:
        return None

# --- 3. UI STYLE & CONFIG ---
st.set_page_config(page_title="RABBIT 12.0 - NEURAL", layout="wide")
st.markdown("<style>.main { background-color: #050505; color: #00FFCC; }</style>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🐰 RABBIT MASTER")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    st.divider()
    st.write(f"Neural Status: **Online**")
    if st.button("💾 Save to Laptop Memory"):
        save_brain(st.session_state.brain)
        st.success("Memory Locked!")

# --- 4. MAIN MODULES ---
st.title("🛡️ SUPREME COMMANDER - RABBIT 12.0")
tabs = st.tabs(["🧬 Self-Evolution", "🎬 Multimedia 3D/360", "🧠 Brain Logs"])

with tabs[0]:
    st.header("Neural Evolution Engine")
    cmd = st.text_area("Order Rabbit to Evolve (Hinglish):", placeholder="Rabbit, mera video editing module advance karo...")
    
    if st.button("🚀 INITIATE EVOLUTION"):
        if gem_key and git_key and cmd:
            with st.status("Rabbit is Rewriting Itself...") as s:
                model = get_working_model(gem_key)
                if model:
                    try:
                        prompt = f"You are a Self-Evolving AI. Task: {cmd}. Return ONLY raw Python code for app.py. No HCS or exams."
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
                                    "message": "Evolution Update",
                                    "content": base64.b64encode(new_code.encode()).decode(),
                                    "sha": sha
                                })
                                st.session_state.brain["history"].append(f"Evolved: {cmd[:20]}")
                                save_brain(st.session_state.brain)
                                st.balloons()
                                s.update(label="Evolution Complete! Refresh karein.", state="complete")
                    except Exception as e: st.error(f"Logic Error: {e}")
                else: st.error("Model Connection Failed. API Key check karein.")

with tabs[1]:
    st.header("3D & 360° Media Processor")
    up = st.file_uploader("Upload Image", type=['jpg','png','jpeg'])
    if up:
        img = Image.open(up)
        st.image(img, caption="Original", use_container_width=True)
        if st.button("🔥 Apply Technical 3D Render"):
            # Real Pixel Depth Logic
            img_np = np.array(img.convert('RGB'))
            shift = 15
            three_d = np.zeros_like(img_np)
            three_d[:, shift:, 0] = img_np[:, :-shift, 0] # Red layer shift
            three_d[:, :-shift, 1:] = img_np[:, shift:, 1:] # Cyan layer shift
            st.image(Image.fromarray(three_d), caption="3D Rendered", use_container_width=True)

with tabs[2]:
    st.header("System Brain History")
    for log in reversed(st.session_state.brain.get("history", [])):
        st.caption(f"🧠 {log}")
