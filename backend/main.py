import logging
import os
import sys
import uuid
from typing import Dict, List

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pydantic import ValidationError

# Adjust the Python module search path to correctly point to the project root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.models.llm_agent import LLMAgent, PromptRequest

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")  # Ensure your OPENAI_API_KEY is set in the .env file.

# Initialize Flask app
app = Flask(__name__)

# Initialize the LLM agent
agent = LLMAgent(api_key=OPENAI_API_KEY, model="gpt-4")

# In-memory storage for conversation history (replace with a database for production)
conversations: Dict[str, List[Dict]] = {}

@app.route('/')
def hello_world():
    app.logger.info("Hello world endpoint called.")
    return 'Hello, LMAuto!'

@app.route('/start-conversation', methods=['POST'])
def start_conversation():
    conversation_id = str(uuid.uuid4())
    conversations[conversation_id] = []
    app.logger.info(f"Started new conversation with ID: {conversation_id}")
    return jsonify({"conversation_id": conversation_id}), 201

@app.route('/prompt/<conversation_id>', methods=['POST'])
def send_prompt(conversation_id: str):
    if conversation_id not in conversations:
        return jsonify({"error": "Invalid conversation ID"}), 404

    try:
        prompt_data = request.get_json()
        prompt_request = PromptRequest(**prompt_data)

        # Add prompt to conversation history
        conversations[conversation_id].append({"role": "user", "content": prompt_request.prompt})

        response = agent.send_prompt(prompt_request, conversations[conversation_id])

        # Add response to conversation history
        conversations[conversation_id].append({"role": "assistant", "content": response.response})

        app.logger.info(f"Prompt sent successfully in conversation {conversation_id}")
        return jsonify(response.dict()), 200

    except ValidationError as e:
        app.logger.error(f"Validation error on prompt data: {e.errors()}", exc_info=True)
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        app.logger.error(f"Failed to send prompt in conversation {conversation_id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/history/<conversation_id>', methods=['GET'])
def get_conversation_history(conversation_id: str):
    if conversation_id not in conversations:
        return jsonify({"error": "Invalid conversation ID"}), 404
    return jsonify(conversations[conversation_id]), 200

if __name__ == '__main__':
    try:
        app.run(port=8000)
        app.logger.info("Flask server started successfully on port 8000")
    except Exception as e:
        app.logger.error(f"Failed to start the Flask application: {e}", exc_info=True)