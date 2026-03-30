import streamlit as st
import google.generativeai as genai
import base64
import requests
import json
import os
import time

# --- INITIALIZE BRAIN (Safety First) ---
MEMORY_FILE = "rabbit_brain_data.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try: return json.load(f)
            except: return {"balance": 5000.75, "hcs_score": 0, "logs": []}
    return {"balance": 5000.75, "hcs_score": 0, "logs": ["System Booted"]}

if 'brain' not in st.session_state:
    st.session_state.brain = load_brain()

# --- UI SETTINGS ---
st.set_page_config(page_title="RABBIT 12.0 - LIVE", layout="wide")

with st.sidebar:
    st.header("🐰 MASTER CONTROL")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    
    st.divider()
    # OLLAMA CONFIG
    use_ollama = st.checkbox("Enable Local Ollama Brain")
    if use_ollama:
        st.info("Rabbit is now using your Laptop's Local Brain (Ollama) 🖥️")

# --- PROGRESS TRACKER FUNCTION ---
def push_with_progress(new_code, msg):
    progress_text = st.empty()
    progress_text.text("Connecting to GitHub...")
    
    repo_owner = "sukhdevlaxmi-coder"
    repo_name = "Rabbit-Al-6.py"
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/app.py"
    headers = {"Authorization": f"token {git_key}"}
    
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        progress_text.text("GitHub Found! Encrypting Brain...")
        sha = res.json()['sha']
        encoded = base64.b64encode(new_code.encode('utf-8')).decode('utf-8')
        put_res = requests.put(url, headers=headers, json={"message": msg, "content": encoded, "sha": sha})
        if put_res.status_code in [200, 201]:
            progress_text.text("Evolution Saved Successfully ✅")
            return True
    progress_text.text("Failed to Save ❌")
    return False

# --- MAIN INTERFACE ---
st.title("🛡️ SUPREME MASTER - RABBIT 12.0")

# Agar kuch show nahi ho raha, toh ye test button dabayein
if st.button("🔄 Check System Status"):
    st.write(f"Brain Version: {st.session_state.brain.get('version', '12.0')}")
    st.write(f"HCS Prep Score: {st.session_state.brain.get('hcs_score', 0)}")
    st.success("System is Live and Waiting for Command!")

# EVOLUTION BOX
st.subheader("🧬 Evolution Command")
cmd = st.text_area("Write what Rabbit should do next:")

if st.button("🚀 EXECUTE"):
    if cmd and gem_key and git_key:
        with st.status("Rabbit is working...", expanded=True) as status:
            st.write("Thinking about your command...")
            # Gemini Logic
            genai.configure(api_key=gem_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"Rewrite app.py to: {cmd}. Return ONLY raw code.")
            
            st.write("Writing new Neural Paths (Code)...")
            if response.text:
                clean_c = response.text.strip().replace("```python", "").replace("```", "")
                if push_with_progress(clean_c, "Self-Evolution"):
                    st.balloons()
                    status.update(label="Evolution Complete!", state="complete", expanded=False)
