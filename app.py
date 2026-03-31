import streamlit as st
import google.generativeai as genai
import base64
import requests
import json
import os
import cv2
import numpy as np
from PIL import Image

# --- 1. NEURAL MEMORY (Laptop Storage Logic) ---
MEMORY_FILE = "rabbit_brain_data.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try: return json.load(f)
            except: return {"history": [], "version": "12.0", "settings": {}}
    return {"history": ["Brain Initialized"], "version": "12.0", "settings": {}}

def save_brain(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'brain' not in st.session_state:
    st.session_state.brain = load_brain()

# --- 2. SMART MODEL PICKER (404 Error Fix) ---
def get_working_model(api_key):
    try:
        genai.configure(api_key=api_key)
        for model_name in ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']:
            try:
                m = genai.GenerativeModel(model_name)
                m.generate_content("test") 
                return m
            except: continue
        return None
    except: return None

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="RABBIT 12.0 - NEURAL CORE", layout="wide")
st.markdown("<style>.main { background-color: #050505; color: #00FFCC; }</style>", unsafe_allow_html=True)

st.title("🛡️ SUPREME COMMANDER - RABBIT 12.0")

with st.sidebar:
    st.header("⚙️ MASTER KEYS")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    st.divider()
    st.write(f"Neural Version: {st.session_state.brain.get('version')}")
    if st.button("💾 Lock Memory"):
        save_brain(st.session_state.brain)
        st.success("Memory Saved to Laptop!")

# --- 4. TABS LOGIC ---
t1, t2, t3 = st.tabs(["🧬 Self-Evolution", "🎬 Multimedia 3D/360", "🧠 System Brain"])

with t1:
    st.header("Neural Expansion Interface")
    st.write("Rabbit ko evolve karne ke liye command dein.")
    cmd = st.text_area("Order Rabbit (Hinglish):", placeholder="Rabbit, 3D effects ko aur behtar banao...")
    if st.button("🚀 INITIATE EVOLUTION"):
        if gem_key and git_key and cmd:
            with st.status("Rabbit is Rewriting Neural Pathways...") as s:
                model = get_working_model(gem_key)
                if model:
                    try:
                        prompt = f"You are a Self-Evolving AI. Task: {cmd}. Return ONLY raw Python code for app.py. No HCS or exam matter."
                        response = model.generate_content(prompt)
                        if response.text:
                            new_code = response.text.strip().replace("```python", "").replace("```", "")
                            # GitHub Push Logic
                            repo = "sukhdevlaxmi-coder/Rabbit-Al-6.py"
                            url = f"https://api.github.com/repos/{repo}/contents/app.py"
                            headers = {"Authorization": f"token {git_key}"}
                            r = requests.get(url, headers=headers)
                            if r.status_code == 200:
                                sha = r.json()['sha']
                                encoded = base64.b64encode(new_code.encode()).decode()
                                requests.put(url, headers=headers, json={"message": "Self-Evolution", "content": encoded, "sha": sha})
                                st.session_state.brain["history"].append(f"Evolved: {cmd[:20]}")
                                save_brain(st.session_state.brain)
                                st.balloons()
                                s.update(label="Evolution Successful! Refresh in 1 min.", state="complete")
                    except Exception as e: st.error(f"Logic Error: {e}")
                else: st.error("Model Connection Failed. Check Key.")

with t2:
    st.header("3D & 360° Media Processor")
    up_file = st.file_uploader("Upload Image", type=['jpg','png','jpeg'])
    if up_file:
        img = Image.open(up_file)
        st.image(img, caption="Original", use_container_width=True)
        if st.button("🔥 Process Technical 3D Render"):
            # Technical Depth Logic
            img_np = np.array(img.convert('RGB'))
            shift = 15
            three_d = np.zeros_like(img_np)
            three_d[:, shift:, 0] = img_np[:, :-shift, 0] # Red layer
            three_d[:, :-shift, 1:] = img_np[:, shift:, 1:] # Cyan layer
            st.image(Image.fromarray(three_d), caption="3D Rendered Output", use_container_width=True)

with t3:
    st.header("System Brain & Memory Logs")
    st.write("Laptop Memory Usage: Optimized")
    st.subheader("Neural History")
    for log in reversed(st.session_state.brain.get("history", [])[-5:]):
        st.caption(f"🧠 {log}")
