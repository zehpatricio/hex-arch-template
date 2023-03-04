from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Hex-Arch"
    db_url: str

    class Config:
        env_file = ".env"
