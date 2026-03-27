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
    
    # NAYE NAAM KE HISAB SE BILKUL SAHI CONFIG
    repo_owner = "sukhdevlaxmi-coder"
    repo_name = "Rabbit-AI-6"  # Aapka naya repo naam
    file_path = "app.py"       # Aapki asli file

    if gemini_key and github_key:
        try:
            genai.configure(api_key=gemini_key)
            # Smart model selection to avoid API version errors
            m_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            s_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in m_list else m_list[0]
            model = genai.GenerativeModel(s_model)
            st.success(f"Brain Active: {s_model} ✅")
        except Exception as e:
            st.error(f"Setup Error: {e}")

# --- FUNCTION: THE EVOLUTION ENGINE ---
def evolve_rabbit(new_code):
    try:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        headers = {
            "Authorization": f"token {github_key}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # 1. Get SHA (Current file state)
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            sha = res.json()['sha']
            # 2. Encode New Code
            encoded = base64.b64encode(new_code.encode('utf-8')).decode('utf-8')
            data = {
                "message": "Rabbit 12.0: Self-Evolution Sync",
                "content": encoded,
                "sha": sha
            }
            # 3. Push to GitHub
            put_res = requests.put(url, headers=headers, json=data)
            return put_res.status_code
        return res.status_code
    except Exception as e:
        return str(e)

# --- MAIN INTERFACE ---
st.title("🚀 RABBIT 12.0 - MASTER CONTROL")
st.info(f"Connected to: {repo_name} | Status: Ready for Evolution")

instruction = st.text_area("Sukhi Ram ji, Rabbit ko kya naya feature dena hai?", 
                          placeholder="Example: Background blue karo aur HCS Exam Quiz ka button banao.")

if st.button("EXECUTE EVOLUTION"):
    if instruction and gemini_key and github_key:
        with st.spinner("Rabbit apna naya code likh raha hai..."):
            try:
                # Instruction to rewrite the script but keep essential logic
                prompt = f"""
                You are Rabbit AI 12.0. File: {file_path}.
                User Instruction: {instruction}.
                STRICT RULE: Rewrite the ENTIRE Streamlit app code. 
                Keep the version as 'RABBIT 12.0'.
                MUST PRESERVE: All imports, sidebar configurations, and the 'evolve_rabbit' function.
                Return ONLY raw Python code. Do not use markdown backticks.
                """
                
                response = model.generate_content(prompt)
                
                if response and response.text:
                    clean_code = response.text.strip().replace("```python", "").replace("```", "")
                    
                    # Self-Update via GitHub API
                    status = evolve_rabbit(clean_code)
                    
                    if status in [200, 201]:
                        st.success("Mubarak ho! Update ho gaya. 2 minute rukiye aur refresh karein.")
                        st.balloons()
                    else:
                        st.error(f"GitHub Error {status}: Check Token permissions (repo scope).")
                else:
                    st.error("AI code generate nahi kar paya. Dobara try karein.")
            except Exception as e:
                st.error(f"Evolution Error: {e}")
    else:
        st.warning("Pehle Keys aur Instruction bharein!")
