import os
import sqlite3
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from dotenv import load_dotenv

# ✅ Load API Key
load_dotenv()
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

# ✅ Database Connection Function
def get_human_agent_info():
    """Fetches contact details of a human agent from the database."""
    conn = sqlite3.connect("electronics_company.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone FROM agents LIMIT 1")  # Fetch a human agent
    agent_info = cursor.fetchone()
    conn.close()
    
    if agent_info:
        return f"⚠️ Connecting you to **{agent_info[0]}** at {agent_info[1]}"
    else:
        return "⚠️ No human agent available at the moment."

def get_available_offers():
    """Fetches available offers from the database."""
    conn = sqlite3.connect("electronics_company.db")
    cursor = conn.cursor()
    cursor.execute("SELECT offer_details FROM offers")  # Fetch available offers
    offers = cursor.fetchall()
    conn.close()
    
    if offers:
        return "🎉 Special Offers: " + ", ".join([offer[0] for offer in offers])
    else:
        return "No special offers available at the moment."

def log_feedback(user_id, feedback_text, sentiment):
    """Logs user feedback into the `feedback` table."""
    conn = sqlite3.connect("electronics_company.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO feedback (user_id, feedback_text, sentiment) 
    VALUES (?, ?, ?)
    """, (user_id, feedback_text, sentiment))
    conn.commit()
    conn.close()
    print("✅ Feedback logged successfully.")

class SentimentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Customer Feedback & Sentiment Analysis')
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap('logo.png').scaled(250, 250, Qt.KeepAspectRatio))
        self.logo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo)

        self.speechButton = QPushButton('Speak Now for Feedback Analysis', self)
        self.speechButton.clicked.connect(self.listen_and_analyze)
        self.layout.addWidget(self.speechButton)

        self.sentimentLabel = QLabel('Overall Sentiment Analysis: Not analyzed yet', self)
        self.layout.addWidget(self.sentimentLabel)

        self.actionItemsLabel = QLabel('Action Items from the Feedback: Not analyzed yet', self)
        self.layout.addWidget(self.actionItemsLabel)

        self.actionItemsList = QListWidget(self)
        self.layout.addWidget(self.actionItemsList)

    def listen_and_analyze(self):
        """Captures audio and processes the feedback."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤 Speak now...")
            self.sentimentLabel.setText("Listening... Please speak now.")
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                print(f"🗣 Recognized Speech: {text}")
                self.process_text(text)
            except sr.UnknownValueError:
                print("❌ Could not understand the audio.")
                self.sentimentLabel.setText("Error: Could not understand.")
            except sr.RequestError:
                print("⚠️ API unavailable. Check your internet connection.")
                self.sentimentLabel.setText("Error: Speech API unavailable.")

    def process_text(self, text):
        """Processes the speech-to-text output for sentiment analysis."""
        sentiment = self.analyze_sentiment_text(text)
        action_items = self.get_action_items(text)

        self.sentimentLabel.setText(f"Overall Sentiment Analysis: {sentiment}")
        self.actionItemsLabel.setText(f"Action Items: {len(action_items)} found")
        self.actionItemsList.clear()
        for item in action_items:
            self.actionItemsList.addItem(item)

        # ✅ Fetch user ID (assuming the user exists in DB)
        user_id = self.get_user_id()

        if user_id:
            log_feedback(user_id, text, sentiment)

        # ✅ Handling additional functionalities
        if sentiment == "NEGATIVE":
            print("We are sorry for the inconvenience!!")
            agent_info = get_human_agent_info()
            print(f"⚠️ {agent_info}")  # Display in terminal
            # ✅ Ensure action items are displayed
            if not action_items:
                action_items.append("Apologize for the inconvenience.")
                action_items.append("Escalate the issue to a manager.")
                self.actionItemsLabel.setText(f"Action Items: {len(action_items)} found")
                self.actionItemsList.clear()
                for item in action_items:
                    self.actionItemsList.addItem(item)

        elif sentiment == "POSITIVE":
            print("🙏 Thank you for your valuable feedback! 😊")
            offers = get_available_offers()
            print(f"🎉 {offers}")  # Display in terminal

    def analyze_sentiment_text(self, text):
        """Performs a simple sentiment analysis on user feedback."""
        negative_words = ["angry", "frustrated", "bad", "issue", "poor", "terrible"]
        positive_words = ["happy", "great", "thank you", "satisfied", "excellent", "amazing"]

        text = text.lower()
        if any(word in text for word in negative_words):
            return "NEGATIVE"
        elif any(word in text for word in positive_words):
            return "POSITIVE"
        else:
            return "NEUTRAL"

    def get_action_items(self, text):
        """Suggests action items based on the detected sentiment."""
        action_items = []
        if any(word in text for word in ["angry", "bad", "issue", "frustrated"]):
            action_items.append("Apologize for the inconvenience.")
            action_items.append("Escalate the issue to a manager.")
        if any(word in text for word in ["happy", "great", "thank you", "excellent"]):
            action_items.append("Thank the customer for their feedback.")
            action_items.append("Recommend additional services.")
        return action_items

    def get_user_id(self):
        """Fetches the user ID based on stored email or customer details (mock logic)."""
        conn = sqlite3.connect("electronics_company.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users LIMIT 1")  # Fetching first user for simplicity
        user = cursor.fetchone()
        conn.close()
        return user[0] if user else None

if __name__ == "__main__":
    app = QApplication([])
    window = SentimentApp()
    window.show()
    app.exec_()  # 🔥 This starts the Qt event loop
