from typing import List

from poke_api.abstract import ControllerABC
from poke_api.repository import (
    DatabaseHandler,
    APIHandler,
    JsonFileHandler
)
from poke_api.schema import PokemonTypeCounter, PokemonTypes


class PokemonController(ControllerABC):

    def __init__(self):
        self.database_handler = DatabaseHandler()
        self.api_handler = APIHandler()
        self.json_handler = JsonFileHandler()
        self.results = []

    async def store_all_results(self) -> None:
        result_list = await self.api_handler.get_data_from_api()
        await self.database_handler.start_database()
        await self.database_handler.store_result(result_list)
        return None

    async def print_all_results_from_db(self) -> None:
        for item in await self.database_handler.all_pokemons():
            print(item)
        return None

    async def query_for_count(self) -> List[PokemonTypeCounter]:
        self.results = await self.database_handler.query_counter()
        return self.results

    async def save_results_json(self) -> None:
        json_result = self.json_handler.pydantic_to_json(self.results)
        self.json_handler.save_to_file(json_result)
        return None

    async def exit(self) -> None:
        await self.database_handler.close()
        return None