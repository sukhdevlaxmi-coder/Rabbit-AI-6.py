import streamlit as st
import google.generativeai as genai
import base64
import requests

# --- BASIC CONFIG ---
st.set_page_config(page_title="RABBIT 11.0 - SELF-EVOLVER", layout="wide")

# --- SIDEBAR: CORE SETTINGS ---
with st.sidebar:
    st.title("🐰 RABBIT CORE")
    st.markdown("---")
    # Yahan apni keys bharein
    gemini_key = st.text_input("Gemini API Key:", type="password")
    github_key = st.text_input("GitHub Token (PAT):", type="password")
    
    # Aapki Repository Details
    repo_owner = "sukhdevlaxmi-coder"
    repo_name = "Rabbit-AI-6"
    file_path = "Rabbit-AI-6.py" 

    if gemini_key and github_key:
        try:
            genai.configure(api_key=gemini_key)
            # Latest stable model for automation
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            st.success("Brain & Hands Active! ✅")
        except Exception as e:
            st.error(f"Setup Error: {e}")

# --- FUNCTION: THE SELF-EVOLUTION ENGINE ---
def evolve_rabbit(new_code):
    try:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        headers = {"Authorization": f"token {github_key}"}
        
        # 1. Purani file ka SHA hash lena (Update ke liye zaroori hai)
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            sha = res.json()['sha']
            # 2. Naye code ko Base64 mein badalna
            encoded_content = base64.b64encode(new_code.encode()).decode()
            data = {
                "message": "Rabbit Evolution: Automatic Self-Update",
                "content": encoded_content,
                "sha": sha
            }
            # 3. GitHub par naya code Push (Update) karna
            put_res = requests.put(url, headers=headers, json=data)
            return put_res.status_code
        else:
            return res.status_code
    except Exception as e:
        return str(e)

# --- MAIN INTERFACE ---
st.title("🚀 RABBIT AUTO-EVOLUTION MODE")
st.info("Sukhi Ram ji, Rabbit ab khud code likhega aur khud ko update karega!")

# Instruction Box
instruction = st.text_area("Rabbit ko kya naya sikhna ya badalna hai?", 
                          placeholder="Example: Background light blue karo aur 'Python Lesson 1' ka button banao.")

if st.button("EXECUTE EVOLUTION"):
    if instruction and gemini_key and github_key:
        with st.spinner("Rabbit apna naya roop (Code) likh raha hai..."):
            try:
                # Rabbit ko instruction: Pura code wapas likho naye feature ke saath
                prompt = f"""
                You are Rabbit AI. Your file name is {file_path}.
                Based on this instruction: '{instruction}', rewrite the ENTIRE Streamlit app code.
                STRICT RULE: Ensure all existing imports, sidebar configs, and the 'evolve_rabbit' function are PRESERVED in the new code.
                Return ONLY the raw Python code. Do not use markdown backticks like ```python.
                """
                response = model.generate_content(prompt)
                
                if response and response.text:
                    clean_code = response.text.strip()
                    # Markdown backticks cleaning
                    if clean_code.startswith("```"):
                        clean_code = clean_code.split("\n", 1)[1].rsplit("\n", 1)[0]
                    
                    # Update GitHub (Self-Update)
                    status = evolve_rabbit(clean_code)
                    
                    if status in [200, 201]:
                        st.success("Mubarak ho! Rabbit ne khud ko update kar liya hai. 2 minute baad refresh karein.")
                        st.balloons()
                    else:
                        st.error(f"GitHub Error Code: {status}. Token ya Repo permissions check karein.")
                else:
                    st.error("AI code generate nahi kar paya. Dobara try karein.")
            except Exception as e:
                st.error(f"Evolution Error: {e}")
    else:
        st.warning("Pehle Keys aur Instruction bharein!")
