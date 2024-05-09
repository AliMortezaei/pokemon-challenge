from typing import List, Tuple
import json
import os
import sqlite3
import asyncio


import httpx
from tortoise import Tortoise
from tortoise.functions import Count


from poke_api.schema import PokemonTypes, PokemonTypeCounter
from poke_api.config import settings
from poke_api.models import PokemonModel
from poke_api.abstract import (
    APIHandlerABC,
    DatabaseHandlerABC,
    JsonFileHandlerABC
)


class APIHandler(APIHandlerABC):
    def __init__(self):
        self._data = None

    async def get_single_pokemon_data(
        self, client: httpx.AsyncClient, name: str
    ) -> Tuple[list, str]:
        
        resp = await client.get(f"{settings.BASE_API_URL}/pokemon/{name}")
        return (resp.json()["types"], name)

    async def get_data_from_api(self) -> List[PokemonTypes]:
        if self._data is not None:
            return self._data
        temp = {}
        self._data = []
        async with httpx.AsyncClient() as client:
            tasks = [
                self.get_single_pokemon_data(client, name)
                for name in settings.POKEMON_NAMES
            ]
            responses = await asyncio.gather(*tasks)
            for resp, name in responses:
                temp[name] = list(name["type"]["name"] for name in resp)
            for key, value in temp.items():
                for item in value:
                    self._data.append(
                        PokemonTypes(pokemon_name=key, pokemon_type=item)
                    )
        return self._data


class DatabaseHandler(DatabaseHandlerABC):

    async def _orm_up(self) -> None:

        await Tortoise.init(config=settings.TORTOISE_ORM_CONF)
        await Tortoise.generate_schemas()
        return None

    async def store_result(self, result: List[PokemonTypes]) -> None:
        await PokemonModel.bulk_create(
            [PokemonModel(**item.model_dump()) for item in result]
        )
        return None

    async def all_pokemons(self) -> List[PokemonTypes.dict]:
        return await PokemonModel.all().values_list(
            "id","pokemon_name", "pokemon_type"
        )

    async def start_database(self) -> None:
        conn = sqlite3.connect(settings.DATABASE_URL)
        conn.executescript("""
        DROP TABLE IF EXISTS pokemon_types;
        """)
        conn.close()
        await self._orm_up()
        return None

    async def close(self) -> None:
        await Tortoise.close_connections()
        return None

    async def query_counter(self) -> List[PokemonTypeCounter]:
        result = await PokemonModel.all().annotate(
            type_count=Count('pokemon_type')
        ).group_by("pokemon_type").values("pokemon_type", "type_count")
        return [
            PokemonTypeCounter(**item) for item in result
        ]


class JsonFileHandler(JsonFileHandlerABC):
    def pydantic_to_json(self, result: List[PokemonTypeCounter]):
        json_data = json.dumps(
            {counter.pokemon_type: counter.type_count for counter in result}
        )
        return json_data

    def save_to_file(self, data):
        file_path = os.path.join(os.getcwd(), "result.json")

        try:
            with open(file_path, "w") as file:
                file.write(data)
            print(f"Data saved to {file_path} successfully.")
        except IOError as error:
            print(
                "An error occurred while saving the data to"
                f"{file_path}: {error}"
            )