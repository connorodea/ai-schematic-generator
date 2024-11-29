import anthropic
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from .schematic_generator import SchematicGenerator, Component
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AISchematicGenerator:
    def __init__(self, api_key: str):
        """Initialize the AI Schematic Generator with Anthropic API key."""
        self.client = anthropic.Anthropic(api_key=api_key)
        self.schematic_generator = SchematicGenerator()
        logger.info("Initialized AI Schematic Generator")
    
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

        prompt = f"""Based on the following circuit description, generate a JSON specification:
Description: {description}

Use this schema:
{schema}

Provide only the JSON output without any additional text or explanation."""
        
        logger.debug(f"Generated prompt for description: {description}")
        return prompt

    async def generate_schematic_from_description(
        self, 
        description: str, 
        output_file: str,
        max_retries: int = 3
    ) -> str:
        """Generate a schematic from a natural language description."""
        logger.info(f"Generating schematic for description: {description}")
        
        for attempt in range(max_retries):
            try:
                prompt = self._generate_circuit_prompt(description)
                logger.debug("Sending request to Anthropic API")
                
                response = await self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=2000,
                    temperature=0,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )
                
                logger.debug("Processing API response")
                self.schematic_generator.from_json(response.content)
                self.schematic_generator.save(output_file)
                
                logger.info(f"Successfully generated schematic: {output_file}")
                return f"Successfully generated schematic: {output_file}"
                
            except Exception as e:
                logger.error(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                if attempt == max_retries - 1:
                    msg = f"Failed to generate schematic after {max_retries} attempts: {str(e)}"
                    logger.error(msg)
                    raise Exception(msg)
                continue
        
        return "Failed to generate schematic"

    async def analyze_existing_schematic(self, image_path: str) -> str:
        """Analyze an existing schematic image."""
        logger.info(f"Analyzing schematic: {image_path}")
        
        try:
            with open(image_path, 'rb') as img:
                logger.debug("Sending request to Anthropic API for analysis")
                response = await self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=2000,
                    messages=[{
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
                                    "data": img.read(),
                                    "media_type": "image/svg+xml"
                                }
                            }
                        ]
                    }]
                )
                
            logger.info("Successfully analyzed schematic")
            return response.content
            
        except Exception as e:
            msg = f"Failed to analyze schematic: {str(e)}"
            logger.error(msg)
            raise Exception(msg)
