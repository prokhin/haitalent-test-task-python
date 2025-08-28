import os
from app.core.config import Settings

def test_settings_accepts_extra_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./temp.db")
    monkeypatch.setenv("TEST_DATABASE_URL", "sqlite:///./temp_test.db")
    # Extra variable should not raise an error
    monkeypatch.setenv("UNUSED_VAR", "value")
    settings = Settings()
    assert settings.DATABASE_URL.endswith("temp.db")
    assert settings.TEST_DATABASE_URL.endswith("temp_test.db")
