import pytest
from src.extract.extract import fetch_data

@pytest.fixture
def mock_response():
    return {
        'response': [{'id': 1, 'name': 'test'}]
    }

def test_fetch_data(monkeypatch, mock_response):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def json(self):
                return mock_response
        return MockResponse()

    monkeypatch.setattr('requests.get', mock_get)
    result = fetch_data('some/path', {})
    assert len(result) == 1
    assert result[0]['name'] == 'test'
