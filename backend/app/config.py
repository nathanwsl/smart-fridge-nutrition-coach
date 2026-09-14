"""
Configuration centralisée de l'application.
Toutes les valeurs sensibles (clés, secrets) viennent du fichier .env
et ne doivent JAMAIS être écrites en dur ici.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    themealdb_base_url: str = "https://www.themealdb.com/api/json/v1/1"
    usda_api_key: str = ""
    usda_base_url: str = "https://api.nal.usda.gov/fdc/v1"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Cache la config pour éviter de relire le .env à chaque appel."""
    return Settings()