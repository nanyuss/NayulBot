import discord
from discord.ext import commands
from discord import app_commands

class Profile(commands.Cog):
    def __init__(self, nayul):
        self.nayul = nayul

    @app_commands.command(name='profile', description='Mostra o perfil de um usuário.')
    @app_commands.describe(member='O membro para ver o perfil.')
    async def profile(self, inter: discord.Interaction, member: discord.Member = None):

        await inter.response.send_message('teste')

async def setup(nayul):
    await nayul.add_cog(Profile(nayul))