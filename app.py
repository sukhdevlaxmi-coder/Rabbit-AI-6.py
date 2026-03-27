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
    # --- PURANE CODE KI JAGAH YE DAALEIN ---
if user_input and api_key:
    try:    
        with st.spinner("Rabbit dimaag chala raha hai..."):
            response = model.generate_content(user_input)
            if response.text:
                st.markdown(f"**Rabbit:** {response.text}")
            else:
                st.warning("Rabbit ko koi jawab nahi mila. Dobara koshish karein.")
    except Exception as e:
        st.error(f"Opps! Brain connection mein dikkat hai: {e}")
        st.info("Check karein: 1. API Key sahi hai? 2. Internet chal raha hai?")

# --- 4. HCS & OFFICE SECTION ---
tabs = st.tabs(["📚 HCS Academy", "📝 Drafting Desk"])
with tabs[0]:
    st.write("76 Sets Database Online.")
with tabs[1]:
    st.write("Architecture Dept Templates Ready.")
