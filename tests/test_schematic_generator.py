import pytest
from ai_schematic_generator.schematic_generator import SchematicGenerator, Component

class TestSchematicGenerator:
    @pytest.fixture
    def generator(self):
        """Create a SchematicGenerator instance for testing."""
        return SchematicGenerator()

    def test_add_component(self, generator):
        """Test adding different types of components."""
        components = [
            Component("resistor", "R1", value="10k", position=(0, 0)),
            Component("capacitor", "C1", value="100nF", position=(2, 0)),
            Component("inductor", "L1", value="1mH", position=(4, 0))
        ]
        
        for comp in components:
            generator.add_component(comp)
            assert comp.id in generator.components
            
    def test_invalid_component_type(self, generator):
        """Test adding an invalid component type."""
        with pytest.raises(ValueError):
            generator.add_component(Component("invalid_type", "X1"))
            
    def test_component_with_rotation(self, generator):
        """Test adding a component with rotation."""
        comp = Component("resistor", "R1", value="10k", position=(0, 0), rotation=90)
        generator.add_component(comp)
        assert comp.id in generator.components

    def test_add_connection(self, generator):
        """Test adding connections between components."""
        # Add two components
        r1 = Component("resistor", "R1", position=(0, 0))
        r2 = Component("resistor", "R2", position=(2, 0))
        generator.add_component(r1)
        generator.add_component(r2)
        
        # Connect them
        generator.add_connection("R1", "R2")
        assert ("R1", "R2") in generator.connections
