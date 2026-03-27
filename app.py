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
    try:
        genai.configure(api_key=api_key)
        # Naya Model Name Yahan Hai:
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.success("Brain Active with Gemini 1.5! ✅")
    except Exception as e:
        st.error(f"Setup Error: {e}")
# --- 3. MAIN BODY ---
st.title("🚀 SELF-EVOLVING ENGINE")
user_input = st.text_input("Rabbit ko command dein (Hindi/Python/C++):")
# --- Line 28 se check karein ---
if user_input and api_key:
    try:
        # Dekhiye yahan 4 spaces ka gap hai
        with st.spinner("Rabbit dimaag chala raha hai..."):
            response = model.generate_content(user_input)
            if response.text:
                st.markdown(f"<div class='chat-bubble'><b>Rabbit:</b> {response.text}</div>", unsafe_allow_html=True)
            else:
                st.warning("Rabbit ko jawab nahi mila.")
    except Exception as e:
        st.error(f"Brain Error: {e}")
# --- 4. HCS & OFFICE SECTION ---
tabs = st.tabs(["📚 HCS Academy", "📝 Drafting Desk"])
with tabs[0]:
    st.write("76 Sets Database Online.")
with tabs[1]:
    st.write("Architecture Dept Templates Ready.")
