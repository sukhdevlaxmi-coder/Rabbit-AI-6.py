import streamlit as st
import google.generativeai as genai
import base64
import requests

st.set_page_config(page_title="RABBIT 9.5 MASTER", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.title("🐰 RABBIT CORE")
    gemini_key = st.text_input("Gemini API Key:", type="password")
    github_key = st.text_input("GitHub Token (PAT):", type="password")
    repo_name = st.text_input("Repo (e.g. Sukhdev-Laxmi/Rabbit-AI-6):", value="Sukhdev-Laxmi/Rabbit-AI-6")
    
    if gemini_key and github_key:
        try:
            genai.configure(api_key=gemini_key)
        
            # Ye line available models ki list mangwayegi
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
            # Agar flash model list mein hai toh wahi use karein, nahi toh pehla available model
            selected_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in models else models[0]
        
            model = genai.GenerativeModel(selected_model)
            st.success(f"Brain Active with {selected_model}! ✅")
        except Exception as e:
            st.error(f"Brain Connection Error: {e}")            

# --- UPDATE FUNCTION ---
def update_github_code(new_code):
    try:
        url = f"https://api.github.com/repos/{repo_name}/contents/app.py"
        headers = {"Authorization": f"token {github_key}"}
        res = requests.get(url, headers=headers)
    if res.status_code == 200:
            sha = res.json()['sha']
            content = base64.b64encode(new_code.encode()).decode()
            data = {"message": "Rabbit Self-Evolution", "content": content, "sha": sha}
            put_res = requests.put(url, headers=headers, json=data)
            return put_res.status_code
        return res.status_code
    except:
        return 500

# --- MAIN ---
st.title("🚀 RABBIT AUTO-EVOLVE")
instruction = st.text_area("Aapki Instruction (Rabbit kya naya sikhe?):")

if st.button("EXECUTE EVOLUTION"):
    if instruction and gemini_key and github_key:
        with st.spinner("Rabbit evolution in progress..."):
            try:
                # AI Logic
                prompt = f"Improve this Streamlit code based on: {instruction}. Return ONLY Python code."
                response = model.generate_content(prompt)
                
                if response and response.text:
                    clean_code = response.text.replace("```python", "").replace("```", "")
                    status = update_github_code(clean_code)
                    if status in [200, 201]:
                        st.success("Mubarak ho! Rabbit ne khud ko update kar liya hai. 2 min baad refresh karein.")
                    else:
                        st.error(f"GitHub Error: {status}")
            except Exception as e:
                st.error(f"Error: {e}")
