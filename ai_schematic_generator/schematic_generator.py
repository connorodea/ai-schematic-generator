import schemdraw
from schemdraw import elements as elm
from schemdraw.segments import *
import json
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import numpy as np

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
            elem = elm.Resistor2().label(f'{component.id}\n{component.value}')
        elif component.type == 'capacitor':
            elem = elm.Capacitor2().label(f'{component.id}\n{component.value}')
        elif component.type == 'inductor':
            elem = elm.Inductor2().label(f'{component.id}\n{component.value}')
        elif component.type == 'diode':
            elem = elm.Diode2().label(component.id)
        elif component.type == 'transistor':
            elem = elm.BjtNpn().label(component.id)
        else:
            raise ValueError(f"Unknown component type: {component.type}")
            
        # Position and rotate the component
        elem.at(component.position).rotate(component.rotation)
        self.drawing.add(elem)
    
    def add_connection(self, start_component: str, end_component: str):
        """Add a wire connection between components."""
        self.connections.append((start_component, end_component))
        
        # Get the components' positions
        start_pos = self.components[start_component].position
        end_pos = self.components[end_component].position
        
        # Draw the wire
        self.drawing.add(elm.Line().start(start_pos).end(end_pos))
    
    def from_json(self, json_data: str):
        """Load schematic from JSON description."""
        data = json.loads(json_data)
        
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
        self.drawing.save(filename)
