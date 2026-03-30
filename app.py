import streamlit as st
import google.generativeai as genai
import base64
import requests
import json
import os
import time
import math

# --- BRAIN DATA PERSISTENCE ---
MEMORY_FILE = "rabbit_brain_data.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try: return json.load(f)
            except: return {"balance": 5000.75, "hcs_score": 0, "logs": []}
    return {"balance": 5000.75, "hcs_score": 0, "logs": ["System Booted"]}

def save_brain(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'brain' not in st.session_state:
    st.session_state.brain = load_brain()

# --- MODEL SELECTION LOGIC ---
def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if 'models/gemini-1.5-flash' in available_models: return 'gemini-1.5-flash'
        return available_models[0].replace('models/', '')
    except: return 'gemini-1.5-flash-latest'

# --- UI CONFIG ---
st.set_page_config(page_title="RABBIT 12.0 - SUPREME", layout="wide")

with st.sidebar:
    st.header("🐰 RABBIT MASTER CONTROL")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    
    st.divider()
    st.subheader("⚙️ Local Brain (Ollama)")
    ollama_active = st.checkbox("Use Local Ollama (Offline Mode)")
    
    if gem_key and git_key:
        try:
            genai.configure(api_key=gem_key)
            model_name = get_working_model()
            model = genai.GenerativeModel(model_name)
            st.success(f"Brain Fixed: {model_name} Active ✅")
        except Exception as e:
            st.error(f"Sync Error: {e}")

# --- GITHUB PUSH FUNCTION ---
def push_to_github(new_code, commit_msg):
    repo_owner = "sukhdevlaxmi-coder"
    repo_name = "Rabbit-Al-6.py"
    file_path = "app.py"
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {"Authorization": f"token {git_key}", "Accept": "application/vnd.github.v3+json"}
    
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        sha = res.json()['sha']
        encoded = base64.b64encode(new_code.encode('utf-8')).decode('utf-8')
        put_res = requests.put(url, headers=headers, json={"message": commit_msg, "content": encoded, "sha": sha})
        return put_res.status_code
    return 404

# --- MAIN INTERFACE ---
st.title("🛡️ SUPREME MASTER - RABBIT 12.0")
st.write(f"Status: {'Ollama Local' if ollama_active else 'Cloud Neural'} Active 🧠")

tabs = st.tabs(["🧬 Evolve Brain", "🎬 Multimedia", "🎮 Gaming", "📚 HCS Master", "🔐 Guardian"])

# TAB 0: EVOLUTION
with tabs[0]:
    st.header("Brain Expansion Interface")
    evolution_input = st.text_area("Next Evolution Command:", placeholder="E.g. Rabbit, family tracking tab banao.")
    
    if st.button("🚀 INITIATE EVOLUTION"):
        if evolution_input and gem_key and git_key:
            with st.spinner("Rabbit is evolving..."):
                try:
                    # Logic: If Ollama is checked, it could use local API (Future setup)
                    prompt = f"You are Rabbit AI 12.0. Task: {evolution_input}. Return ONLY raw Python code."
                    response = model.generate_content(prompt)
                    if response.text:
                        clean_code = response.text.strip().replace("```python", "").replace("```", "")
                        status = push_to_github(clean_code, "Self-Evolution Update")
                        if status in [200, 201]:
                            st.balloons()
                            st.session_state.brain["logs"].append(f"Evolved: {evolution_input[:20]}")
                            save_brain(st.session_state.brain)
                            st.success("Evolution Complete! Refresh karein.")
                except Exception as e: st.error(f"Failed: {e}")

# TAB 1: MULTIMEDIA
with tabs[1]:
    st.header("360° Media & Video Editor")
    st.write("Ollama analyzing media trends...")
    if st.button("Scan Library"):
        st.success("Connected to External Storage.")

# TAB 3: HCS MASTER (Error Fixed: Using .get() for safety)
with tabs[3]:
    st.header("HCS Prep Hub")
    score = st.session_state.brain.get('hcs_score', 0)
    st.write(f"Knowledge Level: {score}")
    if st.button("Generate Today's Set"):
        st.session_state.brain["hcs_score"] = score + 1
        save_brain(st.session_state.brain)
        st.rerun()

# TAB 4: GUARDIAN
with tabs[4]:
    st.header("Bank & Security")
    bal = st.session_state.brain.get('balance', 5000.75)
    st.metric("Balance", f"${bal}")
    if st.button("Secure Deposit $100"):
        st.session_state.brain["balance"] = bal + 100
        save_brain(st.session_state.brain)
        st.rerun()
