import streamlit as st
import google.generativeai as genai
import base64
import requests
import json
import os
import traceback
from datetime import datetime

# ---------------- MEMORY ----------------
MEMORY_FILE = "rabbit_brain_data.json"
BACKUP_FILE = "backup_app.py"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"version": 1.0, "history": ["System Started"], "errors": []}

def save_brain(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

if "brain" not in st.session_state:
    st.session_state.brain = load_brain()

# ---------------- GEMINI ----------------
def get_model(api_key):
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        st.error(f"Model error: {e}")
        return None

# ---------------- SAFE RESPONSE ----------------
def get_ai_code(model, prompt):
    try:
        response = model.generate_content(prompt)

        text = ""
        if hasattr(response, "text") and response.text:
            text = response.text
        else:
            text = response.candidates[0].content.parts[0].text

        text = text.strip().replace("```python", "").replace("```", "")

        if len(text) < 50:
            return None

        return text

    except Exception as e:
        st.error("⚠️ AI response error")
        st.text(traceback.format_exc())
        return None

# ---------------- BACKUP ----------------
def save_backup(code):
    with open(BACKUP_FILE, "w") as f:
        f.write(code)

# ---------------- GITHUB PUSH ----------------
def push_to_github(code, token):
    repo = "sukhdevlaxmi-coder/Rabbit-AI-6"  # FIXED
    path = "app.py"

    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"}

    r = requests.get(url, headers=headers)

    sha = None
    if r.status_code == 200:
        sha = r.json()["sha"]

    data = {
        "message": f"Auto Update {datetime.now()}",
        "content": base64.b64encode(code.encode()).decode(),
    }

    if sha:
        data["sha"] = sha

    res = requests.put(url, headers=headers, json=data)

    if res.status_code in [200, 201]:
        return True
    else:
        st.error(f"GitHub Error: {res.json()}")
        return False

# ---------------- UI ----------------
st.set_page_config(page_title="RABBIT AI STABLE", layout="wide")

st.title("🐰 RABBIT AI - STABLE ENGINE")

with st.sidebar:
    gem_key = st.text_input("Gemini API Key", type="password")
    git_key = st.text_input("GitHub Token", type="password")

    st.write(f"Version: {st.session_state.brain['version']}")

    if st.button("💾 Save Memory"):
        save_brain(st.session_state.brain)
        st.success("Saved")

# ---------------- MAIN ----------------
instruction = st.text_area("Instruction", placeholder="Add feature...")

if st.button("🚀 EXECUTE SAFE EVOLUTION"):

    if not (instruction and gem_key and git_key):
        st.warning("Sab fields bharo")
        st.stop()

    model = get_model(gem_key)

    if not model:
        st.stop()

    prompt = f"""
    You are a professional Python Streamlit developer.

    TASK:
    Improve this app safely.

    USER REQUEST:
    {instruction}

    RULES:
    - Return ONLY Python code
    - No explanation
    - No markdown
    - Keep existing structure stable
    """

    with st.spinner("AI working..."):

        new_code = get_ai_code(model, prompt)

        if not new_code:
            st.error("❌ AI ne valid code nahi diya")
            st.stop()

        # BACKUP FIRST
        save_backup(new_code)

        success = push_to_github(new_code, git_key)

        if success:
            st.success("✅ Code Updated Safely!")

            st.session_state.brain["version"] += 0.1
            st.session_state.brain["history"].append(
                f"Updated {datetime.now()}"
            )

            save_brain(st.session_state.brain)

        else:
            st.error("❌ GitHub push fail")

# ---------------- LOGS ----------------
st.subheader("🧠 Logs")

for log in reversed(st.session_state.brain["history"]):
    st.text(log)
