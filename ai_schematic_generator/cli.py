#!/usr/bin/env python3
import click
import os
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from pathlib import Path
from .ai_generator import AISchematicGenerator

console = Console()

def check_api_key():
    """Check if the Anthropic API key is set."""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        console.print(Panel(
            "[red]ERROR: ANTHROPIC_API_KEY environment variable not set[/red]\n"
            "Please set your API key:\n"
            "export ANTHROPIC_API_KEY='your-api-key-here'",
            title="API Key Error"
        ))
        exit(1)
    return api_key

@click.group()
def cli():
    """AI-powered electronic schematic generator using Claude 3.5 Sonnet."""
    pass

@cli.command()
@click.argument('description', type=str)
@click.option('--output', '-o', default='schematic.png', help='Output file path')
def generate(description: str, output: str):
    """Generate a schematic from a natural language description."""
    api_key = check_api_key()
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Generating schematic...", total=100)
        
        async def run():
            generator = AISchematicGenerator(api_key)
            result = await generator.generate_schematic_from_description(
                description,
                output
            )
            return result
            
        result = asyncio.run(run())
        
    console.print(Panel(result, title="Generation Complete"))

@cli.command()
@click.argument('image_path', type=click.Path(exists=True))
def analyze(image_path: str):
    """Analyze an existing schematic image."""
    api_key = check_api_key()
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Analyzing schematic...", total=100)
        
        async def run():
            generator = AISchematicGenerator(api_key)
            analysis = await generator.analyze_existing_schematic(image_path)
            return analysis
            
        result = asyncio.run(run())
        
    console.print(Panel(result, title="Schematic Analysis"))

if __name__ == '__main__':
    cli()
