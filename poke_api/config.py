

from typing import List


class Settings:

    DATABASE_URL: str = "./database.db"
    # Docs https://pokeapi.co/
    BASE_API_URL: str = "https://pokeapi.co/api/v2"

    # Name Pokemon 
    POKEMON_NAMES: List[str] = [
        "bulbasaur",
        "pidgeot",
        "charizard",
        "pikachu",
        "psyduck",
        "sandslash",
        "wartortle",
        "vileplume",
        "arcanine",
        "dugtrio",
        "vileplume",
        "growlithe",
        "onix",
        "cloyster",
        "raticate",
   
    ]

    TORTOISE_ORM_CONF: dict = {
        "connections": {
            "default": {
                "engine": "tortoise.backends.sqlite",
                "credentials": {
                    "file_path": DATABASE_URL
                }
            }
        },
        "apps": {
            "models": {
                "models": ["poke_api.models"],
                "default_connection": "default"
            }
        }
    }

settings = Settings()

