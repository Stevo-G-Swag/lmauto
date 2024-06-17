import os
import sys

from dotenv import load_dotenv
from flask import Flask, jsonify, request

# Adjust the Python module search path to correctly point to the project root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.llm_agent import LLMAgent, PromptRequest
from pydantic import ValidationError

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Initialize the LLM agent
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
agent = LLMAgent(api_key=api_key, model="gpt-4o")

@app.route('/')
def hello_world():
    app.logger.info("Hello world endpoint called.")
    return 'Hello, LMAuto!'

@app.route('/init', methods=['POST'])
def init_agents():
    try:
        # Initialization logic if any
        app.logger.info("Initializing LLM agents.")
        return jsonify({"message": "LLM agents initialized"}), 200
    except ValueError as init_error:
        app.logger.error("Failed to initialize LLM agents: %s", init_error, exc_info=True)
        return jsonify({"error": str(init_error)}), 500

@app.route('/prompt', methods=['POST'])
def send_prompt():
    try:
        prompt_data = request.json
        if prompt_data is not None:
            prompt_request = PromptRequest(**prompt_data)
            response = agent.send_prompt(prompt_request)
            app.logger.info("Prompt sent successfully.")
            return jsonify(response.dict()), 200
        else:
            app.logger.error("No data provided for prompt.")
            return jsonify({"error": "No data provided"}), 400
    except ValidationError as validation_error:
        app.logger.error("Validation error on prompt data: %s", validation_error.errors(), exc_info=True)
        return jsonify({"error": str(validation_error.errors())}), 400
    except Exception as e:
        app.logger.error("Failed to send prompt: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/retrieve', methods=['GET'])
def retrieve_output():
    try:
        # Placeholder for retrieval logic
        app.logger.info("Retrieving output.")
        return jsonify({"message": "Retrieved output"}), 200
    except ValidationError as validation_error:
        app.logger.error("Validation error on retrieval: %s", validation_error.errors(), exc_info=True)
        return jsonify({"error": str(validation_error.errors())}), 400

if __name__ == '__main__':
    try:
        app.run(port=8000)  # Using a port other than 5000
        app.logger.info("Flask server started successfully on port 8000")
    except Exception as inner_exception:
        app.logger.error("Failed to start the Flask application: %s", inner_exception, exc_info=True)
        app.logger.error("Error details: %s", inner_exception)