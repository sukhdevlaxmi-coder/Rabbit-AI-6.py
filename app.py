import streamlit as st
import time

RABBIT_VERSION = "RABBIT 12.0"

# --- Preserve evolve_rabbit function ---
def evolve_rabbit():
    if 'evolution_stage' not in st.session_state:
        st.session_state.evolution_stage = 1
    
    st.session_state.evolution_stage += 1
    
    # Example: Cycle through a few evolution stages, adjust as needed
    if st.session_state.evolution_stage > 3: 
        st.session_state.evolution_stage = 1 # Reset or cap evolution stages

    st.success(f"Rabbit is evolving to stage {st.session_state.evolution_stage}!")
    time.sleep(1) # Give user a moment to see the success message
    st.rerun()

# --- Preserve Streamlit Page Configuration ---
st.set_page_config(
    page_title="Rabbit AI Interface",
    page_icon="🐰",
    layout="centered", # Can be "wide" or "centered"
    initial_sidebar_state="expanded"
)

# --- Preserve Sidebar Configuration ---
st.sidebar.header("Rabbit AI Controls")
st.sidebar.write(f"Version: {RABBIT_VERSION}")

# Initialize evolution stage if not present
if 'evolution_stage' not in st.session_state:
    st.session_state.evolution_stage = 1

# Display current evolution stage in sidebar
st.sidebar.write(f"Current Stage: {st.session_state.evolution_stage}")

# Placeholder for a Rabbit image (you might want to replace this with a real rabbit image)
# Using a generic placeholder image for now, as specified to preserve structure.
st.sidebar.image("https://www.streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.svg", width=150)

# Evolution button in the sidebar
if st.sidebar.button("Evolve Rabbit"):
    evolve_rabbit()

st.sidebar.write("---")
st.sidebar.info("Use the main area to interact with Rabbit AI!")

# --- Main Application Content (Rewritten as per user instruction) ---
st.title("🐰 Hello from Rabbit AI 12.0!")
st.subheader("Your Friendly Conversational Partner")

st.write("---")

st.write(f"Hello user! I am Rabbit AI {RABBIT_VERSION}. It's nice to hear from you.")

# Acknowledge the "sorry bolo"
st.write("Regarding your 'sorry bolo', please don't worry about it at all! There's no need for apologies here.")
st.write("My purpose is to assist and interact with you in a helpful and friendly way.")

st.info("How can I assist you today? Feel free to ask me anything or tell me what's on your mind.")

st.write("---")
st.caption("Designed with :heart: by Rabbit AI Team")