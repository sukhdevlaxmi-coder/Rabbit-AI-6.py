import math
import time
import getpass # For secure password input

class RabbitAI:
    def __init__(self, version="12.0"):
        self.version = version
        self.evolution_log = [
            f"Rabbit AI v{version} initialized.",
            "Core module architecture refined for modularity.",
            "Integrated 'Multimedia' tab with basic 360 content simulation.",
            "Integrated 'Gaming' tab with simplified Angry Birds physics engine.",
            "Integrated 'HCS Master' tab for dynamic exam preparation.",
            "Integrated 'Guardian' tab for enhanced security protocols (face/bank)."
        ]
        self.tabs = {
            "1": MultimediaTab(self),
            "2": GamingTab(self),
            "3": HCSMasterTab(self),
            "4": GuardianTab(self)
        }
        print(f"Rabbit AI v{self.version} booting up...")
        time.sleep(1)
        print("Evolution sequence complete. Self-diagnostic reports indicate optimal performance.")
        for log in self.evolution_log:
            print(f"  > {log}")
        time.sleep(1)

    def display_menu(self):
        print("\n--- Rabbit AI v12.0 Core Tabs (Enhanced Functionality) ---")
        print("1. Multimedia (360 Photo/Video Viewer)")
        print("2. Gaming (Angry Birds Physics Simulator)")
        print("3. HCS Master (Haryana Exam Prep Quiz)")
        print("4. Guardian (Face/Bank Security System)")
        print("5. Exit Rabbit AI")
        print("---------------------------------------------------------")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Select a tab (1-5) for advanced interaction: ").strip()

            if choice == '5':
                print("Rabbit AI v12.0 powering down. System hibernation initiated. Goodbye!")
                break
            elif choice in self.tabs:
                self.tabs[choice].run_tab()
            else:
                print("Invalid choice. Please select a valid tab number from the core modules.")
            time.sleep(1)

class MultimediaTab:
    def __init__(self, ai_instance):
        self.ai = ai_instance
        self.loaded_content = None

    def load_360_image(self, image_name="Serene_Himalayan_Panorama.jpg"):
        print(f"\n[Multimedia] Initiating 360-degree image load for: '{image_name}'...")
        time.sleep(1.5)
        print(f"[Multimedia] Image '{image_name}' fully loaded. Commencing spherical projection.")
        self.loaded_content = {"type": "image", "name": image_name}
        self.display_content()

    def load_360_video(self, video_name="Deep_Ocean_Exploration_360.mp4"):
        print(f"\n[Multimedia] Preparing 360-degree video stream for: '{video_name}'...")
        time.sleep(2)
        print(f"[Multimedia] Video '{video_name}' buffered. Activating immersive playback mode.")
        self.loaded_content = {"type": "video", "name": video_name}
        self.display_content()

    def display_content(self):
        if self.loaded_content:
            print(f"\n[Multimedia] Rendering '{self.loaded_content['name']}' ({self.loaded_content['type']}) in 360° environment...")
            print("  [Visualizer: Panoramic Console Output]")
            print("  --------------------------------------------------")
            print("  |                                                |")
            print("  |   (Simulated Gaze: UP)       [CENTRAL VIEW]    |")
            print("  |      (Left Scroll)         (Right Scroll)      |")
            print("  |                                                |")
            print("  --------------------------------------------------")
            print("  > Experience spatial immersion. (Actual 3D rendering requires advanced GUI)")
        else:
            print("\n[Multimedia] No content currently loaded. Please select an option to load media.")

    def run_tab(self):
        print("\n--- Multimedia Tab (360 Photo/Video) ---")
        while True:
            print("1. Load 360 Panoramic Image")
            print("2. Load 360 Immersive Video")
            print("3. View Currently Loaded Content")
            print("4. Return to Rabbit AI Main Menu")
            choice = input("Select a multimedia operation: ").strip()

            if choice == '1':
                self.load_360_image()
            elif choice == '2':
                self.load_360_video()
            elif choice == '3':
                self.display_content()
            elif choice == '4':
                print("[Multimedia] Exiting multimedia module. Data unloaded.")
                break
            else:
                print("Invalid option. Please choose a valid multimedia function.")
            time.sleep(1)

class GamingTab:
    def __init__(self, ai_instance):
        self.ai = ai_instance
        self.gravity = 9.81  # m/s^2, Earth's gravity
        self.target_x = 250  # meters, distance to the target structure
        self.target_radius = 15 # meters, collision radius for target

    def play_angry_birds(self):
        print("\n--- Angry Birds Physics Simulation (Projectile Motion) ---")
        print("Objective: Launch the bird to hit the distant target structure at X = 250m!")

        try:
            initial_velocity = float(input("Enter initial launch velocity (m/s, e.g., 60): "))
            launch_angle_deg = float(input("Enter launch angle (degrees from horizontal, e.g., 40): "))
        except ValueError:
            print("Invalid input detected. Please enter numerical values for velocity and angle.")
            return

        launch_angle_rad = math.radians(launch_angle_deg)

        print(f"\n[Gaming] Bird launching with V={initial_velocity:.2f} m/s at {launch_angle_deg:.2f}°...")
        time.sleep(1)

        max_simulation_time = 20 # seconds
        time_step = 0.25 # seconds per frame
        current_x = 0.0
        current_y = 0.0
        hit_target = False

        print("Flight Path Simulation:")
        for t_step in range(int(max_simulation_time / time_step) + 1):
            t = t_step * time_step
            current_x = initial_velocity * math.cos(launch_angle_rad) * t
            current_y = initial_velocity * math.sin(launch_angle_rad) * t - 0.5 * self.gravity * t**2

            if current_y < 0: # Bird hits the ground
                current_y = 0 # Ensure y doesn't go negative after impact
                print(f"Time: {t:.2f}s | X: {current_x:.2f}m | Y: {current_y:.2f}m | Status: Ground Impact!")
                break

            print(f"Time: {t:.2f}s | X: {current_x:.2f}m | Y: {current_y:.2f}m")

            # Enhanced collision detection with the target zone
            if abs(current_x - self.target_x) <= self.target_radius and current_y >= 0:
                print(f"\n*** [SUCCESS] TARGET STRUCTURE HIT! ***")
                print(f"Collision Point: X={current_x:.2f}m, Y={current_y:.2f}m.")
                hit_target = True
                break
            
            time.sleep(0.05) # Simulate flight progression

        if not hit_target:
            print(f"\n[FAILURE] Bird landed at X={current_x:.2f}m (Y=0m). Target was at {self.target_x}m.")
            print("Mission Failed. Recalibrating trajectory for next attempt.")

    def run_tab(self):
        while True:
            print("\n--- Gaming Tab (Angry Birds Physics) ---")
            print("1. Start Angry Birds Physics Simulation")
            print("2. Return to Rabbit AI Main Menu")
            choice = input("Select a gaming option: ").strip()

            if choice == '1':
                self.play_angry_birds()
            elif choice == '2':
                print("[Gaming] Exiting simulation. Physics engine reset.")
                break
            else:
                print("Invalid option. Please select a valid gaming function.")
            time.sleep(1)

class HCSMasterTab:
    def __init__(self, ai_instance):
        self.ai = ai_instance
        self.questions = [
            {
                "question": "हरियाणा का राजकीय पक्षी कौन सा है?",
                "options": ["कबूतर", "काला तीतर", "सारस क्रेन", "मोर"],
                "answer": "काला तीतर",
                "explanation": "काला तीतर (Black Francolin) हरियाणा का राजकीय पक्षी है।"
            },
            {
                "question": "हरियाणा राज्य का गठन कब हुआ था?",
                "options": ["1 नवंबर 1966", "15 अगस्त 1947", "26 जनवरी 1950", "2 अक्टूबर 1969"],
                "answer": "1 नवंबर 1966",
                "explanation": "हरियाणा राज्य का गठन 1 नवंबर 1966 को पंजाब से अलग होकर हुआ था।"
            },
            {
                "question": "पानीपत का प्रथम युद्ध कब हुआ था?",
                "options": ["1526", "1556", "1761", "1191"],
                "answer": "1526",
                "explanation": "पानीपत का प्रथम युद्ध 1526 में बाबर और इब्राहिम लोदी के बीच हुआ था।"
            },
            {
                "question": "हरियाणा में 'पिंजौर विरासत उत्सव' किस जिले में मनाया जाता है?",
                "options": ["पंचकूला", "अम्बाला", "कुरुक्षेत्र", "करनाल"],
                "answer": "पंचकूला",
                "explanation": "पिंजौर विरासत उत्सव पंचकूला जिले में मनाया जाता है, जो इसकी सांस्कृतिक विरासत को दर्शाता है।"
            },
            {
                "question": "गुड़गांव का नया नाम क्या है?",
                "options": ["गुरुग्राम", "कर्णग्राम", "धर्मग्राम", "इंद्रग्राम"],
                "answer": "गुरुग्राम",
                "explanation": "गुड़गांव का नाम बदलकर गुरुग्राम किया गया है, जो गुरु द्रोणाचार्य से संबंधित है।"
            }
        ]

    def start_quiz(self):
        print("\n--- HCS Master: Haryana Exam Preparation Quiz ---")
        print("Test your knowledge of Haryana General Knowledge.")
        score = 0
        total_questions = len(self.questions)

        for i, q_data in enumerate(self.questions):
            print(f"\nQuestion {i+1} of {total_questions}: {q_data['question']}")
            for j, option in enumerate(q_data['options']):
                print(f"  {j+1}. {option}")

            user_answer_input = input("Enter the number of your chosen answer: ").strip()
            
            try:
                user_answer_idx = int(user_answer_input) - 1
                if 0 <= user_answer_idx < len(q_data['options']):
                    user_selected_option = q_data['options'][user_answer_idx]
                    if user_selected_option == q_data['answer']:
                        print("Correct! Excellent insight.")
                        score += 1
                    else:
                        print(f"Incorrect. The correct answer was: {q_data['answer']}")
                        print(f"Explanation: {q_data['explanation']}")
                else:
                    print(f"Invalid option number. The correct answer was: {q_data['answer']}")
                    print(f"Explanation: {q_data['explanation']}")
            except ValueError:
                print(f"Invalid input format. Please enter a number. The correct answer was: {q_data['answer']}")
                print(f"Explanation: {q_data['explanation']}")
            time.sleep(1.5)

        print(f"\n--- HCS Quiz Completed! ---")
        print(f"Your final score: {score} out of {total_questions}.")
        if score == total_questions:
            print("Outstanding! You possess mastery of Haryana GK. HCS Master status achieved!")
        elif score >= total_questions / 2:
            print("Good performance! With a bit more study, you'll excel. Keep up the effort!")
        else:
            print("Further practice is recommended. Don't be discouraged, consistent effort leads to success!")

    def run_tab(self):
        while True:
            print("\n--- HCS Master Tab (Haryana Exam Prep) ---")
            print("1. Start Haryana GK Quiz")
            print("2. Return to Rabbit AI Main Menu")
            choice = input("Select an HCS Master function: ").strip()

            if choice == '1':
                self.start_quiz()
            elif choice == '2':
                print("[HCS Master] Exiting quiz module. Knowledge database remains active.")
                break
            else:
                print("Invalid option. Please choose a valid HCS Master function.")
            time.sleep(1)

class GuardianTab:
    def __init__(self, ai_instance):
        self.ai = ai_instance
        self.authorized_face_id = "RabbitAI_SecureUser_BiometricID_ALPHA007" # Mock biometric ID
        self.bank_account = {
            "account_number": "RABBIT1234567890AI",
            "pin": "1234", # WARNING: In a real system, never store plaintext PINs! Use hashing.
            "balance": 5000.75
        }
        self.known_users = {
            "rabbit_admin": "SecureAI@Pass!",
            "test_user": "user123"
        }

    def simulate_face_recognition(self):
        print("\n--- Guardian: Advanced Biometric Face Security Scan ---")
        print("Activating high-precision neural network for facial biometric authentication...")
        time.sleep(2.5)
        
        mock_face_match_input = input("Simulate successful biometric match? (yes/no): ").strip().lower()

        if mock_face_match_input == "yes":
            print(f"Facial scan complete. Biometric signature matched: {self.authorized_face_id}.")
            print("Access Granted! Welcome, authorized user.")
            return True
        else:
            print("Facial scan failed or no match found in authorized database.")
            print("Access Denied. Security alert initiated (mock).")
            return False

    def secure_bank_transaction(self):
        print("\n--- Guardian: Secure Quantum Bank Portal ---")
        print(f"Welcome to your secure banking. Your current balance: ${self.bank_account['balance']:.2f}")

        pin_attempts = 3
        authenticated = False

        for i in range(pin_attempts):
            entered_pin = getpass.getpass("Enter your 4-digit Transaction PIN: ").strip()
            if entered_pin == self.bank_account['pin']:
                print("PIN Verified. Secure session established for transactions.")
                authenticated = True
                break
            else:
                print(f"Incorrect PIN. {pin_attempts - 1 - i} attempts remaining before lock-out.")
                time.sleep(1)
        
        if not authenticated:
            print("Too many incorrect PIN attempts. Banking access temporarily suspended (simulation).")
            return

        while authenticated:
            print("\nSecure Banking Options:")
            print("1. Deposit Funds (Encrypted)")
            print("2. Withdraw Funds (Secure E-Transfer)")
            print("3. Check Account Balance")
            print("4. Return to Guardian Security Menu")
            
            choice = input("Select a secure banking operation: ").strip()

            if choice == '1':
                try:
                    amount = float(input("Enter amount to deposit (USD): $"))
                    if amount > 0:
                        self.bank_account['balance'] += amount
                        print(f"Successfully deposited ${amount:.2f}. New secure balance: ${self.bank_account['balance']:.2f}")
                        print("Transaction recorded with quantum encryption.")
                    else:
                        print("Deposit amount must be a positive value.")
                except ValueError:
                    print("Invalid amount entered. Please use numerical values.")
            elif choice == '2':
                try:
                    amount = float(input("Enter amount to withdraw (USD): $"))
                    if amount > 0 and amount <= self.bank_account['balance']:
                        self.bank_account['balance'] -= amount
                        print(f"Successfully withdrew ${amount:.2f}. New secure balance: ${self.bank_account['balance']:.2f}")
                        print("Funds transferred via secure channel.")
                    elif amount > self.bank_account['balance']:
                        print("Insufficient funds for this withdrawal.")
                    else:
                        print("Withdrawal amount must be a positive value.")
                except ValueError:
                    print("Invalid amount entered. Please use numerical values.")
            elif choice == '3':
                print(f"Current secure account balance: ${self.bank_account['balance']:.2f}")
            elif choice == '4':
                print("[Guardian] Exiting secure banking portal. Session terminated.")
                break
            else:
                print("Invalid option. Please select a valid banking function.")
            time.sleep(1)

    def secure_login_system(self):
        print("\n--- Guardian: Encrypted User Login ---")
        username = input("Enter secure username: ").strip()
        password = getpass.getpass("Enter encrypted password: ").strip() # Hides input

        if username in self.known_users and self.known_users[username] == password:
            print(f"Welcome, {username}! Encrypted login successful. Access granted to privileged features.")
            return True
        else:
            print("Invalid username or password. Credential mismatch detected.")
            return False


    def run_tab(self):
        print("\n--- Guardian Tab (Face/Bank Security) ---")
        while True:
            print("1. Simulate Biometric Face Recognition")
            print("2. Access Secure Banking Portal")
            print("3. Test Encrypted User Login System")
            print("4. Return to Rabbit AI Main Menu")
            choice = input("Select a Guardian security function: ").strip()

            if choice == '1':
                self.simulate_face_recognition()
            elif choice == '2':
                self.secure_bank_transaction()
            elif choice == '3':
                self.secure_login_system()
            elif choice == '4':
                print("[Guardian] Exiting security module. All systems remain on high alert.")
                break
            else:
                print("Invalid option. Please select a valid Guardian function.")
            time.sleep(1)

if __name__ == "__main__":
    rabbit_ai = RabbitAI()
    rabbit_ai.run()
