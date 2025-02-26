import os
import requests
import sqlite3
import datetime
import speech_recognition as sr  # ✅ Importing Speech Recognition for Speech-to-Text
from dotenv import load_dotenv

# ✅ Load API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ✅ Refrigerator-Related Keywords
refrigerator_keywords = [
    "refrigerator", "fridge", "cooling", "freezer", "compressor", "defrost", "temperature",
    "ice maker", "coolant", "refrigerant", "door seal", "power consumption", "energy efficiency",
    "smart fridge", "inverter technology", "multi-door", "single-door", "double-door",
    "humidity control", "vegetable crisper", "water dispenser", "noise issue", "thermostat",
    "food storage", "odors", "auto-defrost", "LED display"
]

# ✅ Servicing Keywords
servicing_keywords = ["service", "servicing", "services", "schedule service", "service plan"]

# ✅ Maintenance Keywords
maintenance_keywords = ["maintain", "maintenance", "maintainance", "maintaining", "maintenance plan"]

# ✅ Function to Validate Email in Database
def is_valid_email(email):
    conn = sqlite3.connect("electronics_company.db")
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# ✅ Function to Convert Speech to Text
# ✅ Function to Convert Speech to Text
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now... Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for noise

        try:
            audio = recognizer.listen(source, timeout=10)  # ⬆ Increased timeout to 10 seconds
            text = recognizer.recognize_google(audio).lower()
            print(f"🗣 Recognized: {text}")
            return text
        except sr.WaitTimeoutError:
            print("⚠️ No speech detected. Please try speaking again.")
            return recognize_speech()  # Retry speech recognition
        except sr.UnknownValueError:
            print("❌ Couldn't understand the audio. Please try again.")
            return recognize_speech()  # Retry on failure
        except sr.RequestError:
            print("⚠️ API unavailable. Check your internet connection.")
            return ""


# ✅ Function to Fetch AI-Predicted Service Cost
def get_dynamic_service_price(model):
    prompt = f"""
    Provide an estimated servicing cost for a {model} refrigerator.
    Consider warranty status, age, common issues, and brand reputation.
    """
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-002:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "⚠️ Error fetching service cost."
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# ✅ Function to Fetch Warranty Details
def get_warranty_info(email):
    conn = sqlite3.connect("electronics_company.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT users.name, products.name, users.warranty_expiry
    FROM users
    JOIN products ON users.product_id = products.id
    WHERE users.email = ?
    """, (email,))
    user_data = cursor.fetchone()
    conn.close()
   
    if user_data:
        return f"Hello {user_data[0]}, your {user_data[1]} has a warranty until {user_data[2]}."
    else:
        return "No warranty details found for this email."

# ✅ Function to Fetch AI-Driven Maintenance Plan Suggestions
def get_best_maintenance_plan(model, current_plan):
    prompt = f"""
    A user owns a {model} refrigerator and currently has the '{current_plan}' maintenance plan.
    Based on cost, longevity, and energy efficiency, recommend the best maintenance plan:
    - Options: Basic, Standard, or Premium.
    - Ensure the suggestion benefits both the user and the company profit-wise.
    """
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-002:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "⚠️ Error fetching maintenance plan recommendation."
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# ✅ Function to Fetch Maintenance Plan
def get_maintenance_plan(email):
    conn = sqlite3.connect("electronics_company.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT users.name, products.name, users.maintenance_plan
    FROM users
    JOIN products ON users.product_id = products.id
    WHERE users.email = ?
    """, (email,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        name, model, current_plan = user_data
        best_plan = get_best_maintenance_plan(model, current_plan)
        return f"Hello {name}, your current maintenance plan is **'{current_plan}'**.\n\n💡 **Suggested Plan:** {best_plan}"
    else:
        return "No maintenance plan details found for this email."

# ✅ Function to Fetch Last Service Date & Schedule Service
def get_service_info(email):
    conn = sqlite3.connect("electronics_company.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT users.name, products.name, users.last_service_date, users.warranty_expiry
    FROM users
    JOIN products ON users.product_id = products.id
    WHERE users.email = ?
    """, (email,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        name, model, last_service_date, warranty_expiry = user_data
        today = datetime.date.today()
        warranty_expiry_date = datetime.datetime.strptime(warranty_expiry, "%Y-%m-%d").date()

        print(f"📅 Your last service date was: {last_service_date}.")
        choice = input("Would you like to schedule a new service? (yes/no): ").strip().lower()

        if choice == "yes":
            while True:
                new_service_date = input("Enter the new service date (YYYY-MM-DD): ").strip()
                try:
                    new_date = datetime.datetime.strptime(new_service_date, "%Y-%m-%d").date()
                    if new_date < today:
                        print("⚠️ Error: The selected date is in the past. Please choose a future date.")
                        continue

                    conn = sqlite3.connect("electronics_company.db")
                    cursor = conn.cursor()
                    
                    if today <= warranty_expiry_date:
                        cursor.execute("UPDATE users SET last_service_date = ? WHERE email = ?", (new_service_date, email))
                        conn.commit()
                        conn.close()
                        return f"✅ Your **free service** has been scheduled for {new_service_date}!"
                    else:
                        service_cost = get_dynamic_service_price(model)
                        cursor.execute("UPDATE users SET last_service_date = ? WHERE email = ?", (new_service_date, email))
                        conn.commit()
                        conn.close()
                        return f"🔴 Your service has been scheduled !! Your warranty has expired. **Estimated service cost:** {service_cost}"

                except ValueError:
                    print("⚠️ Error: Invalid date format. Please use YYYY-MM-DD.")
                    continue
        else:
            return "Okay, no service scheduled."
    
    return "No service details found for this email."
# ✅ Function to Get Chatbot Response Using Gemini AI API (Restricted to Refrigerators)
def chatbot_response(user_input):
    if not any(keyword in user_input.lower() for keyword in refrigerator_keywords):
        return "⚠️ I can only assist with **refrigerator-related queries**. Let me know if you need help with refrigerator warranty, maintenance, or servicing."

    prompt = f"Answer this question specifically about refrigerators: {user_input}"

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-002:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}        
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"⚠️ API Error: {response.json()}"
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ✅ Chatbot Interaction Loop (Now Includes Speech Recognition)
if __name__ == "__main__":
    email = input("Enter your registered email: ").strip()

    if not is_valid_email(email):
        print("⚠️ Error: This email is not registered.")
        exit()

    while True:
        choice = input("\nDo you want to type or speak? (type/speak): ").strip().lower()

        if choice == "speak":
            user_input = recognize_speech()
            if not user_input:  
                user_input = input("You (type): ").lower().strip()
        else:
            user_input = input("You: ").lower().strip()

        if user_input == "exit":
            print("👋 Goodbye!")
            break
        elif any(word in user_input for word in maintenance_keywords):
            response = get_maintenance_plan(email)
        elif any(word in user_input for word in servicing_keywords):
            response = get_service_info(email)
        elif "warranty" in user_input:
            response = get_warranty_info(email)
        else:
            response = chatbot_response(user_input) 

        print("Bot:", response)
