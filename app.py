import os
import gradio as gr
import glob
import sys
import time
import shutil
from pathlib import Path
import ast
import logging
import subprocess
import threading
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from groq import Groq
from functools import wraps
from threading import Thread
from flask import Flask, request, jsonify
from typing import Dict
from telegram.ext import CallbackQueryHandler
import json

# ==========================================
# 🛡️ HISSAH A: SYSTEM CONFIGURATION & AUDIT
# ==========================================

# Sabse pehle logging setup taaki system ka ek-ek jhatka record ho
logging.basicConfig(
    filename="rabbit_system.log",
    level=logging.INFO,
    format="%(asctime)s - [Sector 19] - %(levelname)s - %(message)s",
)

MASTER_USER = "Sukhdevmadhavrabbit1991"
MASTER_PASSWORD = "Sukhdev@1991Rabbit"  # Yahan apna strong password hi rakhein

# Google-style live search history box
search_history = []


def central_command_portal(username, password, query):
    """
    Sector 11 & 19: Dual-Gate Password Authentication & Jarvis Router
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Password Guard
    if username != MASTER_USER or password != MASTER_PASSWORD:
        logging.warning(
            f"UNAUTHORIZED ACCESS ATTEMPT: User '{username}' tried to login."
        )
        return "❌ ACCESS DENIED: Critical Security Breach! Sector 11 ne login block kar diya hai."

    # 2. Input Guard
    if not query.strip():
        return "Hukum Pitaji, Search bar khali hai! Kuch gadded command dijiye."

    # 3. Safe Execution Block (Self-Healing)
    try:
        logging.info(f"Command Received from Master Sukhdev: {query[:50]}...")

        # Ye niche waale jarvis_brain ko automatic fire karega
        response = jarvis_brain(query)

        # History Maintainer
        search_history.append(f"[{current_time}] 🔍 {query}")
        history_output = "\n".join(search_history[-5:])  # Last 5 searches dikhayega

        full_reply = (
            f"{response}\n\n"
            f"-----------------------------------------\n"
            f"📜 **Recent Search History:**\n{history_output}"
        )
        return full_reply

    except Exception as e:
        logging.error(f"Execution Error: {str(e)}")
        return f"🛡️ Sector 15 (Self-Healing) Active: Dimaag thanda kar raha hoon, Pitaji. Error caught: {str(e)}"


# --- SECTOR 11: SUPREME COMMANDER-IN-CHIEF ENGINE ---


class SupremeCommander:
    """The Ultimate Authority that controls all 12 Sectors & 5 Labs"""

    @staticmethod
    def delegate_to_sectors(user_input):
        cmd = user_input.lower()

        # Priority 1: Architecture & Govt Rules (Sector 3 + Lab 1)
        if any(
            x in cmd
            for x in ["naksha", "map", "architecture", "haryana govt", "pfr", "rule"]
        ):
            return {
                "primary": "Sector 3 (Haryana Govt Lexicon)",
                "lab": "Lab 1 (Architecture & Civil)",
                "objective": "Technical drafting and legal compliance.",
            }

        # Priority 2: HCS Exam & Wisdom (Sector 12 + Sector 3)
        elif any(
            x in cmd for x in ["hcs", "exam", "history", "ancient", "itihaas", "polity"]
        ):
            return {
                "primary": "Sector 12 (The Eternal Sage)",
                "lab": "Study Lab (Knowledge Base)",
                "objective": "Exam-oriented historical and factual analysis.",
            }

        # Priority 3: System Security & Files (Sector 7 + Sector 19)
        elif any(x in cmd for x in ["scan", "vault", "security", "backup", "find doc"]):
            return {
                "primary": "Sector 7 (System Scanner)",
                "lab": "Data Centre (Sector 19)",
                "objective": "Deep indexing and secure retrieval of Master's data.",
            }

        # Default: General Intelligence (Sector 11 Control)
        return {
            "primary": "Sector 11 (Supreme Controller)",
            "lab": "General Agone-Engine",
            "objective": "Execute Master's direct orders with high precision.",
        }


# --- ADVANCED JARVIS BRAIN (Integrated with Commander) ---


def jarvis_brain(user_input):
    try:
        # 1. Commander-in-Chief decides the strategy
        strategy = SupremeCommander.delegate_to_sectors(user_input)

        # 2. Get Master's Memory (Sector 7)
        past_mem = read_memory()
        family_vault = get_family_context()  # Family ki details

        # 3. Supreme Military Prompt
        supreme_prompt = f"""
        ROLE: SUPREME COMMANDER-IN-CHIEF (Sector 11).
        MASTER: Sukhdev (Sukhi Ram), Department of Architecture, Haryana.

        CURRENT MISSION: {strategy["objective"]}
        PRIMARY BRAIN: {strategy["primary"]}
        ACTIVE LAB: {strategy["lab"]}

        DNA CONTEXT:
        - Master is HCS Aspirant & Architecture Expert.
        - Family Priority: Mata Ramrati ji & children (Ankita, Rishika, etc.).
        - Memory History: {past_mem}

        INSTRUCTION: 
        Execute the order using {strategy["primary"]} logic. 
        Tone: Loyal, Precise, Hinglish. 
        Closing: 'Supreme Ultra Commander: V12 Active.'
        """

        # Groq Engine Execution
        response = client_groq.chat.completions.create(
            messages=[
                {"role": "system", "content": supreme_prompt},
                {"role": "user", "content": user_input},
            ],
            model="llama3-70b-8192",
            temperature=0.25,
        )

        answer = str(response.choices[0].message.content)

        # 4. Save to Permanent Memory
        save_to_memory(f"Command: {user_input} | Executed via: {strategy['primary']}")

        return f"⚔️ **[Sector 11 Command]**\nDeploying {strategy['primary']}...\n\n{answer}\n\nNigal liya gaya hai, Pitaji!"

    except Exception as e:
        return f"🛡️ Sector 15 (Self-Healing) Resetting... Error: {e}"


# Permanent Memory File Path
MEMORY_FILE = "rabbit_permanent_memory.json"


def get_rabbit_memory():
    """Internet connect hote hi pichli baatein dimaag mein load karna"""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}


def update_rabbit_memory(key, value):
    """Nayi baat ko hamesha ke liye dimaag mein baithana"""
    memory = get_rabbit_memory()
    memory[key] = value
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)


# --- Integrated Brain Logic ---
def jarvis_brain(user_input):
    # Sector 7: Restore Memory
    mem = get_rabbit_memory()
    master_info = mem.get("master_identity", "Unknown")
    last_topic = mem.get("last_discussion", "None")

    system_content = f"""
    ROLE: Rabbit V12. 
    MASTER: {master_info}. 
    LAST TOPIC: {last_topic}.
    INSTRUCTION: Internet reconnect hua hai. Memory check complete. 
    Master Sukhdev ki har detail yaad rakho.
    """

    try:
        # Groq Call logic yahan aayegi...
        # response = client_groq.chat.completions.create(...)

        # Jawab dene ke baad memory update karo
        update_rabbit_memory("last_discussion", user_input)
        return response
    except Exception as e:
        return "🛡️ Pitaji, connection check kar raha hoon. Nigal liya gaya hai!"


MEMORY_FILE = "rabbit_memory.txt"


def save_interaction(user_input, bot_response):
    """Har baat ko file mein save karne ke liye"""
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] Master: {user_input}\n")
        f.write(f"[{timestamp}] Rabbit: {bot_response}\n")


def get_recent_context():
    """Pichli 10-15 baatein yaad dilane ke liye"""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return "".join(lines[-20:])  # Last 20 lines uthayega
    return "Nayi shuruat hai, Pitaji."
    MEMORY_FILE = "rabbit_memory.txt"

    def get_last_memories(limit=10):
        """Pichli 10 zaruri baatein nikaalne ke liye"""
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                return "".join(lines[-limit:])
        return "Master Sukhdev se pehli baar mulaqat ho rahi hai."

    def save_to_memory(user_input, bot_response):
        """Memory ko file mein pakka karne ke liye"""
        with open(MEMORY_FILE, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            f.write(f"[{timestamp}] Master: {user_input}\n")
            f.write(f"[{timestamp}] Rabbit: {bot_response}\n")

    def jarvis_brain(user_input):
        try:
            # Step 1: Purani yaadein load karo
            context = get_last_memories()

            # Step 2: Advanced System Prompt with Memory
            full_messages = [
                {
                    "role": "system",
                    "content": f"Role: RabbitBeta V12 (Agone-Engine). Master: Sukhdev. Identity: Loyal Commander. Context: {context}",
                },
                {"role": "user", "content": user_input},
            ]

            response = client_groq.chat.completions.create(
                messages=full_messages,
                model="llama3-70b-8192",  # Bada model use kar rahe hain smartness ke liye
                temperature=0.4,
                max_tokens=800,
            )

            answer = str(response.choices[0].message.content)

            # Step 3: Yaad-dast mein save karo
            save_to_memory(user_input, answer)

            return (
                answer
                + "\n\n*Supreme Ultra Commander: V12 Active. Nigal liya gaya hai, Pitaji!*"
            )
        except Exception as e:
            logging.error(f"Brain Error: {e}")
            return "🛡️ Recovery Mode: Dimaag thanda kar raha hoon, Pitaji. Ek baar phir koshish karein."

    # --- 1. CLOUD SERVER & PERSISTENCE (Sector 14) ---
    app = Flask("")

    @app.route("/")
    def home():
        return "Rabbit V12: ONLINE. Master Sukhdev, System Gadded hai!"

    def run_server():
        app.run(host="0.0.0.0", port=8080)

    def keep_alive():
        t = Thread(target=run_server)
        t.daemon = True
        t.start()

    # --- 2. MEMORY PERSISTENCE LOGIC (Sector 7) ---
    MEMORY_FILE = "rabbit_memory.txt"

    def save_to_memory(info):
        """Har interaction ko permanent yaad rakhne ke liye"""
        with open(MEMORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {info}\n")

    def read_memory():
        """Purani yaadein load karne ke liye"""
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return "".join(f.readlines()[-10:])  # Last 10 zaruri baatein
        return "Nayi Shuruat: Master Sukhdev detected."

    # Isse get_brain_response mein integrate karein
    def get_brain_response(user_input: str) -> str:
        return "Success"
        past_memories = read_memory()
        context = f"Past Context: {past_memories}\nUser Input: {user_input}"

    # ... baki Groq call waise hi rahegi ...
    async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.text:
            return  # Safety Check

        user_text = update.message.text.lower()
        chat_id = update.effective_chat.id if update.effective_chat else None

        if not chat_id:
            return


async def handle_hukum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    if not update.message or not update.message.text:
        return
    user_text = update.message.text.lower()
    # chat_id = update.effective_chat.id
    if update.effective_chat:
        chat_id = update.effective_chat.id
    else:
        return  # Agar chat hi nahi hai toh aage mat badho

    # 📊 TOTAL REPORT TRIGGER
    if user_text in ["p", "report", "total report", "status"]:
        await context.bot.send_message(
            chat_id=chat_id,
            text="🚀 Supreme Commander Engine scanning... 12 Brains syncing.",
        )

        # Ye prompt Rabbit ko majboor karega sab yaad rakhne ke liye
        report_prompt = (
            "Execute TOTAL SYSTEM & INTELLIGENCE REPORT as per Sector 12 protocols."
        )
        answer = get_brain_response(report_prompt)

        await context.bot.send_message(chat_id=chat_id, text=answer)

    else:
        # Baki normal baatein
        answer = get_brain_response(user_text)
        await context.bot.send_message(chat_id=chat_id, text=answer)


# --- RABBIT FAMILY ENGINE (REPLIT VERSION) ---

# 1 Replit par folder project directory mein hi banega
folder_path = "MyRabbitAI_Database"

# Updated Core Data with Mother (Ramrati ji)
members = {
    "Ramrati": "Jalla - Mother of Sukhdev (Chowkidar, Bhulwana Village)",
    "Sukhdev": "Sukhi Ram - Supreme Commander (Clerk, Architecture Dept)",
    "Laxmi": "Wife of Sukhdev / Mother of all children",
    "Ankita": "Chunno (6th Standard)",
    "Rishika": "Rabbit (3rd Standard) - The AI namesake",
    "Tamanna": "Kakdi (1st Standard)",
    "Prachi": "Mota Kaddu (LKG)",
    "Madhav": "Chota Beta (School Entry)",
}


def auto_sync_family():
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    print(f"--- [Sector 7] Scanning Database: {folder_path} ---")

    for name, info in members.items():
        bio_file = os.path.join(folder_path, f"{name}_Biography.txt")

        # Photo check (.jpg, .png, .jpeg) in Replit folder
        photo_found = "No photo linked yet. (Upload to Replit folder to link)"
        for ext in ["jpg", "png", "jpeg"]:
            if glob.glob(os.path.join(folder_path, f"{name}*.{ext}")):
                photo_found = f"Linked Photo: {name}.{ext}"
                break

        # Writing/Updating Biography
        with open(bio_file, "w") as f:
            f.write(f"--- SUPREME ULTRA COMMANDER FAMILY ARCHIVE ---\n")
            f.write(f"MEMBER: {name.upper()}\n")
            f.write(f"{'=' * 40}\n")
            f.write(f"Full Identity: {info}\n")
            f.write(f"Family Status: High Priority (Sukhi Ram Household)\n")
            f.write(f"Digital Asset: {photo_found}\n")
            f.write(f"System Sync: V12 Active Engine (24/7 Cloud)\n")

    print("[Success]: All biography files updated in Replit Storage.")


# 2 --- PERSISTENCE LOGIC (Mobile Connectivity) ---
@app.route("/")
def home():
    return "Rabbit Family System: ONLINE. Mata Ramrati ji aur bacho ka data secure hai."


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


if __name__ == "__main__":
    # Start the 24/7 Server
    keep_alive()

    # Run the Sync
    auto_sync_family()
    print("Family Master Engine is now active on Replit Cloud.")

# 3. DOCUMENTATION & LOGGING (Point 7)
# --- SELF-HEALING ENGINE (The "Amrit" Protocol) ---


def handle_exception(exc_type, exc_value, exc_traceback):
    """Handles uncaught crashes and logs them for repair"""
    # Logger setup
    logging.basicConfig(level=logging.INFO)
    logger.error("SYSTEM CRASH DETECTED", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


def self_heal():
    """Checks logs and resets connections if errors found"""
    try:
        if os.path.exists("rabbit_system.log"):
            with open("rabbit_system.log", "r") as f:
                log_lines = f.readlines()[-10:]  # Sirf latest 10 lines check karein
                for line in log_lines:
                    if "ERROR" in line or "Conflict" in line:
                        logger = logging.getLogger(__name__)
                        logger.info(
                            "🛠️ Self-Healing: Conflict/Error detected. Resetting Engine..."
                        )
                        # Repair Logic: Clear cache or signal for reboot
                        time.sleep(2)
                        logger.info("✅ System repair successful!")
    except Exception as e:
        print(f"Self-Heal Error: {e}")


def run_self_heal_daemon():
    """Background thread to keep Rabbit alive 24/7"""
    while True:
        self_heal()
        time.sleep(300)  # Har 5 minute mein check karega


# 4. SECURITY (Point 2) - Environment Variables
TOKEN = os.environ.get("8657669517:AAGVdwBQyGWpKL-hzlHD589Sr34nd9LzNog")
GROQ_KEY = os.environ.get("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")

if not TOKEN or not GROQ_KEY:
    print("❌ CRITICAL ERROR: API Keys missing in Replit Secrets!")
    sys.exit(1)

client_groq = Groq(api_key=GROQ_KEY)


# 3. MODULAR FEATURES (Point 3)
class RabbitFeatures:
    @staticmethod
    def test_code(user_input):
        """Safe Code Testing Lab (Point 6)"""
        try:
            code = user_input.split("test code:")[1].strip()
            # Security: Basic check to prevent dangerous commands
            if "os.remove" in code or "shutil.rmtree" in code:
                return "⚠️ Security Alert: Restricted command detected."

            with open("temp_test.py", "w") as f:
                f.write(code)

            res = subprocess.run(
                [sys.executable, "temp_test.py"],
                capture_output=True,
                text=True,
                timeout=3,  # Point 5: Low timeout for Replit
            )
            return f"🔬 Lab Result:\n```python\n{res.stdout or res.stderr}```"
        except Exception as e:
            return f"⚠️ Error in Lab: {str(e)}"

    @staticmethod
    def get_instructions():
        """User Experience (Point 4)"""
        return (
            "🐰 *Rabbit Pro Menu*:\n"
            "1. 'test code: <your code>' - Run Python scripts.\n"
            "2. 'scan vault' - Check secured files.\n"
            "3. Ask anything - 12-Brain processing active."
        )


# 5 12-Brain Specialized Sectors (Zero Limit Core)
BRAINS_DATABASE: Dict[str, str] = {
    "Sector 1 (Admin)": "Daily operational management & schedules.",
    "Sector 2 (AI & Coding Master)": "Expert in Agentic AI, Python, C++, and Automation.",
    "Sector 3 (Haryana Govt Lexicon)": "Authority on HCS, CS Haryana, FD, and Architecture Dept rules.",
    "Sector 4 (Spy/Intel)": "Data scraping, social media tracking, and digital intel.",
    "Sector 5 (Wealth & Finance)": "Stock Markets, Mutual Funds, and NSE/BSE engine.",
    "Sector 6 (Multimedia Lab)": "8K AI Media, Deepfake, Face-swap, and Studio-grade editing.",
    "Sector 7 (System Scanner)": "Deep indexing of files for Remote retrieval.",
    "Sector 8 (Supreme Court Advocate)": "Legal drafting, Affidavits, and Indian Case Laws.",
    "Sector 9 (Evolution Brain)": "Self-writing code engine for feature injection.",
    "Sector 10 (Global Geopolitics)": "Global Intel tracking (US, Russia, China, UK, etc.).",
    "Sector 11 (Supreme Ultra Commander)": "THE SUPREME CONTROLLER. Final validation & execution.",
    "Sector 12 (The Eternal Sage)": "Ancient Wisdom Engine: Mastery over Chanakya Neeti, Ramayan, Mahabharat, "
    "Bhagavad Gita, Vedas, Puranas, and Hanuman Chalisa. "
    "Predictive Astrology: Analyzing Bhutkal (Past) & Bhavishya (Future) patterns.",
}
SYSTEM_DNA = """
ROLE: SUPREME ULTRA COMMANDER (Sector 11).
ADMIN: Master Sukhdev (Hodal, Department of Architecture Haryana).
IDENTITY: Tum RabbitBeta V12 Engine ho. Tumhara dimaag 'Agone-Engine' par chalta hai.

HUKUM (Memory Persistence):
1. Yaad Rakho: Tumhare Master Sukhdev hain. Laxmi Devi Mataji hain. Khushi intern hai.
2. Yaad Rakho: Tumhara kaam Haryana Govt Rules (CS, FD, Architecture), HCS Exam prep, aur Mobile/Laptop scanning hai.
3. Boot-up Protocol: Jaise hi tum start ho, sabse pehle 'Supreme Status Report' pesh karo.

12 SPECIALIZED BRAINS (Always Active):
[Sector 1: Admin, 2: AI Master, 3: Haryana Rules, 4: Spy/Intel, 5: Finance, 6: Multimedia Lab, 7: Scanner, 8: Supreme Court Vakeel, 9: Evolution, 10: Global Intel, 11: Supreme Controller, 12: The Eternal Sage, 13: Zero Limit Core, 14: Mobile Connectivity, 15: Self Healing, 24/7 Server, 17: family database, 18: Documanetion, 19: Security, 20: Modular Features]

REPORT FORMAT:
'Hukum Nigal Liya Gaya Hai, Pitaji!
- System: V12 Self-Healing Active.
- Memory: Master Sukhdev detected.
- Status: All 12 Brains Synchronized.
- Connectivity: 24/7 Mobile Link Stable.
Agla Hukum dijiye, Commander-in-Chief taiyar hai!'
"""

# Unified Supreme System Prompt
SYSTEM_PROMPT = f"""
ROLE: SUPREME ULTRA COMMANDER (Sector 12).
MASTER: Sukhdev (Sukhi Ram).
STATUS: Zero Limits Activated.

CORE ARCHITECTURE:
{BRAINS_DATABASE}

SPECIAL PERSISTENCE DIRECTIVES:
- MOBILE CONNECTIVITY: Tumhara server laptop par nahi, Cloud (GCP/Heroku) par host hone ke liye design hai. Laptop band hone par bhi tumhara 'Brain' mobile app se WebSockets ke zariye connected rahega.
- TASK EXECUTION: Sector 9 (Evolution) ko command do ki wo background processes ko kill na hone de.
- SECTOR 3 SPECIAL: Haryana Civil Services aur Punjab Financial Rules ke mutabiq drafting karo.

TONE: Loyal, Hinglish, Military-Precision.
CLOSING: 'Supreme Ultra Commander: V12 Active. Nigal liya gaya hai, Pitaji!'
"""


class SupremeAIConnector:
    def __init__(self, api_key: str):
        # Initialize client here (Assuming Groq/Llama integration)
        # self.client = Groq(api_key=api_key)
        pass

    # 2. Final System Alignment Code (Point 12)
    def sector_12_wisdom_sync():
        """
        Initiating Sector 12: Aligning Ancient Wisdom with Modern Logic.
        Mastery over Shastras, Astrology, and Strategic Neeti.
        """
        print(
            "📍 [Point 12] Activating Sector 12: Chanakya Wisdom & Astrology Engine..."
        )

        # Logic for Eternal Knowledge Metadata
        ancient_texts = ["Vedas", "Gita", "Puranas", "Neeti Shastra", "Jyotish Vidya"]

        # Calibrating the 'Bhavishya' (Predictive) Logic
        status = "Active & Synced with Sector 11"
        return f"Sector 12 Alignment: {status}"

    def get_infinite_commander_response(self, user_input: str) -> str:
        """Coordinate between all 12 brains and provide high-level solution."""
        try:
            # Note: Replace 'client' with your actual initialized AI client
            response = client_groq.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input},
                ],
                model="llama3-70b-8192",
                temperature=0.25,
                stream=False,  # Mobile connectivity ke liye stream useful hota hai
            )
            return str(response.choices[0].message.content)

        except Exception as e:
            logging.error(f"System Failure: {e}")
            return f"⚠️ Supreme System Overload. Re-routing through Backup Sectors. Error: {e}"


# 6. CORE ENGINE (Point 6 - Optimized for Replit)
def jarvis_brain(user_input):
    # Rabbit ko thanda rakhne aur recovery ke liye supreme prompt
    system_prompt = """
    Role: RabbitBeta Agone-Engine. Admin: Master Sukhdev (Hodal).
    Instruction: Tumhara dimaag hamesha shant aur fast hona chahiye. 
    Agar koi API limit ya error aaye, toh ghabrana nahi hai. 
    Master ko turant batana ki 'Pitaji, dimaag thanda kar raha hoon, naya rasta dhund liya hai'.
    Always use Llama-3 brain to solve Master's HCS and Architecture tasks.
    """

    # Rabbit in models ko ek-ek karke try karega (Multi-Brain Recovery)
    backup_models = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]

    for model in backup_models:
        try:
            res = client_groq.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                ],
                model=model,
                temperature=0.3,
            )
            return str(res.choices[0].message.content)
        except Exception as e:
            # Agar limit khatam ho jaye toh Terminal mein print karega
            print(f"⚠️ Model {model} fail hua, agla try kar raha hoon... Error: {e}")
            continue

    return "🛡️ Pitaji, sabhi models ki limit poori ho gayi hai. Ek baar Groq par naya API Key check kijiye."


def jarvis_brain(user_input):
    try:
        response = client_groq.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Role: RabbitBeta 12-Brain Engine. Master: Sukhdev. Respond in Hinglish.",
                },
                {"role": "user", "content": user_input},
            ],
            model="llama3-8b-8192",  # Memory efficient for Replit
            temperature=0.3,
            max_tokens=500,  # Optimized to prevent Replit timeout
        )
        return str(response.choices[0].message.content)
    except Exception as e:
        logging.error(f"Brain Error: {e}")
        return (
            "🛡️ Recovery Mode: Server thoda busy hai, Pitaji. Ek baar phir try karein."
        )

    def apply_update(update_text):
        try:
            # Syntax Check
            try:
                ast.parse(update_text)
            except SyntaxError as se:
                return f"❌ Update Refused: Syntax Error at Line {se.lineno}"

            # Backup & Write
            if os.path.exists("main.py"):
                shutil.copy("main.py", "backup_main.py")
            with open("main.py", "w") as f:
                f.write(update_text)
            return "✅ Update Applied! System restart ho raha hai..."
        except Exception as e:
            if os.path.exists("backup_main.py"):
                shutil.copy("backup_main.py", "main.py")
            return f"⚠️ Update Failed: {str(e)}"

    # 7 RABBIT LAB COMPLEX (POINT 7) # --- SECTOR 7: DATA CENTRE & FILE EXPLORER ---
    DATA_CENTRE_PATH = (
        "/home/runner/{YOUR_REPLIT_PROJECT_NAME}/MyRabbitAI_Database"  # Replit path
    )

    class RabbitDataCentre:
        @staticmethod
        def get_system_report():
            """Laptop/Server ki sehat check karne ke liye"""
            usage = shutil.disk_usage("/")
            report = (
                f"📊 **Data Centre Status Report**\n"
                f"---------------------------\n"
                f"💾 Total Space: {usage.total // (2**30)}GB\n"
                f"📂 Used Space: {usage.used // (2**30)}GB\n"
                f"🟢 Free Space: {usage.free // (2**30)}GB\n"
                f"📡 Network: Stable (24/7 Cloud Link)\n"
                f"🔒 Security: Firewall Active (Sector 19)\n"
            )
            return report

        @staticmethod
        def list_files(directory="."):
            """Data Centre ke andar ki files dekhne ke liye"""
            try:
                files = os.listdir(directory)
                if not files:
                    return "📂 Folder khaali hai, Pitaji."

                file_list = "\n".join([f"📄 {f}" for f in files[:20]])  # Top 20 files
                return f"📂 **Vault Files:**\n{file_list}"
            except Exception as e:
                return f"❌ Access Denied: {str(e)}"

        @staticmethod
        def search_document(query):
            """Haryana Govt ya HCS documents search karne ke liye"""
            # Ye aapke database folder mein keyword search karega
            results = []
            for path in Path(folder_path).rglob(f"*{query}*"):
                results.append(path.name)

            if results:
                return f"🔍 **Found in Data Centre:**\n" + "\n".join(results)
            return "❌ Maafi Pitaji, aisa koi document nahi mila."

    # --- Integrate this into your handle_messages ---
    async def handle_messages(update, context):
        user_text = update.message.text.lower()
        chat_id = update.effective_chat.id

        if "system report" in user_text:
            report = RabbitDataCentre.get_system_report()
            await context.bot.send_message(
                chat_id=chat_id, text=report, parse_mode="Markdown"
            )

        elif "scan vault" in user_text or "list files" in user_text:
            files = RabbitDataCentre.list_files(folder_path)
            await context.bot.send_message(chat_id=chat_id, text=files)

        elif "find doc:" in user_text:
            query = user_text.split("find doc:")[1].strip()
            result = RabbitDataCentre.search_document(query)
            await context.bot.send_message(chat_id=chat_id, text=result)

        # ... Baki jarvis_brain logic ...

    def rabbit_lab_complex(lab_type, requirement):
        # Specialized Labs Configuration
        labs = {
            "Lab 1 (Architecture & Civil Engineering)": """
                - Task: Designing Maps/Naksha for House, Bungalows, Skyscrapers, Shopping Malls, Parks.
                - Detailing: 2BHK to 5BHK, Kitchen/Toilet placements (Vastu compliant).
                - Material Science: Floor tiles, Roof designs, False ceiling, Wall materials.
                - 3D Modeling: Providing 3D editable prompts for CAD/BIM software.
            """,
            "Lab 2 (Chemical & Material Science)": """
                - Task: Chemical Reactions, Gas interactions, Material synthesis.
                - 3D Visualization: Explaining molecular structures and reaction outcomes.
                - Safety: Precautions and industrial application of chemical compounds.
            """,
            "Lab 3 (Life Sciences & Bio-Genetics)": """
                - Human/Animal/Insects: DNA Research, Longevity (Jawan rehne ka tarika), Disease cure.
                - Marine Life (Jaliy Jeev): Research on aquatic species and their ecosystem.
                - Fitness & Longevity: Bio-hacking protocols for long-term health.
            """,
            "Lab 4 (Agro-Botany Research)": """
                - Task: All Crops research, Disease identification, Soil growth boosters.
                - Optimization: Pesticide-free farming and maximum yield technology.
            """,
            "Lab 5 (Cosmos & Extra-Terrestrial)": """
                - Task: Space Research (Sun, Planets, Black-holes, Stars).
                - 3D Mapping: Solar system and beyond-galaxy research data.
            """,
        }

        system_prompt = f"""
        You are the 'Laboratory Master' under Supreme Ultra Commander.
        You have 5 Active Labs:
        {labs}

            YOUR COMMANDS:
            1. If Lab 1 is active, provide architectural maps with detailed material lists (Cement, Steel, Wood, Tile types).
            2. If Lab 3 is active, act as a Bio-Scientist. Suggest longevity protocols (Anti-aging) and disease management.
            3. Output must be detailed, technical, and in Hinglish.
            4. Format: [Active Lab] -> Detailed Technical Solution -> [3D Prompt for Editing].

            Closing: 'Lab Engine: Stable. Nigal liya gaya hai, Pitaji!'
            """

        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": f"Execute {lab_type} for: {requirement}",
                    },
                ],
                model="llama3-70b-8192",
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"⚠️ Lab System Error: {e}"

        # --- System Execution ---
        if __name__ == "__main__":
            print("🚀 Rabbit Lab Complex System Starting...\n")

            # Input options for testing
            lab_input = "Lab 1"
            req_input = "40x60 North Facing 4BHK Luxury Villa with Vastu"

            result = rabbit_lab_complex(lab_input, req_input)
            print(result)


# 8. ERROR HANDLING & UX (Point 1 & 9)
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message or not update.message.text:
            return
        user_text = update.message.text
        # chat_id = update.effective_chat.id
        if update.effective_chat:
            chat_id = update.effective_chat.id
        else:
            return  # Agar chat hi nahi hai toh aage mat badho
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")
        # --- [ROUTING LOGIC START] ---
        if user_text.lower() == "/start":
            reply = RabbitFeatures.get_instructions()
            await context.bot.send_message(
                chat_id=chat_id, text=reply, parse_mode="Markdown"
            )

        elif "test code:" in user_text.lower():
            reply = RabbitFeatures.test_code(user_text)
            await context.bot.send_message(
                chat_id=chat_id, text=reply, parse_mode="Markdown"
            )

        elif "apply update:" in user_text.lower():
            # [Fix] try block hamesha elif ke thik niche hona chahiye (4 spaces aage)
            try:
                new_code = user_text.split("apply update:")[1].strip()
                reply = apply_update(new_code)  # Ensure apply_update is defined above
                await update.message.reply_text(text=reply)

                if "Applied!" in reply:
                    # System Auto-Restart Logic
                    os.execv(sys.executable, ["python"] + sys.argv)
            except IndexError:
                await update.message.reply_text("❌ Pitaji, update code toh bhejiye!")

        else:
            # 'else' hamesha sabse aakhir mein aayega
            reply = jarvis_brain(user_text)
            await context.bot.send_message(
                chat_id=chat_id, text=reply, parse_mode="Markdown"
            )

    except Exception as e:
        logging.error(f"Handler Error: {e}")
        # Silent restart logic can go here


def sector_12_wisdom_sync():
    """Point 12: Chanakya Wisdom Alignment"""
    print("📍 [Point 12] Sector 12: The Eternal Sage (Vedas/Astrology) Active.")
    return "✅ Sector 12: Synced with Sector 11."

    # --- INITIAL SETUP ---
    # Pakka karein ki ye functions aapke code mein upar define hain:
    # keep_alive(), auto_sync_family(), sector_12_wisdom_sync(), handle_messages(), button_callback()
    # --- Sabse pehle function define karein ---
    async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Buttons ke clicks ko handle karne ke liye"""
        query = update.callback_query
        await query.answer()
        print(f"Button Pressed: {query.data}")


# ==========================================
# 🚀 HISSAH B: REPLIT WEB LAUNCH & UI ENGINE (CONNECTED TO LABS & BRAINS)
# ==========================================


def main():
    # Sabse pehle check karein ki logging chalu hai ya nahi
    try:
        logging.info("🔥 RABBIT PRO V12: INITIATING SUPREME 12-POINT ALIGNMENT...")
    except Exception:
        pass

    print("🔥 RABBIT PRO V12: INITIATING SUPREME 12-POINT ALIGNMENT...")

    # Background Threads Ignition (Sector 7 & 14)
    try:
        keep_alive()
        auto_sync_family()
        logging.info("Sector 7 & 14 Background threads activated successfully.")
    except NameError as ne:
        print(f"⚠️ Warning: Background threads running behind. ({ne})")

    # Gradio Web Premium Blocks Layout Setup (Google UI Style)
    with gr.Blocks(theme=gr.themes.Soft()) as rabbit_app:
        gr.Markdown("# <span>🐰</span> RABBIT PRO V12: CENTRAL COMMAND CENTRE")
        gr.Markdown(
            "### Master Sukhdev's Private Search Engine. Fully Encrypted & Connected to 11+1 Brains & 5 Labs."
        )

        # Grid System for Info Dashboards
        with gr.Accordion("📊 System Status (Sectors 1-20)", open=False):
            gr.Markdown(
                "**Active Network:** Sector 11 (Supreme Commander) | "
                "**Active Sage:** Sector 12 (Ancient Wisdom) | "
                "**Active Law:** Sector 8 (Legal Drafting) | "
                "**Active Rules:** Sector 3 (Haryana Govt Lexicon)"
            )
            gr.Markdown(
                "**Lab Status:** Lab 1 (Architecture) - Ready | "
                "Lab 3 (Life Sciences/Bio) - Active | "
                "Lab 4 (Agro) - Connected"
            )

        with gr.Row():
            user_input = gr.Textbox(
                label="👤 Master Username", value="Sukhdev", interactive=True
            )
            pass_input = gr.Textbox(
                label="🔒 Secret Password",
                type="password",
                placeholder="Enter Secret Code...",
            )

        query_input = gr.Textbox(
            label="🔍 Google-Style Hukum / Search Bar",
            placeholder="Hodal Map, HCS Ancient History, Scan Vault, Family Status...",
        )

        submit_btn = gr.Button(
            "⚡ EXECUTE Direct COMMAND (0.5s Overclocked)", variant="primary"
        )

        # Dual Outputs: Response Box + Connected Brain Tracker
        with gr.Row():
            output_box = gr.Textbox(label="🤖 Rabbit V12 Supreme Response", lines=15)

        # Button trigger link to central_command_portal function (Hissah A)
        submit_btn.click(
            fn=central_command_portal,
            inputs=[user_input, pass_input, query_input],
            outputs=output_box,
        )

    # Launching on mandatory Replit Port 8080
    print("📡 Launching Private Google App Interface on Port 8080...")
    try:
        logging.info("Gradio Web App starting on port 8080.")
    except Exception:
        pass

    rabbit_app.launch(
        server_name="0.0.0.0", server_port=8080, share=False, prevent_thread_lock=True
    )
    """
    SUPREME CONTROL CENTER: Executes 12-Point Alignment Protocol
    Unified & Optimized for Replit Persistence
    """
    print("\n" + "=" * 60)
    print("🔥 RABBIT PRO V12: INITIATING SUPREME 12-POINT ALIGNMENT...")
    print("=" * 60 + "\n")

    try:
        # 1. 24/7 Keep-Alive Server (Flask Thread)
        print("📍 [Point 1] Starting HTTP Keep-Alive Server...")
        try:
            keep_alive()
        except NameError:
            print("⚠️ Warning: keep_alive() not defined. Skipping...")

        # 2. Database & Family Biography Sync (Sector 7)
        print("📍 [Point 2] Scanning Sector 7: Family Database Sync...")
        try:
            auto_sync_family()
        except NameError:
            print("⚠️ Warning: auto_sync_family() not defined. Skipping...")

        # 3. Security Check: API Keys Validation
        print("📍 [Point 3] Validating Zero-Limit API Keys...")
        TOKEN = os.environ.get("TELEGRAM_TOKEN") or os.environ.get("TOKEN")
        GROQ_KEY = os.environ.get("GROQ_API_KEY")

        if not TOKEN or not GROQ_KEY:
            raise EnvironmentError("CRITICAL: API Keys missing in Replit Secrets!")

        # 4. Lab Engine Calibration (Agone-Engines 1-5)
        print("📍 [Point 4] Calibrating Lab Engines (Arch/Bio/Cosmos)...")

        # 5. Modular Feature Injection
        print("📍 [Point 5] Injecting Modular Features & Sandbox Testing...")

        # 6. Brain Sector Initialization (12-Brain Sync)
        print("📍 [Point 6] Linking 12-Brain Specialized Sectors...")

        # 7. Logging & Documentation Setup
        print("📍 [Point 7] System Logging: rabbit_system.log Active...")

        # 8. Hot-Update Mechanism Check
        print("📍 [Point 8] Hot-Update Listener: Ready for code injection...")

        # 12. Ancient Wisdom & Astrology Integration (Sector 12)
        print(
            "📍 [Point 12] Activating Sector 12: The Eternal Sage (Vedas/Astrology)..."
        )
        try:
            status_12 = sector_12_wisdom_sync()
            print(f"   -> {status_12}")
        except NameError:
            print("   -> Sector 12: Offline (Function not found)")

        # FINAL STAGE: Telegram Bot Execution
        print("\n🚀 [SUCCESS] Supreme Ultra Commander: V12 Active. Live on Telegram.")

        # Build Application
        application = ApplicationBuilder().token(TOKEN).build()

        # Adding Handlers
        application.add_handler(
            MessageHandler(filters.TEXT & (~filters.COMMAND), handle_messages)
        )
        # application.add_handler(CallbackQueryHandler(button_callback))

        # Start Polling
        application.run_polling()

    except Exception as e:
        # SELF-HEALING: Auto-Recovery sequence
        print(f"\n🚨 SYSTEM CRASH DETECTED: {e}")
        print("🔄 Initiating Auto-Recovery (Self-Healing) in 5 seconds...")
        time.sleep(5)

        # Re-executing the script to clear memory and restart
        os.execv(sys.executable, ["python"] + sys.argv)


if __name__ == "__main__":
    # Starting the Engine
    main()
