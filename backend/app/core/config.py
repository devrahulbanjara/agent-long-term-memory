from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    GROQ_API_KEY: str
    GEMINI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra variables in the .env file that are not defined in the class
    )


settings = Setting()
