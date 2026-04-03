from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_name: str = "./model_cache/AI-ModelScope/bge-small-zh-v1.5"
    model_cache_dir: str = "./model_cache"
    intents_file: str = "./intents/intents.yaml"
    default_threshold: float = 0.5
    host: str = "0.0.0.0"
    port: int = 8765
    log_level: str = "info"

    class Config:
        env_file = ".env"

settings = Settings()