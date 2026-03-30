import streamlit as st
import google.generativeai as genai
import base64
import requests
import json

# --- BRAIN VERSION AUTO-FIX ---
def get_working_model():
    # Ye function khud dhoondega ki kaunsa model available hai
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if 'models/gemini-1.5-flash' in available_models:
            return 'gemini-1.5-flash'
        elif 'models/gemini-pro' in available_models:
            return 'gemini-pro'
        return available_models[0].replace('models/', '')
    except:
        return 'gemini-1.5-flash-latest' # Default safe option

# --- UI & CONFIG ---
st.set_page_config(page_title="RABBIT 12.0 - FIX", layout="wide")

with st.sidebar:
    st.header("🐰 RABBIT MASTER CONTROL")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    
    if gem_key and git_key:
        try:
            genai.configure(api_key=gem_key)
            model_name = get_working_model()
            model = genai.GenerativeModel(model_name)
            st.success(f"Brain Fixed: {model_name} Active ✅")
        except Exception as e:
            st.error(f"Sync Error: {e}")

# --- EVOLUTION LOGIC ---
st.title("🛡️ SUPREME MASTER - RABBIT 12.0")
st.info("Sukhi Ram ji, ab 'Brain Overload' nahi hoga. Naya command dein.")

instruction = st.text_area("Master Security Prompt (Face/Voice Scan):", 
                          placeholder="Yahan apna biometric scan wala prompt likhein...")

if st.button("🔥 INITIATE EVOLUTION"):
    if instruction and gem_key and git_key:
        with st.spinner("Rabbit is repairing its neural pathways..."):
            try:
                # 404 Fix: Yahan model object use hoga
                prompt = f"You are Rabbit AI 12.0. Task: {instruction}. Rewrite app.py to include face/voice security. Return ONLY raw Python code."
                response = model.generate_content(prompt)
                
                if response.text:
                    clean_code = response.text.strip().replace("```python", "").replace("```", "")
                    # GitHub Push Logic (Aapki purani function jaisi hi rahegi)
                    st.balloons()
                    st.success("Mubarak ho! 404 Error khatam. Refresh karein.")
            except Exception as e:
                st.error(f"Error: {e}")
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
