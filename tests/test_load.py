import pytest

@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    # Define variáveis de ambiente fictícias
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", "/fake/path/to/fake_credentials.json")
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "fake_project_id")
