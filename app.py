import streamlit as st
import google.generativeai as genai
import base64
import requests

# --- CONFIG ---
st.set_page_config(page_title="RABBIT 12.0", layout="wide")

st.markdown("""
    <style>
    .main { background: #000000; color: #00FFCC; }
    .stButton>button { background: linear-gradient(45deg, #00f2fe, #4facfe); color: black; font-weight: bold; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.header("🐰 RABBIT MASTER CORE")
    gem_key = st.text_input("Gemini API Key:", type="password")
    git_key = st.text_input("GitHub Token:", type="password")
    
    # AAPKI PDF KE HISAB SE SAHI NAAM
    repo_owner = "sukhdevlaxmi-coder"
    repo_name = "Rabbit-Al-6.py" # L for Lion wala 'l'
    file_path = "app.py"

    if gem_key and git_key:
        try:
            genai.configure(api_key=gem_key)
            # Smart Model Search
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            active_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in models else models[0]
            model = genai.GenerativeModel(active_model)
            st.success(f"Guardian Brain Active: {active_model} ✅")
        except Exception as e:
            st.error(f"Brain Sync Error: {e}")

def push_to_github(new_code, msg):
    try:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        headers = {"Authorization": f"token {git_key}", "Accept": "application/vnd.github.v3+json"}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            sha = res.json()['sha']
            encoded = base64.b64encode(new_code.encode('utf-8')).decode('utf-8')
            data = {"message": msg, "content": encoded, "sha": sha}
            put_res = requests.put(url, headers=headers, json=data)
            return put_res.status_code
        return res.status_code
    except: return 500

st.title("🛡️ MASTER SUKHI RAM - RABBIT 12.0")
instruction = st.text_area("Supreme Command:")

if st.button("🔥 EXECUTE EVOLUTION"):
    if instruction and gem_key and git_key:
        with st.spinner("Rabbit is evolving..."):
            try:
                prompt = f"You are Rabbit AI. Task: {instruction}. Return ONLY raw Python code. No backticks."
                response = model.generate_content(prompt)
                if response.text:
                    clean_c = response.text.strip().replace("```python", "").replace("```", "")
                    status = push_to_github(clean_c, "Supreme Sync")
                    if status in [200, 201]:
                        st.balloons()
                        st.success("Mubarak ho! Update ho gaya. Refresh karein.")
                    else:
                        st.error(f"GitHub Error {status}: Check Token Scopes (Repo Tick).")
            except Exception as e:
                st.error(f"Error: {e}")
