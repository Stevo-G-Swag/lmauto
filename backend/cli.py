import os
import sys

import typer
from flask import Flask

app = Flask(__name__)

# Adjust the Python module search path to correctly point to the project root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .main import app as flask_app

cli = typer.Typer()

@cli.command()
def init_agents():
    """
    Initialize the LLM agents.
    """
    # Placeholder for agent initialization logic
    typer.echo("LLM agents initialized.")
    app.logger.info("LLM agents have been initialized.")

@cli.command(name="start-server")
def start_server(port: int = typer.Option(8000, help="The port on which to run the server")):
    """
    Start the Flask web server on a specified port.
    """
    try:
        flask_app.run(port=port)
        typer.echo(f"Server started on port {port}")
        app.logger.info(f"Flask server started successfully on port {port}")
    except Exception as e:
        typer.echo(f"Failed to start the server: {e}")
        app.logger.error("Failed to start the Flask application: %s", e, exc_info=True)
        app.logger.error(f"Error details: {e}")

@cli.command(name="trigger-system")
def trigger_system():
    """
    Trigger the multi-agent system.
    """
    try:
        # Placeholder for triggering the multi-agent system
        typer.echo("Multi-agent system triggered.")
        app.logger.info("Multi-agent system has been triggered.")
    except Exception as e:
        typer.echo(f"Error occurred: {e}")
        app.logger.error("Error during triggering the multi-agent system: %s", e, exc_info=True)
        app.logger.error(f"Error details: {e}")
        raise e

def run():
    """
    Entry point for running the CLI with module execution method.
    """
    cli()

if __name__ == "__main__":
    run()