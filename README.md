# PsychAI 🧠 

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)
![Groq](https://img.shields.io/badge/AI-Groq-orange.svg)
![Twilio](https://img.shields.io/badge/Alerts-Twilio-red.svg)

**PsychAI** is an AI-driven mental health ecosystem built to provide 24/7 support to patients while giving psychologists real-time, data-backed insights. It bridges the gap between AI empathy and human clinical expertise.

---

## 🌟 Core Features

### 👤 Patient Chatbot
* **Groq-Powered Conversations:** Utilizes LPU technology for near-instant, empathetic responses.
* **Real-time Emotion Detection:** Analyzes user input using HuggingFace models to identify emotional states (Anxiety, Depression, Joy, etc.).
* **Crisis SOS System:** Integrated with **Twilio**. If the AI detects high-risk keywords, it automatically initiates an emergency voice call to the assigned supervisor (e.g., Dr. Sarakshi).

### 👨‍⚕️ Psychologist Dashboard
* **Live Monitoring:** A secure portal for clinicians to view patient-AI interactions.
* **Sentiment Analytics:** Graphical representation of mood trends over time.
* **Clinical Flags:** Highlights specific symptoms or recurring triggers detected in conversations.
* **Secure Access:** Protected via password authentication to maintain patient confidentiality.

---

## 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Frontend** | Streamlit (Modern, Minimalist UI) |
| **LLM Inference** | Groq Cloud (LLama-3/Mixtral) |
| **NLP/Sentiment** | HuggingFace Transformers |
| **Communications** | Twilio Voice/SMS API |
| **Backend** | Python |

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.9 or higher
* A Groq API Key
* A Twilio Account (SID, Token, and Verified Number)

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/your-username/PsychAI.git](https://github.com/your-username/PsychAI.git)
cd PsychAI

# Install required packages
pip install -r requirements.txt

### 3. Environment Setup
Create a .env file in the root directory
GROQ_API_KEY="your_groq_key"
TWILIO_SID="your_twilio_sid"
TWILIO_TOKEN="your_twilio_token"
ADMIN_PASS="your_secure_password"
CONTACT_NUMBER="+1234567890"

### 4. Run Application
streamlit run app.py
