from flask import Flask, request, jsonify
import requests
import streamlit as st

app = Flask(__name__)

# Set Hugging Face API key and URL
API_KEY = st.secrets["HUGGINGFACE_API_KEY"]
API_URL = "https://api-inference.huggingface.co/models/gpt2"

@app.route('/api/get_response', methods=['POST'])
def get_response():
    data = request.json
    prompt = data.get('prompt')

    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    response_json = response.json()
    return jsonify(response_json[0])

if __name__ == '__main__':
    app.run(port=5000)
