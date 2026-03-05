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

# Custom CSS for enhanced aesthetics
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Header styling */
    h1 {
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.025em;
        margin-bottom: 0.5rem;
    }
    
    /* Subtitle styling */
    .subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: #1e293b;
        border-radius: 0.75rem;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* User message specific */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #0f172a;
        border: 1px solid #1e293b;
    }
    
    /* Input field styling */
    .stChatInputContainer {
        border-radius: 9999px;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Application Header
st.title("✨ Summarizer AI")
st.markdown('<p class="subtitle">Instantly distill long texts into clear, concise summaries using Google Gemini.</p>', unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg", width=50) # Gemini icon
    st.title("Settings")
    
    st.markdown("### About")
    st.info("This application uses the `gemini-2.5-flash` model to provide fast and accurate summaries of your provided text.")
    
    if st.button("Clear Conversation"):
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
