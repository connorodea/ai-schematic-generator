import anthropic
import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from .schematic_generator import SchematicGenerator, Component

class AISchematicGenerator:
    def __init__(self, api_key: str):
        """Initialize the AI Schematic Generator with Anthropic API key."""
        self.client = anthropic.Anthropic(api_key=api_key)
        self.schematic_generator = SchematicGenerator()
        
    def _generate_circuit_prompt(self, description: str) -> str:
        """Generate a structured prompt for the LLM."""
        return f"""Based on the following circuit description, generate a JSON specification that follows this schema:

{
    "components": [
        {
            "type": "resistor|capacitor|inductor|diode|transistor",
            "id": "unique_id",
            "value": "component_value",
            "position": [x, y],
            "rotation": degrees
        }
    ],
    "connections": [
        {
            "start": "component_id_1",
            "end": "component_id_2"
        }
    ]
}

Description: {description}

Provide only the JSON output without any additional text or explanation."""

    async def generate_schematic_from_description(
        self, 
        description: str, 
        output_file: str,
        max_retries: int = 3
    ) -> str:
        """Generate a schematic from a natural language description."""
        for attempt in range(max_retries):
            try:
                # Generate the circuit specification using Claude
                prompt = self._generate_circuit_prompt(description)
                response = await self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=2000,
                    temperature=0,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                
                # Generate the schematic
                self.schematic_generator.from_json(response.content)
                self.schematic_generator.save(output_file)
                
                return f"Successfully generated schematic: {output_file}"
                
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Failed to generate schematic after {max_retries} attempts: {str(e)}")
                continue

    async def analyze_existing_schematic(self, image_path: str) -> str:
        """Analyze an existing schematic image."""
        with open(image_path, 'rb') as img:
            response = await self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this electronic schematic and provide a detailed description."
                            },
                            {
                                "type": "image",
                                "source": {
                                    "type": "bytes",
                                    "data": img.read()
                                }
                            }
                        ]
                    }
                ]
            )
        return response.content
