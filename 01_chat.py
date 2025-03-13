import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize session state for title
if 'title' not in st.session_state:
    st.session_state.title = "AI Chat Demo with GPT-4o v.0.1"

def change_the_title():
    """Function to change the title of the application"""
    st.session_state.title = "New Title: AI Chat with GPT-4o v.0.2"

def chat_with_gpt(message, history):
    """
    Function to interact with the OpenAI GPT-4o model
    """
    # Format history for API call
    messages = []
    for human, ai in history:
        messages.append({"role": "user", "content": human})
        if ai:  # Check if there's a response
            messages.append({"role": "assistant", "content": ai})
    
    # Add the new message from the user
    messages.append({"role": "user", "content": message})
    
    # Get response from OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Streamlit UI
st.title(st.session_state.title)

# Add button to change title
st.button("Change Title", on_click=change_the_title)

st.markdown("Have a conversation with OpenAI's GPT-4o model")

# Chat display area
for human, ai in st.session_state.chat_history:
    st.write(f"**You:** {human}")
    if ai:
        st.write(f"**AI:** {ai}")
    st.write("---")

# Input area
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("Your message:", height=100)
    submitted = st.form_submit_button("Send")
    
    if submitted and user_input:
        # Add user message to history
        st.session_state.chat_history.append([user_input, None])
        
        # Get AI response
        with st.spinner("AI is thinking..."):
            ai_response = chat_with_gpt(user_input, st.session_state.chat_history[:-1])
            
        # Update the last message with AI's response
        st.session_state.chat_history[-1][1] = ai_response
        st.rerun()

# Clear button
if st.button("Clear conversation"):
    st.session_state.chat_history = []
    st.rerun()