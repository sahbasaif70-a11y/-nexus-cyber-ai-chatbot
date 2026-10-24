import os
import uuid
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Load environment variables
load_dotenv(find_dotenv(), override=True)

# Page Configuration
st.set_page_config(
    page_title="Nexus Cyber AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Ultra-Modern Cyberpunk Dashboard CSS (Matching Image Exactly)
custom_css = """
<style>
    /* Dark Theme Core */
    .stApp {
        background: #060515 !important;
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Top Navbar */
    .top-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.8rem 1.5rem;
        background: rgba(12, 11, 36, 0.6);
        backdrop-filter: blur(15px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 1rem;
    }
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.85rem;
        color: #00f0ff;
        font-weight: 500;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #00f0ff;
        border-radius: 50%;
        box-shadow: 0 0 10px #00f0ff;
    }
    .nav-user-profile {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .user-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: #fff;
        font-size: 0.9rem;
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background: #090820 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }
    .sidebar-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1.2rem;
    }
    .sidebar-chip {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: linear-gradient(135deg, #00f0ff, #b829ff);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        color: #fff;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.5);
    }
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00f0ff, #b829ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    /* Sidebar Navigation Links */
    .nav-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0.7rem 1rem;
        border-radius: 12px;
        color: #94a3b8;
        font-weight: 500;
        margin-bottom: 0.4rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .nav-item.active {
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.3), rgba(168, 85, 247, 0.3));
        color: #fff;
        border: 1px solid rgba(168, 85, 247, 0.4);
    }

    /* Chat History Cards in Sidebar */
    .stButton button {
        border-radius: 12px !important;
        text-align: left !important;
        padding: 0.6rem 0.8rem !important;
        font-size: 0.88rem !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        background: rgba(18, 16, 48, 0.5) !important;
        color: #cbd5e1 !important;
        transition: all 0.2s ease !important;
    }
    .stButton button:hover {
        border-color: #00f0ff !important;
        background: rgba(0, 240, 255, 0.1) !important;
        color: #fff !important;
    }
    .stButton button[kind="primary"] {
        background: linear-gradient(90deg, rgba(0, 240, 255, 0.2), rgba(184, 41, 255, 0.3)) !important;
        border: 1px solid #00f0ff !important;
        color: #fff !important;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.2) !important;
    }

    /* Hero AI Badge in Main Area */
    .hero-container {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
        position: relative;
    }
    .ai-orbit-badge {
        width: 90px;
        height: 90px;
        margin: 0 auto 1.5rem auto;
        border-radius: 26px;
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.2), rgba(184, 41, 255, 0.4));
        border: 2px solid #00f0ff;
        box-shadow: 0 0 40px rgba(0, 240, 255, 0.5), inset 0 0 20px rgba(184, 41, 255, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.2rem;
        font-weight: 900;
        color: #fff;
        position: relative;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 900;
        margin: 0 0 0.5rem 0;
        background: linear-gradient(90deg, #00f0ff 0%, #b829ff 50%, #ff2a85 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        max-width: 600px;
        margin: 0 auto 2.5rem auto;
        line-height: 1.6;
    }

    /* Quick Action Prompt Cards (Grid of 4) */
    .quick-card {
        background: rgba(15, 14, 42, 0.7);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 20px;
        padding: 1.2rem;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
        backdrop-filter: blur(10px);
    }
    .quick-card:hover {
        border-color: #00f0ff;
        transform: translateY(-4px);
        box-shadow: 0 10px 25px rgba(0, 240, 255, 0.25);
    }
    .quick-icon {
        font-size: 1.5rem;
        margin-bottom: 0.8rem;
        color: #00f0ff;
    }
    .quick-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.3rem;
    }
    .quick-desc {
        font-size: 0.82rem;
        color: #64748b;
    }

    /* Floating Pill Chat Input */
    [data-testid="stBottom"] > div {
        background: transparent !important;
    }
    .stChatInputContainer {
        border-radius: 35px !important;
        background: rgba(11, 10, 32, 0.92) !important;
        backdrop-filter: blur(20px) !important;
        border: 1.5px solid rgba(0, 240, 255, 0.4) !important;
        box-shadow: 0 0 35px rgba(0, 240, 255, 0.25), inset 0 0 15px rgba(184, 41, 255, 0.15) !important;
        padding: 6px 14px !important;
    }

    /* Bottom Glowing Waves Graphic Overlay */
    .wave-bg {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100vw;
        height: 220px;
        pointer-events: none;
        z-index: 0;
        opacity: 0.6;
    }

    /* Chat Messages */
    [data-testid="stChatMessage"] {
        position: relative;
        z-index: 10;
        border-radius: 20px !important;
        padding: 1.2rem 1.6rem !important;
        margin-bottom: 1rem !important;
        backdrop-filter: blur(16px) !important;
    }
    [data-testid="stChatMessageHuman"] {
        background: rgba(18, 16, 52, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
    }
    [data-testid="stChatMessageAI"] {
        background: rgba(36, 16, 68, 0.8) !important;
        border: 1px solid rgba(184, 41, 255, 0.35) !important;
        box-shadow: 0 0 30px rgba(184, 41, 255, 0.15) !important;
    }
</style>

<!-- Bottom Glowing Neon Wave Vector Ribbon -->
<svg class="wave-bg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" preserveAspectRatio="none">
  <defs>
    <linearGradient id="waveGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#b829ff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#0066ff" stop-opacity="0.5"/>
    </linearGradient>
    <filter id="waveGlow">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>
  <path fill="none" stroke="url(#waveGrad)" stroke-width="3" filter="url(#waveGlow)" d="M0,224L60,213.3C120,203,240,181,360,186.7C480,192,600,224,720,224C840,224,960,192,1080,181.3C1200,171,1320,181,1380,186.7L1440,192"></path>
  <path fill="none" stroke="url(#waveGrad)" stroke-width="2" opacity="0.6" d="M0,256L80,240C160,224,320,192,480,202.7C640,213,800,267,960,261.3C1120,256,1280,192,1360,160L1440,128"></path>
</svg>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY") or ""

if "authenticated" not in st.session_state:
    st.session_state.authenticated = bool(st.session_state.api_key and st.session_state.api_key.strip())

if "chats" not in st.session_state:
    initial_id = str(uuid.uuid4())
    st.session_state.chats = {
        initial_id: {
            "title": "AI Learning Roadmap",
            "system_role": "You are Sahba Saif's personal AI Assistant.",
            "messages": []
        }
    }
    st.session_state.current_chat_id = initial_id

if "current_chat_id" not in st.session_state or st.session_state.current_chat_id not in st.session_state.chats:
    st.session_state.current_chat_id = list(st.session_state.chats.keys())[0]

# ---------------------------------------------------------
# LOGIN GATE SCREEN (Shows BEFORE chatbot unlocks)
# ---------------------------------------------------------
if not st.session_state.authenticated:
    st.markdown("""
    <div style="max-width: 500px; margin: 5rem auto; padding: 2.5rem; background: rgba(12, 11, 36, 0.85); backdrop-filter: blur(25px); border: 1.5px solid rgba(0, 240, 255, 0.4); border-radius: 28px; box-shadow: 0 0 50px rgba(0, 240, 255, 0.25); text-align: center;">
        <div style="width: 70px; height: 70px; margin: 0 auto 1.2rem auto; background: linear-gradient(135deg, rgba(0,240,255,0.3), rgba(184,41,255,0.5)); border: 2px solid #00f0ff; border-radius: 20px; box-shadow: 0 0 25px #00f0ff; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: 900; color: #fff;">AI</div>
        <h1 style="font-size: 2.2rem; font-weight: 900; background: linear-gradient(90deg, #00f0ff, #b829ff, #ff2a85); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;">Nexus Cyber AI</h1>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 2rem;">Enter your API Key to authenticate and unlock your smart assistant interface.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        entered_key = st.text_input(
            "🔑 API Key Authentication",
            value=st.session_state.api_key,
            type="password",
            placeholder="Enter Groq (gsk_...) or OpenAI (sk-...) Key",
            label_visibility="collapsed"
        )
        
        if st.button("⚡ CONNECT & UNLOCK CHATBOT", use_container_width=True, type="primary"):
            if entered_key and entered_key.strip():
                st.session_state.api_key = entered_key.strip()
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Please enter a valid API Key.")
    st.stop()

# ---------------------------------------------------------
# UNLOCKED MAIN INTERFACE
# ---------------------------------------------------------
current_chat = st.session_state.chats[st.session_state.current_chat_id]

# ---------------------------------------------------------
# Top Navbar
# ---------------------------------------------------------
st.markdown("""
<div class="top-navbar">
    <div class="status-indicator">
        <div class="status-dot"></div>
        <span>Online</span> <span style="color: #64748b; margin: 0 6px;">|</span> <span style="color: #94a3b8;">Always here to help</span>
    </div>
    <div class="nav-user-profile">
        <span style="font-size: 1.1rem; cursor: pointer;">🌙</span>
        <span style="font-size: 1.1rem; cursor: pointer;">🔔</span>
        <div class="user-avatar">SS</div>
        <span style="font-weight: 600; font-size: 0.95rem; color: #f8fafc;">Sahba Saif</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    # Header Branding
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-chip">AI</div>
        <div>
            <h2 class="sidebar-title">Nexus Cyber AI</h2>
            <p style="margin: 0; color: #64748b; font-size: 0.8rem;">Your Smart Assistant</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation Links
    st.markdown("""
    <div class="nav-item active">💬 Chat</div>
    <div class="nav-item">🧭 Explore</div>
    <div class="nav-item">⚙️ Settings & Tools</div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Chat History Header + New Chat Button
    col_h1, col_h2 = st.columns([0.6, 0.4])
    with col_h1:
        st.markdown("<p style='font-size: 0.9rem; font-weight: 700; color: #94a3b8; margin-top: 5px;'>📜 Chat History</p>", unsafe_allow_html=True)
    with col_h2:
        if st.button("➕ New Chat", key="new_chat_btn", use_container_width=True, type="primary"):
            new_id = str(uuid.uuid4())
            st.session_state.chats[new_id] = {
                "title": "New Conversation",
                "system_role": "You are Sahba Saif's personal AI Assistant.",
                "messages": []
            }
            st.session_state.current_chat_id = new_id
            st.rerun()

    # Chat History Cards List
    for chat_id, chat_data in list(st.session_state.chats.items()):
        title = chat_data["title"]
        if len(title) > 22:
            title = title[:20] + "..."
        
        btn_type = "secondary" if chat_id != st.session_state.current_chat_id else "primary"
        col1, col2 = st.columns([0.82, 0.18])
        with col1:
            if st.button(f"💬 {title}", key=f"select_{chat_id}", use_container_width=True, type=btn_type):
                st.session_state.current_chat_id = chat_id
                st.rerun()
        with col2:
            if len(st.session_state.chats) > 1:
                if st.button("🗑️", key=f"del_{chat_id}", help="Delete chat"):
                    del st.session_state.chats[chat_id]
                    st.session_state.current_chat_id = list(st.session_state.chats.keys())[0]
                    st.rerun()

    st.markdown("---")

    # Key Logout Button
    if st.button("🔓 Logout / Change API Key", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

    # Bottom Promo Banner
    st.markdown("""
    <div style="margin-top: 1.5rem; padding: 0.8rem; background: linear-gradient(135deg, rgba(0,240,255,0.1), rgba(184,41,255,0.15)); border: 1px solid rgba(0,240,255,0.3); border-radius: 14px; text-align: center; font-size: 0.82rem; font-weight: 600; color: #00f0ff;">
        ⚡ Build your dreams with AI ›
    </div>
    """, unsafe_allow_html=True)

# Build LLM Instance
try:
    if st.session_state.api_key.startswith("gsk_"):
        chat_model = ChatGroq(
            model_name="openai/gpt-oss-20b",
            temperature=0.7,
            max_tokens=4096,
            groq_api_key=st.session_state.api_key
        )
    else:
        chat_model = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.7,
            openai_api_key=st.session_state.api_key
        )
except Exception as e:
    st.error(f"Error initializing model: {str(e)}")
    st.stop()

# ---------------------------------------------------------
# Hero Section (When Chat is New)
# ---------------------------------------------------------
if len(current_chat["messages"]) == 0:
    st.markdown("""
    <div class="hero-container">
        <div class="ai-orbit-badge">AI</div>
        <h1 class="hero-title">Hello Sahba Saif 👋</h1>
        <p class="hero-subtitle">I'm your Nexus Cyber AI — Ask me anything, get instant help, or explore ideas together.</p>
    </div>
    """, unsafe_allow_html=True)

    # 4 Quick Action Prompt Cards
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    with q_col1:
        if st.button("</>\n\nGet Coding Help\nDebug, learn, build", key="q1", use_container_width=True):
            st.session_state.quick_prompt = "Can you help me write and debug Python code?"
            st.rerun()

    with q_col2:
        if st.button("💡\n\nExplore Ideas\nProjects, study, career", key="q2", use_container_width=True):
            st.session_state.quick_prompt = "Give me 5 innovative AI project ideas for my portfolio."
            st.rerun()

    with q_col3:
        if st.button("📄\n\nWrite & Create\nDocs, content, plans", key="q3", use_container_width=True):
            st.session_state.quick_prompt = "Help me write a professional speech and documentation."
            st.rerun()

    with q_col4:
        if st.button("📈\n\nGrow Together\nBetter skills, brighter future", key="q4", use_container_width=True):
            st.session_state.quick_prompt = "Create a step-by-step learning roadmap for AI Development."
            st.rerun()

# Handle quick prompt selection if clicked
quick_input = st.session_state.get("quick_prompt", None)
if quick_input:
    del st.session_state.quick_prompt
    user_prompt = quick_input
else:
    # Main Chat Input (Pill Style)
    user_prompt = st.chat_input("Type your message here...")

# Display Chat Messages
for msg in current_chat["messages"]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("human", avatar="🧑‍💻"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("ai", avatar="🧠"):
            st.write(msg.content)

# Process Prompt
if user_prompt:
    # Set dynamic chat title based on first message
    if len(current_chat["messages"]) == 0 or current_chat["title"] == "AI Learning Roadmap" or current_chat["title"] == "New Conversation":
        current_chat["title"] = user_prompt[:25] + ("..." if len(user_prompt) > 25 else "")

    # Append user message
    current_chat["messages"].append(HumanMessage(content=user_prompt))
    with st.chat_message("human", avatar="🧑‍💻"):
        st.write(user_prompt)

    # Prepare message list with System Message at index 0
    formatted_messages = [SystemMessage(content=current_chat["system_role"])] + current_chat["messages"]

    # Generate Response
    try:
        with st.spinner("Nexus is processing..."):
            response = chat_model.invoke(formatted_messages)

        with st.chat_message("ai", avatar="🧠"):
            st.write(response.content)

        current_chat["messages"].append(AIMessage(content=response.content))
        st.rerun()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
