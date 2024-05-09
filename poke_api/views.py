from poke_api.controller import PokemonController
from poke_api.abstract import PokemonViewABC


class PokemonView(PokemonViewABC):

    def __init__(self, controller: PokemonController):
        self.controller = controller()

    async def execute(self) -> None:
        await self.controller.store_all_results()
        await self.controller.print_all_results_from_db()
        await self.controller.query_for_count()
        await self.controller.save_results_json()
        await self.controller.exit()
        return None