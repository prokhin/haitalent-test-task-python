from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Настройки подключения к базе данных
    DATABASE_URL: str
    TEST_DATABASE_URL: str

    # Настройки для pydantic-settings
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
