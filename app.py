import streamlit as st
from google import genai
import json
import os
import traceback

# ---------------- MEMORY ----------------
MEMORY_FILE = "rabbit_brain_data.json"

def load_brain():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)
        except:
            data = {}
    else:
        data = {}

    data.setdefault("version", 1.0)
    data.setdefault("history", ["System Started"])
    return data

def save_brain(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

if "brain" not in st.session_state:
    st.session_state.brain = load_brain()

# ---------------- AI FUNCTION ----------------
def get_ai_code(api_key, prompt):
    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        text = response.text

        if not text or len(text) < 20:
            return None

        return text.strip().replace("```python", "").replace("```", "")

    except Exception as e:
        if "API key expired" in str(e):
            st.error("❌ API Key expire ho gayi hai, nayi key dalo")
        else:
            st.error("AI Error")
            st.text(traceback.format_exc())
        return None

# ---------------- UI ----------------
st.set_page_config(page_title="RABBIT AI", layout="wide")

st.title("🐰 RABBIT AI - Stable Version")

with st.sidebar:
    gem_key = st.text_input("Gemini API Key", type="password")

    st.write(f"Version: {st.session_state.brain['version']}")

    if st.button("💾 Save Memory"):
        save_brain(st.session_state.brain)
        st.success("Saved")

# ---------------- MAIN ----------------
instruction = st.text_area("Instruction", placeholder="Feature add ya bug fix likho...")

if st.button("🚀 EXECUTE"):

    if not gem_key:
        st.error("API key daalo")
        st.stop()

    if not instruction:
        st.warning("Instruction likho")
        st.stop()

    prompt = f"""
    Improve this Streamlit app safely.

    USER REQUEST:
    {instruction}

    RULES:
    - No infinite loops
    - Do not break existing code
    - Only improve required part
    - Return only Python code
    """

    with st.spinner("AI working..."):
        new_code = get_ai_code(gem_key, prompt)

        if not new_code:
            st.error("❌ AI ne valid code nahi diya")
            st.stop()

        st.success("✅ Code Generated!")

        st.code(new_code, language="python")

        st.session_state.brain["version"] += 0.1
        st.session_state.brain["history"].append("Update done")
        save_brain(st.session_state.brain)

# ---------------- LOGS ----------------
st.subheader("🧠 Logs")

for log in reversed(st.session_state.brain.get("history", [])):
    st.text(log)
