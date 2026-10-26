"""
Multi-Format RAG Agent - Futuristic Neon Glassmorphism UI
Stack: OpenAI API + LangChain + FAISS + Pandas + Streamlit

Run with:
    py -m streamlit run "Rag Practice/rag.py"

Required packages:
    py -m pip install streamlit langchain langchain-openai langchain-community langchain-text-splitters faiss-cpu pypdf pandas openpyxl
"""

import json
import os
import tempfile

import pandas as pd
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ---------------------------------------------------------------------------------
# Page Setup & Custom Neon Glassmorphism CSS
# ---------------------------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Format RAG Agent",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Futuristic Dark Glassmorphism CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    }

    /* Main App Background Gradient */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(30, 20, 65, 0.8) 0%, rgba(8, 7, 21, 0.95) 90%),
                    radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.15) 0%, transparent 60%);
        background-attachment: fixed;
        color: #f1f5f9;
    }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background: rgba(14, 12, 34, 0.85) !important;
        backdrop-filter: blur(25px) saturate(190%);
        border-right: 1px solid rgba(168, 85, 247, 0.25);
        box-shadow: 10px 0 40px rgba(124, 58, 237, 0.15);
    }

    /* Headers Styling */
    .sidebar-header {
        font-size: 1.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #c084fc 0%, #e879f9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }
    .sidebar-sub {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-bottom: 20px;
    }

    /* Glowing Section Cards */
    .hero-card {
        background: linear-gradient(135deg, rgba(23, 20, 52, 0.6) 0%, rgba(15, 12, 35, 0.8) 100%);
        border: 1px solid rgba(168, 85, 247, 0.3);
        border-radius: 24px;
        padding: 30px;
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4), inset 0 0 20px rgba(168, 85, 247, 0.08);
        margin-bottom: 25px;
        animation: fadeIn 0.8s ease-in-out;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f3e8ff 0%, #c084fc 40%, #e879f9 70%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        margin-bottom: 8px;
    }

    .hero-desc {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 400;
        max-width: 700px;
    }

    /* Success Status Banner */
    .status-banner {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.08) 100%);
        border: 1px solid rgba(16, 185, 129, 0.4);
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.2);
        border-radius: 20px;
        padding: 16px 24px;
        color: #34d399;
        font-weight: 600;
        font-size: 1.05rem;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 25px;
        animation: slideDown 0.5s ease-out;
    }

    /* Custom Input, Selectbox & Sliders Glow */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background: rgba(20, 17, 45, 0.7) !important;
        border: 1px solid rgba(168, 85, 247, 0.35) !important;
        border-radius: 14px !important;
        color: #f8fafc !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    .stTextInput input:focus, .stSelectbox [data-baseweb="select"]:focus-within {
        border-color: #c084fc !important;
        box-shadow: 0 0 20px rgba(192, 132, 252, 0.4) !important;
    }

    /* Custom File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(22, 18, 50, 0.5) !important;
        border: 2px dashed rgba(168, 85, 247, 0.4) !important;
        border-radius: 20px !important;
        padding: 15px !important;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #e879f9 !important;
        box-shadow: 0 0 25px rgba(232, 121, 249, 0.3) !important;
    }

    /* Chat Messages Glassmorphism */
    [data-testid="stChatMessage"] {
        background: rgba(20, 17, 46, 0.65) !important;
        border: 1px solid rgba(168, 85, 247, 0.25) !important;
        border-radius: 22px !important;
        backdrop-filter: blur(15px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 15px !important;
        padding: 16px !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stChatMessage"]:hover {
        border-color: rgba(192, 132, 252, 0.5) !important;
        box-shadow: 0 0 25px rgba(168, 85, 247, 0.25) !important;
    }

    /* Chat Input Styling */
    [data-testid="stChatInput"] {
        border-radius: 30px !important;
        border: 1px solid rgba(168, 85, 247, 0.5) !important;
        background: rgba(16, 13, 38, 0.9) !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 0 30px rgba(168, 85, 247, 0.25) !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #e879f9 !important;
        box-shadow: 0 0 40px rgba(232, 121, 249, 0.4) !important;
    }

    /* Expander Glassmorphism */
    .stExpander {
        background: rgba(18, 15, 42, 0.5) !important;
        border: 1px solid rgba(168, 85, 247, 0.2) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(10px);
    }

    /* Keyframe Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Preset Button Pill Styling */
    div.stButton > button {
        background: rgba(30, 24, 68, 0.7) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(168, 85, 247, 0.35) !important;
        border-radius: 25px !important;
        padding: 8px 18px !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        background: rgba(168, 85, 247, 0.25) !important;
        border-color: #e879f9 !important;
        color: #ffffff !important;
        box-shadow: 0 0 20px rgba(232, 121, 249, 0.4) !important;
        transform: translateY(-2px) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-header">⚙️ Configuration</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Fine-tune your RAG Agent parameters</div>', unsafe_allow_html=True)
    
    # OpenAI API Key Input
    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", "")
    )
    
    if not openai_api_key:
        st.info("Enter your OpenAI API key in the sidebar to begin")
        st.stop()
    elif not openai_api_key.startswith("sk-"):
        st.warning("⚠️ OpenAI API keys usually start with 'sk-'. Make sure you copied the full key from https://platform.openai.com/api-keys")

    os.environ["OPENAI_API_KEY"] = openai_api_key.strip()
    
    # Model Selection
    model_name = st.selectbox("Chat model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])

    chunk_size = st.slider("Chunk size", 500, 2000, 1000, step=100)
    chunk_overlap = st.slider("Chunk overlap", 0, 400, 150, step=50)
    top_k = st.slider("Retrieved chunks (k)", 2, 10, 4)
    
    # Multi-Format File Uploader
    uploaded_file = st.file_uploader(
        "Upload Document (PDF, JSON, Excel, CSV)",
        type=["pdf", "json", "xlsx", "xls", "csv"]
    )

# ---------------------------------------------------------------------------------
# Function to Parse PDF, JSON, Excel, and CSV into Documents
# ---------------------------------------------------------------------------------
def load_documents_from_file(file_path: str, file_name: str):
    ext = os.path.splitext(file_name)[1].lower()
    docs = []

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
        docs = loader.load()

    elif ext in [".xlsx", ".xls", ".csv"]:
        if ext == ".csv":
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        for idx, row in df.iterrows():
            row_text = "\n".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
            docs.append(
                Document(
                    page_content=f"[Row {idx + 1}]\n{row_text}",
                    metadata={"row": idx + 1, "source": file_name}
                )
            )

    elif ext == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if isinstance(data, list):
            for i, item in enumerate(data):
                item_str = json.dumps(item, indent=2) if isinstance(item, (dict, list)) else str(item)
                docs.append(
                    Document(
                        page_content=f"[Item {i + 1}]\n{item_str}",
                        metadata={"item": i + 1, "source": file_name}
                    )
                )
        elif isinstance(data, dict):
            for k, v in data.items():
                v_str = json.dumps(v, indent=2) if isinstance(v, (dict, list)) else str(v)
                docs.append(
                    Document(
                        page_content=f"[{k}]\n{v_str}",
                        metadata={"key": k, "source": file_name}
                    )
                )
        else:
            docs.append(Document(page_content=str(data), metadata={"source": file_name}))

    return docs

# ---------------------------------------------------------------------------------
# Function to Process File and Create FAISS Vectorstore
# ---------------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def build_vectorstore(file_bytes: bytes, file_name: str, size: int, overlap: int, api_key: str) -> FAISS:
    ext = os.path.splitext(file_name)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        docs = load_documents_from_file(tmp_path, file_name)
    finally:
        os.unlink(tmp_path)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    chunks = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key.strip())
    return FAISS.from_documents(chunks, embeddings)

# ---------------------------------------------------------------------------------
# Hero Banner Header
# ---------------------------------------------------------------------------------
st.markdown("""
<div class="hero-card">
    <div class="hero-title">✨ Multi-Format RAG Question-Answering Agent</div>
    <div class="hero-desc">Upload PDF, JSON, Excel (.xlsx/.xls), or CSV files and ask questions based on their content in real time.</div>
</div>
""", unsafe_allow_html=True)

if uploaded_file is not None:
    file_sig = (uploaded_file.name, uploaded_file.size, chunk_size, chunk_overlap)
    if st.session_state.get("file_sig") != file_sig:
        with st.spinner(f"Parsing and indexing **{uploaded_file.name}**..."):
            try:
                st.session_state.vectorstore = build_vectorstore(
                    uploaded_file.getvalue(), uploaded_file.name, chunk_size, chunk_overlap, openai_api_key
                )
                st.session_state.file_sig = file_sig
                st.session_state.messages = []
            except Exception as e:
                st.error(f"Error indexing file with OpenAI: {str(e)}")

    if "file_sig" in st.session_state:
        st.markdown(f"""
        <div class="status-banner">
            <span>✔</span>
            <span>Indexed <strong>{uploaded_file.name}</strong> - ask away!</span>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------------
# RAG Chain Setup
# ---------------------------------------------------------------------------------
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful assistant that answers questions strictly using the provided context from a document (PDF, JSON, Excel, or CSV).\n"
     "1. Answer ONLY from the context below\n"
     "2. If the answer is not in the context, say: \"I couldn't find that in the document.\"\n"
     "3. Cite the relevant page/row/item number(s) or key(s) if applicable.\n\n"
     "Context:\n{context}"),
    ("human", "{question}"),
])

def format_docs(docs) -> str:
    formatted = []
    for d in docs:
        source_tag = ""
        if "page" in d.metadata:
            source_tag = f"[Page {d.metadata['page'] + 1}]"
        elif "row" in d.metadata:
            source_tag = f"[Row {d.metadata['row']}]"
        elif "item" in d.metadata:
            source_tag = f"[Item {d.metadata['item']}]"
        elif "key" in d.metadata:
            source_tag = f"[Key: {d.metadata['key']}]"

        content = d.page_content.strip()
        formatted.append(f"{source_tag}\n{content}" if source_tag else content)
    return "\n\n".join(formatted)

def create_stream_generator(vectorstore: FAISS, model: str, k: int, api_key: str, question: str):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    clean_key = api_key.strip()
    
    llm = ChatOpenAI(model=model, temperature=0, api_key=clean_key)
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | RAG_PROMPT | llm | StrOutputParser()
    )
    return chain.stream(question), retriever

# ---------------------------------------------------------------------------------
# Chat Interface & Quick Suggestion Chips
# ---------------------------------------------------------------------------------
if "vectorstore" in st.session_state:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Prompt Chips
    st.markdown("##### 💡 Quick Suggestions")
    c1, c2, c3, c4 = st.columns(4)
    preset_query = None
    with c1:
        if st.button("📑 Summarize the document"):
            preset_query = "Provide a comprehensive summary of this document."
    with c2:
        if st.button("🔍 Find specific information"):
            preset_query = "What are the main key points and findings in this document?"
    with c3:
        if st.button("📊 Compare data"):
            preset_query = "Compare the main data points or categories present in this document."
    with c4:
        if st.button("✨ Ask anything..."):
            preset_query = "List the top 5 most important details from this file."

    # Replay conversation history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle input (either typed or from suggestion chip)
    user_input = st.chat_input("Ask a question about your uploaded document....")
    question = preset_query if preset_query else user_input

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            try:
                stream, retriever = create_stream_generator(
                    st.session_state.vectorstore,
                    model_name,
                    top_k,
                    openai_api_key,
                    question
                )
                
                answer = st.write_stream(stream)
                
                # Show retrieved chunks for transparency
                with st.expander("Source (retrieved chunks)"):
                    docs = retriever.invoke(question)
                    if docs:
                        for doc in docs:
                            meta = doc.metadata
                            tag = meta.get("page", meta.get("row", meta.get("item", meta.get("key", "Chunk"))))
                            st.markdown(f"**Reference: {tag}**")
                            st.text(doc.page_content[:500])
                            st.divider()
                    else:
                        st.write("No matching text found in document.")

                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"⚠️ OpenAI API Error: {str(e)}")
else:
    st.info("👈 Upload a PDF, JSON, Excel, or CSV file in the sidebar to get started.")
