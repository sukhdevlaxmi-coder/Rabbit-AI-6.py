import streamlit as st
import google.generativeai as genai
import base64
import requests
import json
import os

# --- 1. NEURAL MEMORY (Jo Rabbit Kabhi Nahi Bhulega) ---
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

# Memory ko session mein load karein
if 'brain' not in st.session_state:
    st.session_state.brain = load_brain()

# --- 2. SELF-EVOLVING ENGINE ---
st.set_page_config(page_title="RABBIT - SELF INVOLVING", layout="wide")
st.title("🛡️ NEURAL BRAIN - RABBIT 12.0")

with st.sidebar:
    st.header("⚙️ MASTER SETTINGS")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    
    st.divider()
    st.subheader("📚 Memory Logs")
    for log in reversed(st.session_state.brain.get("history", [])[-5:]):
        st.caption(f"🧠 {log}")

# --- 3. THE "SELF-INVOLVING" LOGIC ---
st.subheader("🧬 Evolution Command (Brain Expansion)")
cmd = st.text_area("Order Rabbit (Hinglish):", placeholder="Rabbit, 360 viewer jodo aur family data save karo...")

if st.button("🚀 INITIATE EVOLUTION"):
    if gem_key and git_key and cmd:
        with st.status("Rabbit is Thinking & Rewriting...", expanded=True) as status:
            genai.configure(api_key=gem_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Ye prompt Rabbit ko batata hai ki usey KHUD ko badalna hai
            prompt = f"""
            You are a Self-Evolving AI. Your code is in app.py. 
            User Task: {cmd}. 
            Instruction: Rewrite the entire app.py to include this feature. 
            Keep the memory loading/saving logic and GitHub sync intact. 
            Return ONLY raw Python code.
            """
            
            response = model.generate_content(prompt)
            if response.text:
                new_code = response.text.strip().replace("```python", "").replace("```", "")
                
                # GitHub Push
                repo = "sukhdevlaxmi-coder/Rabbit-Al-6.py"
                url = f"https://api.github.com/repos/{repo}/contents/app.py"
                headers = {"Authorization": f"token {git_key}"}
                
                r = requests.get(url, headers=headers)
                if r.status_code == 200:
                    sha = r.json()['sha']
                    encoded = base64.b64encode(new_code.encode()).decode()
                    requests.put(url, headers=headers, json={"message": "Self-Evolution", "content": encoded, "sha": sha})
                    
                    # Yaad rakhne ke liye log save karein
                    st.session_state.brain["history"].append(f"Evolved: {cmd[:20]}")
                    save_brain(st.session_state.brain)
                    
                    st.balloons()
                    status.update(label="Evolution Successful! Refresh in 1 min.", state="complete")

# --- 4. DATA DISPLAY (Jo hamesha dikhega) ---
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.metric("Family Funds (Saved)", f"${st.session_state.brain.get('balance', 5000)}")
with col2:
    st.write(f"HCS Mastery: {st.session_state.brain.get('hcs_score', 0)}")
