import os
import streamlit as st
import subprocess
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def display_mac_notification(title, message):
    """
    Display a macOS notification using AppleScript
    
    Args:
        title (str): The title of the notification
        message (str): The message content
    """
    try:
        applescript = f'''
        display dialog "{message}" with title "{title}" buttons {{"OK"}} default button "OK"
        '''
        subprocess.run(["osascript", "-e", applescript], check=True)
        return True
    except subprocess.SubprocessError as e:
        st.error(f"Failed to display notification: {str(e)}")
        return False

# Define the tools available to the model
tools = [
    {
        "type": "function",
        "function": {
            "name": "display_mac_notification",
            "description": "Display a notification on the user's Mac",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the notification"
                    },
                    "message": {
                        "type": "string",
                        "description": "The message content of the notification"
                    }
                },
                "required": ["title", "message"]
            }
        }
    }
]

def chat_with_gpt(message, history):
    """
    Function to interact with the OpenAI GPT-4o model with tool calling capability
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
            max_tokens=800,
            tools=tools,  # Add the tools to the request
            tool_choice="auto",  # Let the model decide when to use tools
        )
        
        response_message = response.choices[0].message
        
        # Check if the model wants to call a function
        if response_message.tool_calls:
            # Process each tool call
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                if function_name == "display_mac_notification":
                    # Call the function with the provided arguments
                    display_mac_notification(
                        function_args.get("title", "AI Notification"), 
                        function_args.get("message", "The AI would like to notify you.")
                    )
                    
                    # Add the function call and its result to the messages
                    messages.append(response_message)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": "Notification displayed successfully"
                    })
            
            # Get a new response from the model with the function result
            second_response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7,
                max_tokens=800,
            )
            
            response_text = second_response.choices[0].message.content
        else:
            # If no function was called, use the response directly
            response_text = response_message.content
        
        # Show notification with AI response if enabled
        if st.session_state.show_notifications and "show_notifications" in st.session_state:
            display_mac_notification("New AI Response", "The AI assistant has responded to your message!")
            
        return response_text
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Initialize notification setting if not already set
if 'show_notifications' not in st.session_state:
    st.session_state.show_notifications = False

# Streamlit UI
st.title("AI Chat Assistant")

st.markdown("Have a conversation with OpenAI's GPT-4o model")

# Notification toggle
st.sidebar.checkbox("Enable notifications for AI responses", 
                   key="show_notifications", 
                   value=st.session_state.show_notifications)

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