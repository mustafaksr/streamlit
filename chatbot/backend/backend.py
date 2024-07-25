from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os

app = Flask(__name__)

# Directory where model will be stored
MODEL_DIR = 'models--gpt2/snapshots/607a30d783dfa663caf39e06633721c8d4cfcd7e'

# Load model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_DIR)
model = GPT2LMHeadModel.from_pretrained(MODEL_DIR)

def generate_response(prompt):
    # Tokenize input
    inputs = tokenizer.encode(prompt, return_tensors="pt")

    # Generate response
    outputs = model.generate(inputs, max_length=100, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    
    # Decode the generated response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

@app.route('/api/get_response', methods=['POST'])
def get_response():
    data = request.json
    prompt = data.get('prompt', '')

    response = generate_response(prompt)

    return jsonify({"generated_text": response})

if __name__ == '__main__':
    app.run(port=6000, host='0.0.0.0', threaded=True)  # Enable threading for handling concurrent requests
