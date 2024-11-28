import pytest
import os
from ai_schematic_generator.ai_generator import AISchematicGenerator
from ai_schematic_generator.schematic_generator import Component

@pytest.mark.integration
class TestIntegration:
    @pytest.fixture
    def api_key(self):
        """Get API key from environment."""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            pytest.skip("API key not available")
        return api_key
    
    @pytest.fixture
    def mock_response(self):
        """Mock API response."""
        return {
            "components": [
                {
                    "type": "resistor",
                    "id": "R1",
                    "value": "10k",
                    "position": [0, 0]
                },
                {
                    "type": "resistor",
                    "id": "R2",
                    "value": "10k",
                    "position": [2, 0]
                }
            ],
            "connections": [
                {
                    "start": "R1",
                    "end": "R2"
                }
            ]
        }
    
    @pytest.mark.asyncio
    async def test_full_workflow(self, api_key, tmp_path, mock_anthropic_client):
        """Test complete workflow from description to schematic."""
        generator = AISchematicGenerator(api_key)
        output_file = tmp_path / "test_output.svg"  # Use .svg extension
        
        result = await generator.generate_schematic_from_description(
            "Create a voltage divider with two 10k resistors",
            str(output_file)
        )
        
        assert "Successfully" in result
        assert output_file.exists()

    @pytest.mark.asyncio
    async def test_complex_circuit(self, api_key, tmp_path, mock_anthropic_client):
        """Test generating a more complex circuit."""
        generator = AISchematicGenerator(api_key)
        output_file = tmp_path / "complex_output.svg"  # Use .svg extension
        
        result = await generator.generate_schematic_from_description(
            """Create an astable multivibrator circuit with:
            - Two 2N3904 transistors
            - Two 10k collector resistors
            - Two 100k base resistors
            - Two 10µF coupling capacitors""",
            str(output_file)
        )
        
        assert "Successfully" in result
        assert output_file.exists()
