

https://github.com/user-attachments/assets/05679a2c-017a-4c78-93ec-52ce4e9e2bb4

# ⚡ Nexus Cyber AI — Next-Gen AI Assistant Dashboard

Nexus Cyber AI is an ultra-modern, cyberpunk-themed AI Assistant web application built with **Streamlit**, **LangChain**, **Groq LLM**, and **OpenAI**. It features dynamic multi-chat session management, customizable system personas, a prompt marketplace template explorer, model parameter controls, and chat history exports.

---

## ✨ Key Features

- ⚡ **Cyberpunk UI & Theme**: Custom CSS design featuring glowing neon gradients, dark mode, floating chat inputs, and responsive layout.
- 🔑 **Secure Key Authentication**: Supports both **Groq API Keys** (`gsk_...`) and **OpenAI API Keys** (`sk-...`).
- 📜 **Multi-Chat History**: Create, switch between, and delete multiple independent chat sessions seamlessly.
- 🧭 **AI Prompt Template Marketplace**: Pre-configured dynamic templates for:
  - 🧑‍💻 *Full-Stack Code Reviewer*
  - 🚀 *AI Startup & Product Strategy*
  - 🎓 *Personalized Learning & Career Roadmap*
  - 📄 *Technical Documentation & Speech Writer*
- ⚙️ **Customizable AI Settings**:
  - Fine-tune model `Temperature` (creativity) and `Max Output Tokens`.
  - Customize system roles/personas per conversation.
  - Custom display name and avatar initials.
- 📥 **Chat Export**: Download conversation logs instantly as structured JSON files.

---

## 🛠️ Tech Stack

- **Frontend / UI Framework**: [Streamlit](https://streamlit.io/)
- **AI Framework**: [LangChain](https://www.langchain.com/)
- **LLM Integrations**:
  - `langchain-groq` (`openai/gpt-oss-20b`)
  - `langchain-openai` (`gpt-4o-mini`)
- **Environment Management**: `python-dotenv`

---

## 🚀 Getting Started Locally

### 1. Prerequisites
Make sure you have Python 3.10 or higher installed.

### 2. Clone the Repository
```bash
git clone https://github.com/sahbasaif70-a11y/-nexus-cyber-ai-chatbot.git
cd -nexus-cyber-ai-chatbot
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup (Optional)
Create a `.env` file in the project folder and add your API keys:
```env
GROQ_API_KEY=your_groq_api_key_here
# OR
OPENAI_API_KEY=your_openai_api_key_here
```
*(You can also enter your API key directly on the login screen inside the app).*

### 5. Run the Application
```bash
streamlit run custom_streamlit_app.py
```

---

## 📁 Project Structure

```
custom_chat_gpt/
├── custom_streamlit_app.py  # Main Streamlit Dashboard Application
├── requirements.txt         # Required Python Dependencies
└── README.md                # Project Documentation
```

---

## 🔑 Getting Free API Keys

- **Groq API Key (Free & Fast)**: Get one at [console.groq.com/keys](https://console.groq.com/keys)
- **OpenAI API Key**: Get one at [platform.openai.com](https://platform.openai.com)

---

## 👤 Author

Developed by **Sahba Saif** ⚡
