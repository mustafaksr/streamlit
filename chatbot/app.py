import streamlit as st
import requests

st.title("Chatbot with HuggingChat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Flask backend URL
BACKEND_URL = "http://localhost:5000/api/get_response"

# Function to get response from Flask backend
def get_flask_response(prompt):
    response = requests.post(BACKEND_URL, json={"prompt": prompt})
    response_json = response.json()
    return response_json.get('generated_text', 'Sorry, I could not generate a response.')

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from Flask backend
    assistant_message = get_flask_response(prompt)

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(assistant_message)
