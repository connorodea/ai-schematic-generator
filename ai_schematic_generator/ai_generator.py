import anthropic
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
        schema = '''{
    "components": [
        {
            "type": "resistor|capacitor|inductor|diode|transistor",
            "id": "unique_id",
            "value": "component_value",
            "position": [0, 0],
            "rotation": 0
        }
    ],
    "connections": [
        {
            "start": "component_id_1",
            "end": "component_id_2"
        }
    ]
}'''

        return f"""Based on the following circuit description, generate a JSON specification:
Description: {description}

Use this schema:
{schema}

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
                prompt = self._generate_circuit_prompt(description)
                response = await self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=2000,
                    temperature=0,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )
                
                self.schematic_generator.from_json(response.content)
                self.schematic_generator.save(output_file)
                
                return f"Successfully generated schematic: {output_file}"
                
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Failed to generate schematic after {max_retries} attempts: {str(e)}")
                continue
        
        return "Failed to generate schematic"
