import streamlit as st
import google.generativeai as genai
import base64
import requests

# --- BASIC CONFIG ---
st.set_page_config(page_title="RABBIT 12.0 - MASTER", layout="wide")

# --- SIDEBAR: CORE SETTINGS ---
with st.sidebar:
    st.title("🐰 RABBIT CORE")
    st.markdown("---")
    gemini_key = st.text_input("Gemini API Key:", type="password")
    github_key = st.text_input("GitHub Token (PAT):", type="password")
    
    # --- UPDATE THESE TWO LINES IF NEEDED ---
    repo_owner = "sukhdevlaxmi-coder"
    # Yahan apni repository ka NAYA NAAM likhein (e.g., 'Rabbit-AI')
    repo_name = st.text_input("GitHub Repo Name:", value="Rabbit-AI-6") 
    file_path = "Rabbit-AI-6.py" 

    if gemini_key and github_key:
        try:
            genai.configure(api_key=gemini_key)
            # 404 Error se bachne ke liye smart model selection
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            selected_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
            
            model = genai.GenerativeModel(selected_model)
            st.success(f"Brain Active: {selected_model} ✅")
        except Exception as e:
            st.error(f"Setup Error: {e}")

# --- FUNCTION: THE SELF-EVOLUTION ENGINE ---
def evolve_rabbit(new_code):
    try:
        # Naye repo name ke saath URL
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        headers = {"Authorization": f"token {github_key}"}
        
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            sha = res.json()['sha']
            encoded_content = base64.b64encode(new_code.encode()).decode()
            data = {
                "message": "Rabbit Evolution: Name Updated & Auto-Sync",
                "content": encoded_content,
                "sha": sha
            }
            put_res = requests.put(url, headers=headers, json=data)
            return put_res.status_code
        else:
            return res.status_code
    except Exception as e:
        return str(e)

# --- MAIN INTERFACE ---
st.title("🚀 RABBIT SELF-EVOLUTION MODE")
st.info("Sukhi Ram ji, ab Rabbit naye raste par doudne ke liye taiyar hai!")

instruction = st.text_area("Rabbit ko kya badalna hai?", 
                          placeholder="Example: Background light blue karo aur 'HCS Exam Prep' button banao.")

if st.button("EXECUTE EVOLUTION"):
    if instruction and gemini_key and github_key:
        with st.spinner("Rabbit apna naya roop (Code) likh raha hai..."):
            try:
                # --- SMART MODEL DISCOVERY ---
                # Ye line khud check karegi ki aapke API par kaunsa model zinda hai
                models_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                # Agar 'models/gemini-1.5-flash' milta hai toh wo, nahi toh pehla available model
                final_model_name = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in models_list else models_list[0]
                
                rabbit_brain = genai.GenerativeModel(final_model_name)
                
                prompt = f"""
                You are Rabbit AI. Your file name is {file_path}.
                Based on this instruction: '{instruction}', rewrite the ENTIRE Streamlit app code.
                STRICT RULE: Keep all imports, sidebar logic, and 'evolve_rabbit' function as they are.
                Return ONLY raw Python code. No markdown.
                """
                
                response = rabbit_brain.generate_content(prompt)
                
                if response and response.text:
                    clean_code = response.text.strip()
                    if clean_code.startswith("```"):
                        clean_code = clean_code.split("\n", 1)[1].rsplit("\n", 1)[0]
                    
                    status = evolve_rabbit(clean_code)
                    
                    if status in [200, 201]:
                        st.success(f"Mubarak ho! {final_model_name} use karke update ho gaya. 2 min baad refresh karein.")
                        st.balloons()
                    else:
                        st.error(f"GitHub Error: {status}")
            except Exception as e:
                st.error(f"Evolution Error (Model Issue): {e}")
