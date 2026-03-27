import streamlit as st
import google.generativeai as genai

# --- 1. SETTINGS ---
st.set_page_config(page_title="RABBIT 9.0 - MASTER", layout="wide")

# --- 2. SIDEBAR (Naya Sidebar Yahan Hai) ---
with st.sidebar:
    st.title("🐰 RABBIT CONTROL")
    # YAHAN AAYEGA API BOX
    api_key = st.text_input("🔑 Enter Gemini API Key:", type="password")
    
    st.write("---")
    st.write("**Owner:** Sukhi Ram")
    st.write("**Status:** Evolving...")
    
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        st.success("Brain Active! ✅")
    else:
        st.warning("Key ka intezaar hai... ⏳")

# --- 3. MAIN BODY ---
st.title("🚀 SELF-EVOLVING ENGINE")
user_input = st.text_input("Rabbit ko command dein (Hindi/Python/C++):")

if user_input and api_key:
    response = model.generate_content(user_input)
    st.markdown(f"**Rabbit:** {response.text}")

# --- 4. HCS & OFFICE SECTION ---
tabs = st.tabs(["📚 HCS Academy", "📝 Drafting Desk"])
with tabs[0]:
    st.write("76 Sets Database Online.")
with tabs[1]:
    st.write("Architecture Dept Templates Ready.")
