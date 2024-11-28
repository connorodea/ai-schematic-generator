import pytest
from click.testing import CliRunner
from ai_schematic_generator.cli import cli
import asyncio
from pathlib import Path
import click

class TestCLI:
    @pytest.fixture
    def runner(self):
        """Create a CLI runner for testing."""
        return CliRunner(mix_stderr=False)

    @pytest.fixture
    async def mock_loop(self):
        """Create a mock event loop that always succeeds."""
        loop = asyncio.new_event_loop()
        return loop
        
    def test_cli_help(self, runner):
        """Test CLI help command."""
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'generate' in result.output
        assert 'analyze' in result.output

    def test_generate_command(self, runner, mock_anthropic_client, monkeypatch):
        """Test generate command with mock API."""
        monkeypatch.setenv('ANTHROPIC_API_KEY', 'dummy-key')
        
        # Mock the event loop and its run_until_complete
        async def mock_coro(*args, **kwargs):
            return "Successfully generated schematic"
            
        mock_loop = asyncio.new_event_loop()
        mock_loop.run_until_complete(mock_coro())
        monkeypatch.setattr(asyncio, 'get_event_loop', lambda: mock_loop)
        
        # Mock the generator
        def mock_generator(*args, **kwargs):
            async def mock_gen():
                return "Successfully generated schematic"
            return mock_gen()
            
        monkeypatch.setattr('ai_schematic_generator.ai_generator.AISchematicGenerator.generate_schematic_from_description', 
                           mock_generator)

        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                'generate',
                'voltage divider with two 10k resistors',
                '-o', 'test_output.svg'
            ], catch_exceptions=False)
            assert result.exit_code == 0
            assert 'Generation Complete' in result.stdout

    def test_missing_api_key(self, runner, monkeypatch):
        """Test error handling when API key is missing."""
        monkeypatch.delenv('ANTHROPIC_API_KEY', raising=False)
        
        result = runner.invoke(cli, [
            'generate',
            'voltage divider'
        ])
        assert result.exit_code == 1
        assert 'API Key Error' in str(result.stdout)

    def test_generate_error_handling(self, runner, mock_anthropic_client, monkeypatch):
        """Test error handling in generate command."""
        monkeypatch.setenv('ANTHROPIC_API_KEY', 'dummy-key')
        
        # Mock the generator to raise an error
        def mock_generator(*args, **kwargs):
            async def mock_gen():
                raise Exception("Test error")
            return mock_gen()
            
        monkeypatch.setattr('ai_schematic_generator.ai_generator.AISchematicGenerator.generate_schematic_from_description', 
                           mock_generator)

        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                'generate',
                'voltage divider',
                '-o', 'test_output.svg'
            ])
            assert result.exit_code == 1
            assert 'Error: Test error' in str(result.stdout)

    def test_analyze_command(self, runner, mock_anthropic_client, monkeypatch, tmp_path):
        """Test analyze command."""
        monkeypatch.setenv('ANTHROPIC_API_KEY', 'dummy-key')
        
        # Create a dummy file to analyze
        test_file = tmp_path / "test.svg"
        test_file.write_text("<svg></svg>")
        
        # Mock the analyzer
        def mock_analyzer(*args, **kwargs):
            async def mock_analyze():
                return "Schematic analysis complete"
            return mock_analyze()
            
        monkeypatch.setattr('ai_schematic_generator.ai_generator.AISchematicGenerator.analyze_existing_schematic', 
                           mock_analyzer)
        
        # Mock event loop
        mock_loop = asyncio.new_event_loop()
        monkeypatch.setattr(asyncio, 'get_event_loop', lambda: mock_loop)
        
        result = runner.invoke(cli, [
            'analyze',
            str(test_file)
        ], catch_exceptions=False)
        assert result.exit_code == 0
        assert 'Schematic Analysis' in str(result.stdout)
