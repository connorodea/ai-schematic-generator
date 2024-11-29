#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Running tests with coverage...${NC}"

# Clean up old coverage data
rm -f .coverage*

# Run tests with coverage
python -m pytest

# Generate coverage report
echo -e "\n${BLUE}Generating coverage summary...${NC}"
python tools/test_summary.py

echo -e "\n${GREEN}Coverage report generated${NC}"
echo "See htmlcov/index.html for detailed report"
