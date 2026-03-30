import streamlit as st
import google.generativeai as genai
import base64
import requests
import json
import os

# --- 1. BRAIN MEMORY GATE ---
MEMORY_FILE = "rabbit_brain_data.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try: return json.load(f)
            except: return {"history": [], "hcs_score": 0, "balance": 5000}
    return {"history": ["Initial Neural Link Established"], "hcs_score": 0, "balance": 5000}

def save_brain(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'brain' not in st.session_state:
    st.session_state.brain = load_brain()

# --- 2. SMART MODEL PICKER (NotFound Error Fix) ---
def get_stable_model(api_key):
    try:
        genai.configure(api_key=api_key)
        # 404 Fix: Sabse pehle 'gemini-1.5-flash-latest' try karein
        # Phir 'gemini-1.5-flash' aur 'gemini-pro'
        for model_name in ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro']:
            try:
                model = genai.GenerativeModel(model_name)
                # Ek chota test message
                model.generate_content("test") 
                return model
            except:
                continue
        return None
    except:
        return None

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="RABBIT 12.0 - SUPREME", layout="wide")
st.title("🛡️ NEURAL BRAIN - RABBIT 12.0")

with st.sidebar:
    st.header("⚙️ MASTER SETTINGS")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    st.divider()
    st.subheader("📚 Memory Logs")
    for log in reversed(st.session_state.brain.get("history", [])[-5:]):
        st.caption(f"🧠 {log}")

# --- 4. SELF-INVOLVING EVOLUTION ENGINE ---
st.subheader("🧬 Evolution Command (Brain Expansion)")
cmd = st.text_area("Order Rabbit (Hinglish):", placeholder="Rabbit, 360 viewer aur security active karo...")

if st.button("🚀 INITIATE EVOLUTION"):
    if gem_key and git_key and cmd:
        with st.status("Rabbit is Thinking & Rewriting...", expanded=True) as status:
            model = get_stable_model(gem_key)
            if model:
                try:
                    prompt = f"You are a Self-Evolving AI. Task: {cmd}. Rewrite the entire app.py code to include this. Return ONLY raw Python code."
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        new_code = response.text.strip().replace("```python", "").replace("```", "")
                        
                        # GitHub Update Logic
                        repo = "sukhdevlaxmi-coder/Rabbit-AI-6.py"
                        url = f"https://api.github.com/repos/{repo}/contents/app.py"
                        headers = {"Authorization": f"token {git_key}"}
                        
                        r = requests.get(url, headers=headers)
                        if r.status_code == 200:
                            sha = r.json()['sha']
                            encoded = base64.b64encode(new_code.encode()).decode()
                            requests.put(url, headers=headers, json={"message": "Evolution", "content": encoded, "sha": sha})
                            
                            st.session_state.brain["history"].append(f"Evolved: {cmd[:20]}")
                            save_brain(st.session_state.brain)
                            
                            st.balloons()
                            status.update(label="Evolution Successful! Refresh in 1 min.", state="complete")
                except Exception as e:
                    st.error(f"Logic Error: {e}")
            else:
                st.error("No compatible Gemini model found. Check API Key or Internet.")

# --- 5. TABS FOR OUTPUT ---
t1, t2, t3 = st.tabs(["📊 Family Data", "📚 HCS Master", "🎬 Multimedia"])

with t1:
    st.metric("Total Family Funds", f"${st.session_state.brain.get('balance', 5000)}")
    st.write("Local Brain (Ollama) is ready.")

with t2:
    st.write(f"HCS Knowledge Score: {st.session_state.brain.get('hcs_score', 0)}")
    if st.button("Add Progress"):
        st.session_state.brain['hcs_score'] += 1
        save_brain(st.session_state.brain)
        st.rerun()

with t3:
    st.info("360 Photo/Video Editor engine is standing by...")
