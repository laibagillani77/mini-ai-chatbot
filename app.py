import streamlit as st
from google import genai

# Connect MiniAi to Google Gemini
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# -----------------------------

# PAGE CONFIG

# -----------------------------

st.set_page_config(

    page_title="MiniAI",

    page_icon="🤖",

    layout="centered",

    initial_sidebar_state="collapsed"

)

# -----------------------------

# CUSTOM CSS

# -----------------------------

st.markdown("""
<style>

/* All your CSS goes here */

/* Main application background */

.stApp {

    background:

        radial-gradient(

            circle at 50% 0%,

            rgba(37, 99, 235, 0.16),

            transparent 45%

        ),

        #0b1220;

    color: #f8fafc;

}

/* Main content */

.block-container {

    max-width: 900px;

    padding-top: 2.5rem;

    padding-bottom: 7rem;

}

/* Main title */

.main-title {

    font-size: 3.2rem;

    font-weight: 800;

    letter-spacing: -1.8px;

    line-height: 1.2;

    color: #f8fafc;

    margin-bottom: 0.4rem;

}

/* Subtitle */

.subtitle {

    color: #94a3b8;

    font-size: 1rem;

    line-height: 1.7;

    margin-bottom: 2rem;

}

/* Welcome card */

.welcome-card {

    background: rgba(30, 41, 59, 0.75);

    border: 1px solid #334155;

    border-radius: 20px;

    padding: 32px;

    margin-bottom: 28px;

    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.16);

}

/* Welcome heading */

.welcome-title {

    font-size: 1.5rem;

    font-weight: 700;

    color: #f8fafc;

    margin-bottom: 10px;

}

/* Welcome description */

.welcome-text {

    color: #cbd5e1;

    font-size: 0.98rem;

    line-height: 1.7;

}

/* Suggested prompts heading */

.section-title {

    font-size: 1.15rem;

    font-weight: 650;

    color: #e2e8f0;

    margin-top: 24px;

    margin-bottom: 14px;

}

/* Buttons */

.stButton > button {

    background: #172338;

    color: #e2e8f0;

    border: 1px solid #334155;

    border-radius: 12px;

    min-height: 48px;

    font-weight: 500;

    transition: all 0.2s ease;

}

.stButton > button:hover {

    background: #1e3a5f;

    color: #ffffff;

    border-color: #60a5fa;

}

/* Chat message containers */

[data-testid="stChatMessage"] {

    background: rgba(30, 41, 59, 0.55);

    border: 1px solid rgba(148, 163, 184, 0.16);

    border-radius: 16px;

    padding: 16px;

    margin-bottom: 12px;

}

/* Chat input */

[data-testid="stChatInput"] {

    border-radius: 14px;

}

/* Footer */

.footer {

    text-align: center;

    color: #64748b;

    font-size: 0.8rem;

    margin-top: 48px;

    padding-top: 20px;

    border-top: 1px solid #253247;

}

/* Mobile layout */

@media (max-width: 640px) {

    .block-container {

        padding-top: 1.5rem;

    }

    .main-title {

        font-size: 2.5rem;

    }

    .welcome-card {

        padding: 22px;

    }

    }
    /* Chat input styling */
    [data-testid="stChatInput"] {
        background: #111c35 !important;
        border: 2px soild #60a5fa !important;
        border-radius: 18px !important;
        box-shadow: 0 8px 30px rgba(37, 99, 235, 0.25) !important;
    }
    [data-testid="stChatInput"] textarea {
        color: white !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #93c5fd !important;
        box-shadow: 0 0 0 4px rgba(96, 165, 250, 0.2); !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

# --------------------------------

# HEADER

# --------------------------------

st.markdown(

    '<div class="main-title">✧Mini<span style="color:#93c5fd;">AI</span></div>',

    unsafe_allow_html=True

)

st.markdown(

    '<div class="subtitle">'

    'A lightweight conversational assistant built with Python'

    '</div>',

    unsafe_allow_html=True

)

# -----------------------------

# CHAT HISTORY

# -----------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []

# -----------------------------

# CLEAR CHAT

# -----------------------------

if st.button("🗑️ Clear conversation"):

    st.session_state.messages = []

    st.rerun()

# -----------------------------

# WELCOME SCREEN

# -----------------------------
if not st.session_state.messages:

    st.info(

        "👋 Welcome to MiniAI\n\n"

        "Ask me about Python, computer science, programming, "

        "or just start a conversation."

    )

    st.markdown("### 💡 Try asking")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("🐍 What is Python?", use_container_width=True):

            st.session_state.messages.append({

                "role": "user",

                "content": "What is Python?"

            })

            st.rerun()

    with col2:

        if st.button("💻 What is computer science?", use_container_width=True):

            st.session_state.messages.append({

                "role": "user",

                "content": "What is computer science?"

            })

            st.rerun()

# -----------------------------

# DISPLAY CHAT HISTORY

# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

# -----------------------------

# CHAT INPUT

# -----------------------------

prompt = st.chat_input("Message MiniAI...")

if prompt:

    # Add user message

    st.session_state.messages.append({

        "role": "user",

        "content": prompt

    })

    with st.chat_message("user"):

        st.write(prompt)

    # Generate an AI response using Gemini

    with st.spinner("MiniAI is thinking..."):

        try:

            conversation = []

            for message in st.session_state.messages:

                role = (

                    "model"

                    if message["role"] == "assistant"

                    else "user"

                )

                conversation.append({

                    "role": role,

                    "parts": [

                        {"text": message["content"]}

                    ]

                })

            ai_response = client.models.generate_content(

                model="gemini-3.8-flash",

                contents=conversation

            )

            response = ai_response.text

            if not response:

                response = (

                    "Sorry, I couldn't generate "

                    "a response. Please try again."

                )

        except Exception as e:

            response = (

                "Sorry, MiniAI couldn't connect "

                "to Gemini. Please try again."

            )

            st.error(f"Gemini error: {e}")

    # Add assistant response

    st.session_state.messages.append({

        "role": "assistant",

        "content": response

    })

    with st.chat_message("assistant"):

        st.write(response)

# -----------------------------

# FOOTER

# -----------------------------

st.markdown(

    '<div class="footer">'

    'MiniAI · Built with Python + Streamlit'

    '</div>',

    unsafe_allow_html=True

)