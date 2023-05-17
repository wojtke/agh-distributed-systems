from pydantic import BaseSettings


class Settings(BaseSettings):
    HOST: str = "localhost"
    PORT: int = 8989
    DEBUG: bool = True
    SPOONACULAR_API_KEY: str
    OPENAI_API_KEY: str

    class Config:
        env_file = "./.env"


settings = Settings()
