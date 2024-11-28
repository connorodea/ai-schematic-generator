#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}Running AI Schematic Generator Tests${NC}"

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${RED}Not in a virtual environment. Creating one...${NC}"
    python3 -m venv venv
    source venv/bin/activate
fi

# Install test dependencies
echo -e "${BLUE}Installing test dependencies...${NC}"
pip install pytest pytest-asyncio pytest-cov pytest-mock

# Run tests
echo -e "${BLUE}Running unit tests...${NC}"
pytest -v --cov=ai_schematic_generator --cov-report=html --cov-report=term -m "not integration"

# Check if integration tests should be run
if [ ! -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${BLUE}Running integration tests...${NC}"
    pytest -v -m integration
else
    echo -e "${RED}Skipping integration tests (ANTHROPIC_API_KEY not set)${NC}"
fi

# Generate coverage report
echo -e "${BLUE}Test coverage report generated in htmlcov/index.html${NC}"

# Check for code style
echo -e "${BLUE}Checking code style...${NC}"
flake8 ai_schematic_generator tests

# Run type checking
echo -e "${BLUE}Running type checking...${NC}"
mypy ai_schematic_generator

echo -e "${GREEN}Testing complete!${NC}"