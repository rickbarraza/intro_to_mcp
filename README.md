# OpenAI Chat Demo with GPT

This is a Streamlit-based chat application that uses OpenAI's GPT model.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

1. Clone the repository
```bash
git clone <repository-url>
cd mcp_demo
```

2. Create and activate a virtual environment
```bash
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
- Copy `.env.example` to `.env`
- Replace `YOUR_API_KEY_HERE` with your actual OpenAI API key

## Running the Application

1. Ensure your virtual environment is activated
2. Run the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your default web browser.

## Project Structure

- `app.py` - Main application file containing the Streamlit UI and chat logic
- `requirements.txt` - Project dependencies
- `.env` - Environment variables (not tracked in git)
- `.env.example` - Example environment variables template

## Features

- Real-time chat interface with GPT-4o
- Chat history management
- Conversation clearing
- Dynamic title updates