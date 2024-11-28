from setuptools import setup, find_packages

setup(
    name="ai-schematic-generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "anthropic",
        "schemdraw",
        "numpy",
        "click",
        "rich",
    ],
    entry_points={
        'console_scripts': [
            'ai_schematics=ai_schematic_generator.cli:cli',
        ],
    },
)
