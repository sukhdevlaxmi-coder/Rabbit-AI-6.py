import streamlit as st
import google.generativeai as genai
import base64
import requests
import json
import os
import cv2
import numpy as np
from PIL import Image
import time

# --- 1. NEURAL MEMORY (Self-Involving Gate) ---
MEMORY_FILE = "rabbit_brain_data.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try: return json.load(f)
            except: return {"hcs_score": 0, "balance": 5000, "history": []}
    return {"hcs_score": 0, "balance": 5000, "history": ["Core Initialized"]}

def save_brain(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'brain' not in st.session_state:
    st.session_state.brain = load_brain()

# --- 2. UI & STYLE ---
st.set_page_config(page_title="RABBIT 12.0 - TECH CORE", layout="wide")
st.markdown("<style>.main { background-color: #050505; color: #00FFCC; }</style>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🐰 MASTER CONTROL")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    st.divider()
    st.write(f"Knowledge: {st.session_state.brain.get('hcs_score', 0)}")
    st.write(f"Funds: ${st.session_state.brain.get('balance', 5000)}")

# --- 3. TECHNICAL 3D & 360 ENGINE ---
def process_3d_effect(image):
    # Technical Red-Cyan Anaglyph Depth Logic
    img = np.array(image.convert('RGB'))
    new_img = np.zeros_like(img)
    shift = 15
    new_img[:, shift:, 0] = img[:, :-shift, 0] # Red Channel Shift
    new_img[:, :-shift, 1:] = img[:, shift:, 1:] # Cyan Channel Shift
    return Image.fromarray(new_img)

st.title("🛡️ RABBIT 12.0 - SUPREME TECH INTERFACE")

tabs = st.tabs(["🎥 Multimedia 3D", "🧬 Evolution", "🔐 Guardian"])

with tabs[0]:
    st.header("Technical 360° & 3D Editor")
    up_file = st.file_uploader("Upload Photo/Video for 3D processing", type=['jpg','png','mp4'])
    
    if up_file:
        if up_file.type.startswith('image'):
            img = Image.open(up_file)
            st.image(img, caption="Original", use_container_width=True)
            
            if st.button("🚀 Generate 3D Technical Render"):
                with st.spinner("Processing 3D Depth Map..."):
                    res = process_3d_effect(img)
                    st.image(res, caption="3D Rendered Output", use_container_width=True)
                    st.success("3D Processing Complete!")
        else:
            st.video(up_file)
            st.info("Video AI Analysis Active: Frame-by-frame depth extraction standing by.")

with tabs[1]:
    st.subheader("Neural Expansion (Self-Evolution)")
    cmd = st.text_area("Order Rabbit (Hinglish):", placeholder="Rabbit, Madhav ke liye 3D game tab banao...")
    
    if st.button("🔥 EXECUTE EVOLUTION"):
        if gem_key and git_key and cmd:
            with st.status("Rabbit is Rewriting Neural Pathways...") as s:
                genai.configure(api_key=gem_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"Rewrite app.py to: {cmd}. Focus on high-end 3D graphics. Return ONLY raw code."
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
                        requests.put(url, headers=headers, json={
                            "message": "3D Tech Update", 
                            "content": base64.b64encode(new_code.encode()).decode(),
                            "sha": sha
                        })
                        st.session_state.brain["history"].append(f"Evolved 3D: {cmd[:15]}")
                        save_brain(st.session_state.brain)
                        st.balloons()
                        s.update(label="Evolution Complete! Refresh karein.", state="complete")

with tabs[2]:
    st.header("Security & Funds")
    st.metric("Family Balance", f"${st.session_state.brain['balance']}")
    if st.button("Add Progress"):
        st.session_state.brain['hcs_score'] += 1
        save_brain(st.session_state.brain)
        st.rerun()
