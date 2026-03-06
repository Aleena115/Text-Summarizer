import streamlit as st
from google import genai
import os

# Page configuration for a premium look
st.set_page_config(
    page_title="Summarizer AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced aesthetics and custom Header
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
<style>
    /* Gradient Background */
    .stApp {
        background: radial-gradient(circle at top, #1e1b4b 0%, #0f172a 40%, #020617 100%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Application Header styling */
    h1.app-title {
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -0.025em;
        padding-top: 1rem;
    }
    h1.app-title span.gradient-text {
        background: linear-gradient(135deg, #c084fc 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Subtitle styling */
    .subtitle {
        color: #cbd5e1;
        font-size: 1.15rem;
        margin-bottom: 2.5rem;
        font-family: 'Inter', sans-serif;
        text-align: center;
        font-weight: 300;
        line-height: 1.6;
    }
    
    /* Chat message global */
    .stChatMessage {
        background: rgba(30, 41, 59, 0.4);
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        font-family: 'Inter', sans-serif;
    }
    
    /* Alternate background for assistant/user */
    .stChatMessage:nth-child(even) {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Input field container styling */
    [data-testid="stChatInput"] {
        padding-bottom: 2rem;
    }
    
    .stChatInputContainer {
        border-radius: 2rem !important;
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    
    /* Input area focus */
    .stChatInputContainer:focus-within {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.3), 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(124, 58, 237, 0.4);
        color: white;
    }
    
    /* Info box styling */
    [data-testid="stAlert"] {
        background: rgba(30, 64, 175, 0.2);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 0.75rem;
        color: #e0e7ff;
    }
    
    /* Hide Streamlit logo & UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}
</style>

<div class="app-header">
    <h1 class="app-title">✨ <span class="gradient-text">Summarizer AI</span></h1>
    <p class="subtitle">Instantly distill long texts into clear, concise summaries using Google Gemini.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:10px;">
            <img src="https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg" width="40">
            <h2 style='margin: 0; font-family: Inter, sans-serif; font-weight: 600;'>Settings</h2>
        </div>
        <hr style='border-color: rgba(255,255,255,0.1); margin: 1.5rem 0;'>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='font-family: Inter, sans-serif; font-size: 1.1rem;'>About</h3>", unsafe_allow_html=True)
    st.info("This application uses the `gemini-2.5-flash` model to provide fast and accurate summaries of your provided text.")
    
    if st.button("Clear Conversation", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Initialize the Gemini Client
# HARDCODED API KEY (Replace with your actual key)
API_KEY = "YOUR_API_KEY_HERE" 

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Failed to initialize Gemini Client: {e}")
    st.stop()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "✨"):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Paste the text you want to summarize here..."):
    # Output the user message immediately
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare assistant response container
    with st.chat_message("assistant", avatar="✨"):
        message_placeholder = st.empty()
        
        # Prepare the summarization prompt
        summarization_prompt = f"Please provide a highly concise and structured summary of the following text. Use bullet points for key takeaways if appropriate:\n\n{prompt}"
        
        try:
            with st.spinner("Analyzing and summarizing..."):
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=summarization_prompt
                )
                
                if response.text:
                    summary = response.text
                    message_placeholder.markdown(summary)
                    st.session_state.messages.append({"role": "assistant", "content": summary})
                else:
                    message_placeholder.error("Could not generate a summary. The model returned an empty response.")
        except Exception as e:
            message_placeholder.error(f"An error occurred during summarization: {e}")

