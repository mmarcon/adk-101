# ADK 101

A tour guide agent application built with Google ADK and TensorLake, featuring an AI-powered tour guide with knowledge of history and culture.

## Features

- AI-powered tour guide agent using Claude Sonnet
- Location-aware recommendations
- Integration with Arize for observability and tracing
- Async execution with TensorLake applications

## Prerequisites

- Python 3.13+
- Anthropic API key
- Arize API key (for observability)

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your credentials:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ARIZE_API_KEY=your_arize_api_key
   ```

## Usage

Run the application:
```bash
python main.py
```

The default query asks about interesting historical sites in the user's location.

## Project Structure

- `main.py` - Entry point for the application
- `adk_ooo/agent.py` - Tour guide agent implementation
- `requirements.txt` - Python dependencies

## Security

The `.env` file containing sensitive credentials is excluded from version control. Never commit API keys or secrets to the repository.

## License

MIT
