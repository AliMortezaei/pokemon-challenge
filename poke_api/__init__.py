from poke_api.views import PokemonView
from poke_api.controller import PokemonController

async def main():
    await PokemonView(PokemonController).execute()