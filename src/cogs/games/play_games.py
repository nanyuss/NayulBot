import discord
from discord.ext import commands
from discord import app_commands

import random
from typing import Set

from src import NayulCore
from .internal.shiritori import MainView as MainViewShiritori
from .internal.wordle import MainView as MainViewWordle

class PlayGames(commands.Cog):
    def __init__(self, nayul: NayulCore):
        self.nayul = nayul

    play = app_commands.Group(
        name='jogar',
        description='Grupo de comandos para iniciar e interagir com jogos divertidos.',
        guild_only=True
    )

    @play.command(name='shiritori', description='Forme palavras começando com a última letra da anterior.')
    @app_commands.checks.bot_has_permissions(
        embed_links=True,
        send_messages=True,
        read_messages=True,
        add_reactions=True
    )
    async def shiritori(self, inter: discord.Interaction[NayulCore]):
        """Inicia uma partida de Shiritori."""
        players: Set[discord.Member] = [inter.user]
        view = MainViewShiritori(inter.user,players)

        await inter.response.send_message(
            view=view, 
            allowed_mentions=discord.AllowedMentions(
                users=False,
                roles=False,
                everyone=False
        ))
        await view.start_game_auto(inter)

    @play.command(name='termo', description='Descubra a palavra secreta em até 6 tentativas no jogo Wordle.')
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def wordle(self, inter: discord.Interaction[NayulCore]):
        """Inicia uma partida de Wordle."""

        word = random.choice(list(self.nayul.word_manager.five_letter_words)) # Pega uma palavra aleatória da lista de palavras
        view = MainViewWordle(inter.user, word, [], inter=inter)
        await inter.response.send_message(view=view)

async def setup(nayul: NayulCore):
    await nayul.add_cog(PlayGames(nayul))