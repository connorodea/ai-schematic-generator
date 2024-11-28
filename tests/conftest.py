import pytest
from unittest.mock import MagicMock, AsyncMock
import anthropic
import json
import asyncio

@pytest.fixture
def mock_anthropic_client(monkeypatch):
    """Mock Anthropic client for testing."""
    mock_client = MagicMock(spec=anthropic.Anthropic)
    
    # Create async mock for messages.create
    mock_messages = AsyncMock()
    mock_response = MagicMock()
    mock_response.content = json.dumps({
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
    })
    
    mock_messages.create = AsyncMock(return_value=mock_response)
    mock_client.messages = mock_messages
    
    monkeypatch.setattr('anthropic.Anthropic', lambda *args, **kwargs: mock_client)
    return mock_client

@pytest.fixture(scope='function')
def event_loop(request):
    """Create a new event loop for each test."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
