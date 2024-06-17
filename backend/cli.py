import os
import sys
import logging

import typer
from flask import Flask
import openai

app = Flask(__name__)

# Adjust the Python module search path to correctly point to the project root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .main import app as flask_app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cli = typer.Typer()

@cli.command()
def init_agents(model_name: str = typer.Option(..., help="The name of the model to use")):
    """
    Initialize the LLM agents.
    """
    try:
        # Initialize the LLM agents
        openai.api_key = "YOUR_OPENAI_API_KEY"
        models = openai.Model.list()["data"]
        model_ids = [model["id"] for model in models]
        if model_name not in model_ids:
            typer.echo("Available models:")
            for i, model_id in enumerate(model_ids):
                typer.echo(f"{i+1}. {model_id}")
            model_name = typer.prompt("Enter the number of the model to use")
            model_name = model_ids[int(model_name) - 1]
        llm_agents = model_name
        logger.info("LLM agents initialized.")
        typer.echo("LLM agents initialized.")
    except Exception as e:
        logger.error("Error initializing LLM agents: %s", e, exc_info=True)
        typer.echo(f"Error initializing LLM agents: {e}")

@cli.command(name="start-server")
def start_server(port: int = typer.Option(8000, help="The port on which to run the server")):
    """
    Start the Flask web server on a specified port.
    """
    try:
        app.run(port=port)
        logger.info(f"Flask server started successfully on port {port}")
        typer.echo(f"Server started on port {port}")
    except Exception as e:
        logger.error("Failed to start the Flask application: %s", e, exc_info=True)
        typer.echo(f"Failed to start the server: {e}")

@cli.command(name="trigger-system")
def trigger_system():
    """
    Trigger the multi-agent system.
    """
    try:
        # Trigger the multi-agent system
        from .agent_system import trigger_system
        trigger_system()
        logger.info("Multi-agent system has been triggered.")
        typer.echo("Multi-agent system triggered.")
    except Exception as e:
        logger.error("Error during triggering the multi-agent system: %s", e, exc_info=True)
        typer.echo(f"Error occurred: {e}")
        raise e

def run():
    """
    Entry point for running the CLI with module execution method.
    """
    cli()

if __name__ == "__main__":
    run()