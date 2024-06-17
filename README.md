# L2MAC - Large Language Model Automatic Computer

The L2MAC (Large Language Model Automatic Computer) framework is an innovative project designed to harness the power of large language models (LLMs) for automating complex tasks such as generating entire codebases or comprehensive documentation. Utilizing a von Neumann architecture, this multi-agent system overcomes the limitations of fixed context windows in LLMs, enhancing productivity and innovation in software development and content creation.

## Overview

### Architecture
L2MAC integrates a multi-agent system using Python for backend processing and OpenAI's GPT models for language processing tasks. The system architecture follows the von Neumann model, incorporating elements such as LLM-based processors, control units, and an external memory system to manage data flow and task execution efficiently.

### Technologies Used
- **Python**: Main programming language for backend operations.
- **Node.js**: Required for running the VitePress-powered documentation site.
- **Pydantic**: Utilized for data validation within Python applications.
- **Typer**: Employed for building command-line interfaces.
- **OpenAI Python Library**: Interface for interacting with OpenAI's GPT models.
- **VitePress**: Vue.js powered static site generator for web documentation.

### Project Structure
- `backend/main.py`: Flask web application setup.
- `backend/cli.py`: Command-line interface for system interaction.
- `models/llm_agent.py`: Module for interacting with OpenAI's language models.
- `.env`: Configuration file for environment variables.
- `utilities/external_memory.py`: Handles data storage and retrieval.

## Features

L2MAC offers several key features:
- **Multi-Agent System**: Allows multiple LLM agents to handle portions of tasks sequentially.
- **Extensive Output Generation**: Capable of producing large-scale outputs from single input prompts.
- **Self-Generating Prompt Programs**: Automates the generation of detailed task-specific prompts.
- **Advanced Memory Handling**: Enhances task consistency and depth by storing past interactions.
- **Error Handling and Tool Integration**: Ensures error-free outputs and adherence to quality standards.
- **Customizable and Scalable**: Adaptable to various domains and scalable for different task complexities.
- **Interactive Web Documentation**: Provides accessible tutorials and guides through a VitePress-based platform.

## Getting Started

### Requirements
- Python 3.8 or higher
- Node.js 14 or higher
- An API key from OpenAI for GPT model interactions

### Quickstart
1. Clone the repository to your local machine.
2. Install Python dependencies: `pip install -r requirements.txt`
3. Set up the environment variable for OpenAI API key in `.env` file.
4. Run the Flask server: `python backend/main.py`
5. Access the VitePress documentation locally by navigating to the respective directory and running `npm install` followed by `npm run dev`.

### License

Copyright (c) 2024.

This documentation and the associated software are proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.