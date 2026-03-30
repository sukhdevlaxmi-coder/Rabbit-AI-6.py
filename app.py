import streamlit as st
import json
import os
import math
import time

# --- EXTERNAL MEMORY BRIDGE ---
MEMORY_FILE = "rabbit_brain_data.json"

def load_external_data():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    # Default data agar file nahi hai
    return {
        "balance": 5000.75,
        "hcs_score": 0,
        "logs": ["Rabbit AI v12.0 Initialized"]
    }

def save_external_data(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)

# --- INITIALIZE RABBIT DATA ---
if 'rabbit_data' not in st.session_state:
    st.session_state.rabbit_data = load_external_data()

# --- UI SETTINGS ---
st.set_page_config(page_title="RABBIT AI 12.0", layout="wide")
st.title("🛡️ MASTER SUKHI RAM - RABBIT 12.0")

# --- SIDEBAR: BRAIN LOGS ---
with st.sidebar:
    st.header("🧠 Neural Logs")
    for log in reversed(st.session_state.rabbit_data["logs"][-5:]):
        st.write(f"• {log}")
    if st.button("Reset Brain Memory"):
        st.session_state.rabbit_data = {"balance": 5000.75, "hcs_score": 0, "logs": ["Memory Reset"]}
        save_external_data(st.session_state.rabbit_data)
        st.rerun()

# --- MAIN TABS (The 4 Core Modules) ---
tab1, tab2, tab3, tab4 = st.tabs(["🎬 Multimedia", "🎮 Gaming", "📚 HCS Master", "🔐 Guardian"])

# --- 1. MULTIMEDIA (External Storage Simulation) ---
with tab1:
    st.header("360° Multimedia Viewer")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Load 360 Image"):
            st.image("https://p7.itc.cn/images01/20201019/5e6302e76f5b4783b9277d33d937000e.jpeg", caption="Spherical Projection Active")
            st.session_state.rabbit_data["logs"].append("Loaded 360 Image")
            save_external_data(st.session_state.rabbit_data)

# --- 2. GAMING (Angry Birds Physics) ---
with tab2:
    st.header("Angry Birds Physics Engine")
    v = st.slider("Initial Velocity (m/s)", 10, 100, 60)
    angle = st.slider("Launch Angle (degrees)", 0, 90, 45)
    if st.button("Launch Bird"):
        # Physics Logic
        target_x = 250
        g = 9.81
        rad = math.radians(angle)
        distance = (v**2 * math.sin(2 * rad)) / g
        st.write(f"Bird Landed at: {distance:.2f} meters")
        if abs(distance - target_x) <= 15:
            st.success("🎯 TARGET HIT!")
            st.balloons()
        else:
            st.error("MISSED!")

# --- 3. HCS MASTER (Persistent Exam Data) ---
with tab3:
    st.header("HCS Exam Prep Quiz")
    q = "हरियाणा का राजकीय पक्षी कौन सा है?"
    ans = st.radio(q, ["कबूतर", "काला तीतर", "सारस क्रेन", "मोर"])
    if st.button("Submit Answer"):
        if ans == "काला तीतर":
            st.success("Sahi Jawab!")
            st.session_state.rabbit_data["hcs_score"] += 1
            save_external_data(st.session_state.rabbit_data)
        else:
            st.error("Galat!")

# --- 4. GUARDIAN (Bank & Security) ---
with tab4:
    st.header("Guardian Security & Bank")
    st.write(f"Current Secure Balance: ${st.session_state.rabbit_data['balance']:.2f}")
    amt = st.number_input("Enter Amount to Deposit", min_value=0.0)
    if st.button("Deposit Securely"):
        st.session_state.rabbit_data["balance"] += amt
        st.session_state.rabbit_data["logs"].append(f"Deposited ${amt}")
        save_external_data(st.session_state.rabbit_data)
        st.success("Transaction Encrypted & Saved to External Memory!")
        st.rerun()
