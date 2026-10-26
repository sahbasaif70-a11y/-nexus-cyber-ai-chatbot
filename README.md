# ✦ Multi-Format RAG Question-Answering Agent

A premium, futuristic, multi-format Retrieval-Augmented Generation (RAG) AI Chatbot that lets you upload **PDF, JSON, Excel (.xlsx/.xls), or CSV** documents and ask questions in real time.

---

## 🎨 Option 1: Futuristic React + Tailwind + Framer Motion UI (Matching Reference Screenshot)

### 1️⃣ Start the Python FastAPI Backend:
```bash
py -m uvicorn backend.main:app --reload --port 8000
```

### 2️⃣ Start the React Frontend:
```bash
cd frontend
npm run dev
```
Open **`http://localhost:3000`** in your browser!

---

## 🐍 Option 2: Streamlit Interface

```bash
py -m streamlit run "Rag Practice/rag.py"
```

---

## ⚡ Features & Capabilities
- **Multi-Format Document Support**: PDF, JSON, Excel (`.xlsx`, `.xls`), and CSV.
- **Interactive Configuration Sidebar**: OpenAI API key toggle, model selector (`gpt-4o-mini`, `gpt-4o`), chunk size, chunk overlap, and retrieved chunks (k) sliders.
- **Glassmorphism & Cyber Neon Visuals**: Deep navy theme, glowing borders, animated floating folder & AI robot graphics.
- **Real-Time Indexing & Sources**: View retrieved reference chunks with page/row metadata.
- **Quick Suggestion Chips**: Summarize, find key insights, compare data, or ask anything with a single click.
