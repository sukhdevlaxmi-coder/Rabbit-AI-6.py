import streamlit as st
import google.generativeai as genai
import base64
import requests
import json
import os
import cv2
import numpy as np
from PIL import Image

# --- 1. MEMORY SYSTEM (Rabbit ka Dimaag) ---
MEMORY_FILE = "rabbit_brain_data.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try: return json.load(f)
            except: return {"hcs": 0, "balance": 5000, "history": []}
    return {"hcs": 0, "balance": 5000, "history": ["System Live"]}

def save_brain(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'brain' not in st.session_state:
    st.session_state.brain = load_brain()

# --- 2. FAIL-SAFE MODEL (No More 404 Error) ---
def get_rabbit_model(api_key):
    genai.configure(api_key=api_key)
    # Sabse stable models ki list
    for m_name in ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']:
        try:
            model = genai.GenerativeModel(m_name)
            return model
        except: continue
    return None

# --- 3. TECHNICAL 3D ENGINE ---
def make_3d(image):
    img = np.array(image.convert('RGB'))
    shift = 15
    three_d = np.zeros_like(img)
    three_d[:, shift:, 0] = img[:, :-shift, 0] # Red Shift
    three_d[:, :-shift, 1:] = img[:, shift:, 1:] # Cyan Shift
    return Image.fromarray(three_d)

# --- 4. UI SETUP ---
st.set_page_config(page_title="RABBIT 12.0 - SUPREME", layout="wide")
st.markdown("<style>.main { background-color: #000; color: #00FFCC; }</style>", unsafe_allow_html=True)

st.title("🛡️ MASTER SUKHI RAM - RABBIT 12.0")

with st.sidebar:
    st.header("⚙️ SETTINGS")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    st.divider()
    st.info(f"HCS Level: {st.session_state.brain.get('hcs', 0)}")
    st.info(f"Funds: ${st.session_state.brain.get('balance', 5000)}")

# --- 5. MAIN MODULES ---
t1, t2, t3 = st.tabs(["🖼️ 3D/360 Editor", "🧬 Evolution", "🔐 Family & Funds"])

with t1:
    st.header("Advanced 3D Media Lab")
    up = st.file_uploader("Upload Image", type=['jpg','png'])
    if up:
        img = Image.open(up)
        st.image(img, caption="Original", use_container_width=True)
        if st.button("🚀 Render 3D"):
            res = make_3d(img)
            st.image(res, caption="3D Technical Output", use_container_width=True)

with t2:
    st.subheader("Self-Evolving Brain")
    cmd = st.text_area("Order Rabbit (Hinglish):")
    if st.button("🔥 EVOLVE NOW"):
        if gem_key and git_key and cmd:
            with st.status("Rabbit is Rewriting Itself...") as s:
                model = get_rabbit_model(gem_key)
                if model:
                    prompt = f"Rewrite app.py to: {cmd}. Return ONLY raw Python code."
                    response = model.generate_content(prompt)
                    if response.text:
                        new_code = response.text.strip().replace("```python", "").replace("```", "")
                        # GitHub Sync
                        url = f"https://api.github.com/repos/sukhdevlaxmi-coder/Rabbit-AI-6.py/contents/app.py"
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
                            s.update(label="Rabbit Updated!", state="complete")

with t3:
    st.header("Secure Data Gate")
    st.metric("Balance", f"${st.session_state.brain['balance']}")
    if st.button("Save Progress"):
        st.session_state.brain['hcs'] += 1
        save_brain(st.session_state.brain)
        st.success("Memory Locked!")
