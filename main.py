import sys
import os
from PyQt5.QtWidgets import QApplication
from chatbot import is_valid_email
from sentiment_analysis import SentimentApp

if __name__ == "__main__":
    email = input("Enter your registered email: ").strip()

    if not is_valid_email(email):
        print("⚠️ Error: This email is not registered in our system.")
        exit()

    chatbot_mode = input("Type 'chatbot' to use chatbot or 'sentiment' to provide feedback: ").strip().lower()

    if chatbot_mode == "chatbot":
        print("🔄 Launching chatbot...")
        os.system("python chatbot.py")  # ✅ Executes chatbot.py

    elif chatbot_mode == "sentiment":
        print("🔄 Launching sentiment analysis application...")
        app = QApplication(sys.argv)
        sentiment_app = SentimentApp()
        sentiment_app.show()
        sys.exit(app.exec_())  # ✅ Runs sentiment_analysis.py

    else:
        print("⚠️ Invalid choice. Please restart and select 'chatbot' or 'sentiment'.")
