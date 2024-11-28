# AI Schematic Generator

An AI-powered electronic schematic generator using Anthropic's Claude 3.5 Sonnet.

## Features

- Generate electronic schematics from natural language descriptions
- Analyze existing schematic diagrams
- Support for common electronic components
- CLI interface for easy use

## Installation

1. Clone the repository:
```bash
git clone https://github.com/connorodea/ai-schematic-generator.git
cd ai-schematic-generator
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -e .
```

3. Set up your Anthropic API key:
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

## Usage

Generate a schematic:
```bash
ai_schematics generate "Create a voltage divider with two 10k resistors"
```

Analyze an existing schematic:
```bash
ai_schematics analyze path/to/schematic.png
```

## License

MIT License
