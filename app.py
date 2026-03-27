import streamlit as st
import google.generativeai as genai
import base64
import requests

# --- CONFIG ---
st.set_page_config(page_title="RABBIT SELF-EVOLVER", layout="wide")

# --- SIDEBAR: SECURE KEYS ---
with st.sidebar:
    st.title("🐰 RABBIT CORE")
    gemini_key = st.text_input("Gemini API Key:", type="password")
    github_key = st.text_input("GitHub Token (PAT):", type="password")
    repo_name = "SukhiRam/Rabbit-AI-6" # Apna sahi repo name yahan likhein
    
    if gemini_key and github_key:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.success("Rabbit Brain & Hands Active! ✅")

# --- FUNCTION: SELF UPDATE LOGIC ---
def update_github_code(new_code):
    url = f"https://api.github.com/repos/{repo_name}/contents/app.py"
    headers = {"Authorization": f"token {github_key}"}
    
    # Purani file ki info lena (SHA hash ke liye)
    res = requests.get(url, headers=headers)
    sha = res.json()['sha']
    
    # Naya code upload karna
    content = base64.b64encode(new_code.encode()).decode()
    data = {
        "message": "Rabbit Self-Evolution: New Feature Added",
        "content": content,
        "sha": sha
    }
    final_res = requests.put(url, headers=headers, json=data)
    return final_res.status_code

# --- MAIN INTERFACE ---
st.title("🚀 AUTO-EVOLUTION MODE")
instruction = st.text_area("Rabbit ko kya naya sikhna ya badalna hai?")

if st.button("EXECUTE EVOLUTION"):
    if instruction and gemini_key and github_key:
        try:
            with st.spinner("Rabbit apna naya roop likh raha hai..."):
                # Yahan hum model ko dobara define kar rahe hain safety ke liye
                rabbit_brain = genai.GenerativeModel('gemini-1.5-flash')
                response = rabbit_brain.generate_content(instruction)
            
            if response and response.text:
                new_generated_code = response.text.replace("```python", "").replace("```", "")
                # Baki ka update logic yahan...
                st.success("Rabbit ne naya code soch liya hai!")
            else:
                st.error("Google ne koi jawab nahi diya. Dobara try karein.")
        except Exception as e:
            st.error(f"Evolution Error: {e}")
            
            # GitHub par khud ko update karna
            status = update_github_code(new_generated_code)
            
            if status == 200 or status == 201:
                st.success("Mubarak ho! Rabbit ne apna code khud update kar diya hai. 2 minute baad refresh karein.")
            else:
                st.error("GitHub update fail ho gaya. Token check karein.")
