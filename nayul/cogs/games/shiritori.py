import discord
from discord.ext import commands
from discord import app_commands

from typing import Set

from nayul import NayulCore
from .internal.shiritori import MainView


class Shiritori(commands.Cog):
    def __init__(self, nayul: NayulCore):
        self.nayul = nayul

    @app_commands.guild_only()
    @app_commands.command(name='shiritori', description='Inicia uma partida de Shiritori.')
    @app_commands.checks.bot_has_permissions(
        embed_links=True,
        send_messages=True,
        read_messages=True,
        add_reactions=True
    )
    async def shiritori(self, inter: discord.Interaction[NayulCore]):
        """Inicia uma partida de Shiritori."""
        players: Set[discord.Member] = [inter.user]
        view = MainView(inter.user,players)

        await inter.response.send_message(
            view=view, 
            allowed_mentions=discord.AllowedMentions(
                users=False,
                roles=False,
                everyone=False
        ))
        await view.start_game_auto(inter)

async def setup(nayul: NayulCore):
    await nayul.add_cog(Shiritori(nayul))