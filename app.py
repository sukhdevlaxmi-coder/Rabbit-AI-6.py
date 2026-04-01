import streamlit as st
import google.generativeai as genai
import base64
import requests
import json
import os
import cv2
import numpy as np
from PIL import Image
import traceback

# --- 1. PERSISTENT NEURAL MEMORY (Laptop Sync) ---
MEMORY_FILE = "rabbit_brain_data.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try: 
                data = json.load(f)
                data.setdefault("version", 12.0)
                data.setdefault("history", [])
                return data
            except: pass
    return {"version": 12.0, "history": ["Core Initialized"], "errors_fixed": 0}

def save_brain(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'brain' not in st.session_state:
    st.session_state.brain = load_brain()

# --- 2. STABLE BRAIN CONNECT (Anti-404 Logic) ---
def get_stable_model(api_key):
    try:
        genai.configure(api_key=api_key)
        # Seedha stable Gemini Flash model (v1beta bypass)
        return genai.GenerativeModel('gemini-1.5-flash')
    except: return None

# --- 3. AUTO-UPDATE & SELF-CORRECTION ENGINE ---
def push_to_github(new_code, git_token, msg="Self-Evolution Update"):
    repo = "sukhdevlaxmi-coder/Rabbit-Al-6.py" # Verified: A + chota 'l'
    url = f"https://api.github.com/repos/{repo}/contents/app.py"
    headers = {"Authorization": f"token {git_token}"}
    
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        sha = r.json()['sha']
        res = requests.put(url, headers=headers, json={
            "message": msg,
            "content": base64.b64encode(new_code.encode()).decode(),
            "sha": sha
        })
        return res.status_code == 200
    return False

# --- 4. UI & STYLE ---
st.set_page_config(page_title="RABBIT 12.0 SUPREME CODER", layout="wide")
st.markdown("<style>.main { background-color: #000; color: #00FFCC; }</style>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🐰 MASTER CONSOLE")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    st.divider()
    st.write(f"System Version: **{st.session_state.brain['version']}**")
    st.write(f"Errors Fixed: **{st.session_state.brain.get('errors_fixed', 0)}**")
    if st.button("💾 Sync Memory"):
        save_brain(st.session_state.brain)
        st.success("Laptop Memory Locked!")

# --- 5. TABS & LOGIC ---
t1, t2, t3 = st.tabs(["🧬 Neural Evolution", "🎬 Multimedia 3D/360", "🧠 Brain Logs"])

with t1:
    st.header("Self-Involving Evolution Engine")
    instruction = st.text_area("Order Rabbit (Hinglish):", placeholder="Rabbit, ek naya real-time face detection module jodo...")
    
    if st.button("🚀 EXECUTE EVOLUTION"):
        if instruction and gem_key and git_key:
            with st.status("Rabbit is Rewriting Itself...") as s:
                model = get_stable_model(gem_key)
                if model:
                    try:
                        # Full System Prompt for Self-Evolution
                        prompt = f"""
                        You are Rabbit AI 12.0, a Supreme Coder. 
                        Current Code: {instruction}
                        TASK: Rewrite the entire app.py for Streamlit.
                        RULES:
                        1. Use 'gemini-1.5-flash' ONLY. No v1beta paths.
                        2. Maintain 'rabbit_brain_data.json' local storage logic.
                        3. Integrate 3D/360 Multimedia features.
                        4. Return ONLY raw Python code.
                        """
                        response = model.generate_content(prompt)
                        if response.text:
                            new_code = response.text.strip().replace("```python", "").replace("```", "")
                            if push_to_github(new_code, git_key):
                                st.session_state.brain["version"] += 0.1
                                st.session_state.brain["history"].append(f"Evolved to {st.session_state.brain['version']}")
                                save_brain(st.session_state.brain)
                                st.balloons()
                                s.update(label="Evolution Complete! 1 min baad refresh karein.", state="complete")
                    except Exception as e:
                        st.error(f"Auto-Correction Active: Detecting Error {e}")
                        # Self-Healing logic could go here to auto-fix 'e'

with t2:
    st.header("Technical Multimedia Lab")
    up = st.file_uploader("Upload for 3D processing", type=['jpg','png'])
    if up:
        img = Image.open(up)
        st.image(img, use_container_width=True)
        if st.button("Apply 3D Depth Render"):
            # Pixel Shift Logic (Simulated 3D)
            img_np = np.array(img.convert('RGB'))
            shift = 15
            three_d = np.zeros_like(img_np)
            three_d[:, shift:, 0] = img_np[:, :-shift, 0]
            three_d[:, :-shift, 1:] = img_np[:, shift:, 1:]
            st.image(Image.fromarray(three_d), caption="Technical 3D Render")

with t3:
    st.header("Neural Brain Logs")
    for log in reversed(st.session_state.brain["history"]):
        st.caption(f"🧠 {log}")
