import pytest
from ai_schematic_generator.ai_generator import AISchematicGenerator

class TestAISchematicGenerator:
    @pytest.fixture
    def ai_generator(self, mock_anthropic_client):
        """Create an AISchematicGenerator instance for testing."""
        return AISchematicGenerator("dummy-api-key")

    def test_generate_circuit_prompt(self, ai_generator):
        """Test prompt generation."""
        description = "voltage divider with two 10k resistors"
        prompt = ai_generator._generate_circuit_prompt(description)
        assert description in prompt
        assert "JSON" in prompt
