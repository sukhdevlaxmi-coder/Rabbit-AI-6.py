import streamlit as st
import google.generativeai as genai
import base64
import requests

# --- BASIC CONFIG ---
st.set_page_config(page_title="RABBIT 12.0", layout="wide")

# --- SIDEBAR: CORE SETTINGS ---
with st.sidebar:
    st.title("🐰 RABBIT CORE 12.0")
    st.markdown("---")
    gemini_key = st.text_input("Gemini API Key:", type="password")
    github_key = st.text_input("GitHub Token (PAT):", type="password")
    
    # PDF KE HISAB SE BILKUL SAHI NAAM
    repo_owner = "sukhdevlaxmi-coder"
    repo_name = "Rabbit-Al-6.py" # Aapki repo ka asli naam yahi hai
    file_path = "app.py"         # Aapki file ka asli naam yahi hai

    if gemini_key and github_key:
        try:
            genai.configure(api_key=gemini_key)
            # 404 Error fix: Automatic model detection
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            selected_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
            
            model = genai.GenerativeModel(selected_model)
            st.success(f"Brain Active: {selected_model} ✅")
        except Exception as e:
            st.error(f"Setup Error: {e}")

# --- FUNCTION: THE EVOLUTION ENGINE ---
def evolve_rabbit(new_code):
    try:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        headers = {"Authorization": f"token {github_key}"}
        
        # 1. Get SHA
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            sha = res.json()['sha']
            # 2. Encode
            encoded_content = base64.b64encode(new_code.encode()).decode()
            data = {
                "message": "Rabbit 12.0 Evolution",
                "content": encoded_content,
                "sha": sha
            }
            # 3. Update
            put_res = requests.put(url, headers=headers, json=data)
            return put_res.status_code
        else:
            return res.status_code
    except Exception as e:
        return str(e)

# --- MAIN INTERFACE ---
st.title("🚀 RABBIT 12.0 - SELF EVOLUTION")
st.info(f"Connected to: {repo_name}/{file_path}")

instruction = st.text_area("Sukhi Ram ji, Rabbit ko kya naya sikhana hai?", 
                          placeholder="Example: Background yellow karo aur HCS Exam Quiz ka button banao.")

if st.button("EXECUTE EVOLUTION"):
    if instruction and gemini_key and github_key:
        with st.spinner("Rabbit code likh raha hai..."):
            try:
                # Instruction to rewrite the script but KEEP version 12.0
                prompt = f"""
                You are Rabbit AI Version 12.0. 
                Instruction: {instruction}.
                STRICT RULE: Rewrite the ENTIRE Streamlit code. 
                Keep the title as 'RABBIT 12.0' always.
                Keep all imports, sidebar logic, and 'evolve_rabbit' function exactly as they are.
                Return ONLY raw Python code. No markdown.
                """
                
                response = model.generate_content(prompt)
                
                if response and response.text:
                    clean_code = response.text.strip()
                    if clean_code.startswith("```"):
                        clean_code = clean_code.split("\n", 1)[1].rsplit("\n", 1)[0]
                    
                    status = evolve_rabbit(clean_code)
                    
                    if status in [200, 201]:
                        st.success("Mubarak ho! Rabbit 12.0 update ho gaya. 2 min baad refresh karein.")
                        st.balloons()
                    else:
                        st.error(f"GitHub Error {status}: Repo settings check karein.")
                else:
                    st.error("AI code generate nahi kar paya.")
            except Exception as e:
                st.error(f"Evolution Error: {e}")
    else:
        st.warning("Pehle Keys aur Instruction bharein!")
