import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError

load_dotenv()  # Load environment variables from .env file

class PromptRequest(BaseModel):
    prompt: str
    max_tokens: int
    temperature: float = 0.5

    class Config:
        extra = "ignore"


class PromptResponse(BaseModel):
    id: str
    choices: list[dict]  # Updated to specify a list of dictionaries

    def __getitem__(self, index):
        return self.choices[index]

    class Config:
        extra = "ignore"


class LLMAgent:
    """
    This is the LLMAgent class.
    """

    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def send_prompt(self, request: PromptRequest) -> PromptResponse:
        """
        Send a prompt and return the response.
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
        Set the model to be used.
        """
        self.model = model


# Example usage
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
agent = LLMAgent(api_key=api_key, model="gpt-4")
try:
    response = agent.send_prompt(PromptRequest(prompt="Hello, world!", max_tokens=5))
    print(response)
except Exception as e:
    print(f"Error during prompt sending: {e}")