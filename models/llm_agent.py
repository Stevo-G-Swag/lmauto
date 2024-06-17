import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError
from flask import Flask, request, jsonify

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

class PromptRequest(BaseModel):
    """
    Represents a prompt request with a prompt, maximum tokens, and temperature.
    """
    prompt: str
    max_tokens: int
    temperature: float = 0.5

    class Config:
        extra = "ignore"


class PromptResponse(BaseModel):
    """
    Represents a prompt response with an ID and a list of choices.
    """
    id: str
    choices: list[dict]  # Updated to specify a list of dictionaries

    def __getitem__(self, index):
        return self.choices[index]

    class Config:
        extra = "ignore"


class LLMAgent:
    """
    Represents an LLM agent that interacts with the OpenAI API.
    """

    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initializes an instance of the LLMAgent class.

        Args:
            api_key (str): The OpenAI API key.
            model (str, optional): The model to use. Defaults to "gpt-4".
        """
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def send_prompt(self, request: PromptRequest) -> PromptResponse:
        """
        Sends a prompt to the OpenAI API and returns the response.

        Args:
            request (PromptRequest): The prompt request.

        Returns:
            PromptResponse: The response from the OpenAI API.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model, messages=[{"role": "system", "content": request.prompt}], max_tokens=request.max_tokens, temperature=request.temperature
            )
            # Transform the response to match the expected structure of PromptResponse
            choices = [{"content": choice['content']} for choice in response.choices]
            return PromptResponse(id=response.id, choices=choices)
        except ValidationError as ve:
            print(f"Validation error: {ve}")
            raise
        except Exception as e:
            print(f"Failed to send prompt: {e}")
            raise

    def set_model(self, model: str):
        """
        Sets the model to be used.

        Args:
            model (str): The model to use.
        """
        self.model = model


# Create an instance of the LLMAgent
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
agent = LLMAgent(api_key=api_key, model="gpt-4")

# Define a route for the web app
@app.route('/prompt', methods=['POST'])
def handle_prompt():
    """
    Handles a prompt request and returns the response.
    """
    data = request.get_json()
    prompt_request = PromptRequest(**data)
    response = agent.send_prompt(prompt_request)
    return jsonify({'id': response.id, 'choices': response.choices})

if __name__ == "__main__":
    app.run(debug=True)