import streamlit as st
import json
import os
import math
import time
import google.generativeai as genai
import base64
import requests

# --- 1. EXTERNAL NEURAL MEMORY (Rabbit ki Yaddasht) ---
# Ye file Rabbit ke brain ka data (Balance, HCS score, Logs) save rakhegi.
MEMORY_FILE = "rabbit_brain_data.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {"balance": 5000.75, "hcs_score": 0, "logs": [], "version": "12.0"}
    return {"balance": 5000.75, "hcs_score": 0, "logs": ["System Booted"], "version": "12.0"}

def save_brain(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Brain Initialize karein
if 'brain' not in st.session_state:
    st.session_state.brain = load_brain()

# --- 2. CONFIGURATION & UI ---
st.set_page_config(page_title="RABBIT AI 12.0 - SELF EVOLVING", layout="wide")

# Neon Matrix Style UI
st.markdown("""
    <style>
    .main { background-color: #000000; color: #00FFCC; font-family: 'Courier New', monospace; }
    .stButton>button { background: linear-gradient(45deg, #00FFCC, #0080FF); color: black; font-weight: bold; border-radius: 8px; border: none; box-shadow: 0 0 10px #00FFCC; }
    .stTextArea>div>div>textarea { background-color: #0a0a0a; color: #00FFCC; border: 1px solid #00FFCC; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: BRAIN MONITOR ---
with st.sidebar:
    st.title("🐰 RABBIT CORE")
    gemini_key = st.text_input("Gemini API Key:", type="password")
    github_token = st.text_input("GitHub Token:", type="password")
    
    st.divider()
    st.subheader("🧬 Neural Evolution Log")
    for log in reversed(st.session_state.brain["logs"][-10:]):
        st.caption(f"⚡ {log}")
    
    if st.button("Reset Neural Paths"):
        st.session_state.brain = load_brain()
        save_brain(st.session_state.brain)
        st.rerun()

# --- 4. THE EVOLUTION ENGINE (Thinking & Writing Code) ---
def push_to_github(new_code, commit_msg):
    repo_owner = "sukhdevlaxmi-coder"
    repo_name = "Rabbit-Al-6.py"
    file_path = "app.py"
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}
    
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        sha = res.json()['sha']
        encoded = base64.b64encode(new_code.encode('utf-8')).decode('utf-8')
        data = {"message": commit_msg, "content": encoded, "sha": sha}
        put_res = requests.put(url, headers=headers, json=data)
        return put_res.status_code
    return res.status_code

# --- MAIN INTERFACE ---
st.title("🛡️ SUPREME MASTER - RABBIT 12.0")
st.write("Status: Self-Evolving Mode Active 🧠")

tabs = st.tabs(["🧬 Evolve Brain", "🎬 Multimedia", "🎮 Gaming", "📚 HCS Master", "🔐 Guardian"])

# TAB 0: EVOLUTION (The Self-Involving Part)
with tabs[0]:
    st.header("Brain Expansion Interface")
    st.info("Sukhi Ram ji, Rabbit ko jo bhi naya sikhana hai yahan likhein.")
    evolution_input = st.text_area("Next Evolution Command:", placeholder="E.g. Rabbit, ek naya tab banao family tracking ke liye aur interface gold karo.")
    
    if st.button("🚀 INITIATE EVOLUTION"):
        if evolution_input and gemini_key and github_token:
            with st.spinner("Rabbit is thinking and rewriting its own code..."):
                try:
                    genai.configure(api_key=gemini_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"""
                    You are Rabbit AI 12.0. Your current code is a Streamlit app. 
                    Task: {evolution_input}.
                    Rules: 
                    1. Return the FULL updated app.py code. 
                    2. Maintain the 'push_to_github' function and 'brain' memory logic.
                    3. Ensure it's self-evolving.
                    Return ONLY raw code.
                    """
                    response = model.generate_content(prompt)
                    if response.text:
                        clean_code = response.text.strip().replace("```python", "").replace("```", "")
                        status = push_to_github(clean_code, "Self-Evolution Update")
                        if status in [200, 201]:
                            st.balloons()
                            st.session_state.brain["logs"].append(f"Evolved: {evolution_input[:20]}")
                            save_brain(st.session_state.brain)
                            st.success("Evolution Complete! 1 min baad refresh karein.")
                        else: st.error(f"GitHub Error: {status}")
                except Exception as e: st.error(f"Evolution Failed: {e}")

# TAB 1: MULTIMEDIA
with tabs[1]:
    st.header("360° Media Center")
    if st.button("Scan Media Library"):
        st.write("Searching external storage...")
        time.sleep(1)
        st.success("Connected to Drive/Local Storage.")

# TAB 2: GAMING
with tabs[2]:
    st.header("Physics Simulator")
    angle = st.slider("Launch Angle", 0, 90, 45)
    if st.button("Launch Test"):
        st.write(f"Calculating Trajectory for {angle} degrees...")

# TAB 3: HCS MASTER
with tabs[3]:
    st.header("HCS Prep Hub")
    st.write(f"Knowledge Level: {st.session_state.brain['hcs_score']}")
    if st.button("Generate Today's Set"):
        st.session_state.brain["hcs_score"] += 1
        save_brain(st.session_state.brain)
        st.rerun()

# TAB 4: GUARDIAN
with tabs[4]:
    st.header("Bank & Security")
    st.metric("Balance", f"${st.session_state.brain['balance']}")
    if st.button("Secure Deposit $100"):
        st.session_state.brain["balance"] += 100
        st.session_state.brain["logs"].append("Deposited $100")
        save_brain(st.session_state.brain)
        st.rerun()
