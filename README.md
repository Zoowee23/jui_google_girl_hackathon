# jui_google_girl_hackathon
# 📞 AI-Powered Customer Support Chatbot & Sentiment Analysis System

🚀 **Revolutionizing customer support for electronics companies using AI-driven chatbots and sentiment analysis!**  

## 📌 Overview  
This project integrates **a chatbot and a sentiment analysis tool** to improve customer support for **refrigerator-related queries**.  
- The **chatbot** provides **instant responses** regarding **warranty, service, and maintenance**.  
- The **sentiment analysis tool** processes **customer feedback** and takes **appropriate action** based on sentiment detection.  

## 🎯 Features  
### ✅ **AI Chatbot for Refrigerator Support**  
- Provides **warranty, servicing, and maintenance details**.  
- **Speech-to-text functionality** for hands-free queries.  
- **Escalates complex queries** to **human agents**.  
- Uses **Gemini AI API / GPT API** for **AI-powered responses**.  

### ✅ **Customer Sentiment Analysis**  
- **Detects positive/negative feedback** from customer input.  
- **Logs feedback** in a **structured database**.  
- **Escalates complaints** to a human agent for critical issues.  
- **Suggests offers** for satisfied customers to enhance engagement.  

### ✅ **Speech Recognition**  
- Allows customers to **speak instead of typing**.  
- Uses **Google Speech Recognition API**.  

---

## 🛠 Technologies Used  
| Component              | Technology |
|------------------------|------------|
| **Backend**            | Python, SQLite |
| **Chatbot AI**         | Google Gemini API, OpenAI GPT API |
| **Speech Recognition** | Google Speech-to-Text API, PyAudio |
| **GUI**               | PyQt (for Sentiment Analysis Tool) |

---

## 🏗 Database Schema  
### **Tables:**
1. **users** → Stores customer details.  
2. **products** → Stores refrigerator details.  
3. **agents** → Stores human agent contacts.  
4. **feedback** → Logs customer sentiment and complaints.  
5. **offers** → Stores available promotional offers
