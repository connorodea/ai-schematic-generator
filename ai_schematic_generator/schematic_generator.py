import schemdraw
from schemdraw import elements as elm
from dataclasses import dataclass
from typing import List, Optional, Tuple
import json
import math
import os

@dataclass
class Component:
    type: str
    id: str
    value: Optional[str] = None
    position: Tuple[float, float] = (0, 0)
    rotation: float = 0
    connections: List[str] = None

class SchematicGenerator:
    def __init__(self):
        self.components = {}
        self.connections = []
        self.drawing = schemdraw.Drawing()
    
    def add_component(self, component: Component):
        """Add a component to the schematic."""
        self.components[component.id] = component
        
        # Create the component based on its type
        if component.type == 'resistor':
            elem = elm.Resistor()
        elif component.type == 'capacitor':
            elem = elm.Capacitor()
        elif component.type == 'inductor':
            elem = elm.Inductor()
        elif component.type == 'diode':
            elem = elm.Diode()
        elif component.type == 'transistor':
            elem = elm.BjtNpn()
        else:
            raise ValueError(f"Unknown component type: {component.type}")
            
        # Position the component
        elem = elem.at(component.position)
        
        # Apply rotation if needed
        if component.rotation != 0:
            theta = math.radians(component.rotation)
            direction = (math.cos(theta), math.sin(theta))
            elem = elem.to((
                component.position[0] + direction[0],
                component.position[1] + direction[1]
            ))
            
        # Add label
        if component.value:
            elem = elem.label(f'{component.id}\n{component.value}')
        else:
            elem = elem.label(component.id)
            
        self.drawing.add(elem)
    
    def add_connection(self, start_component: str, end_component: str):
        """Add a wire connection between components."""
        self.connections.append((start_component, end_component))
        start_pos = self.components[start_component].position
        end_pos = self.components[end_component].position
        self.drawing.add(elm.Line().at(start_pos).to(end_pos))
    
    def from_json(self, json_str: str):
        """Load schematic from JSON description."""
        data = json.loads(json_str)
        
        # Add components
        for comp in data.get('components', []):
            component = Component(
                type=comp['type'],
                id=comp['id'],
                value=comp.get('value'),
                position=tuple(comp.get('position', (0, 0))),
                rotation=comp.get('rotation', 0)
            )
            self.add_component(component)
        
        # Add connections
        for conn in data.get('connections', []):
            self.add_connection(conn['start'], conn['end'])
    
    def save(self, filename: str):
        """Save the schematic to a file."""
        # Ensure file extension is .svg
        base, ext = os.path.splitext(filename)
        if not ext or ext.lower() != '.svg':
            filename = base + '.svg'
            
        self.drawing.save(filename)
        return filename
