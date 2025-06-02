import discord
from discord.ext import commands
from discord import app_commands

import time
import psutil
import platform
from datetime import timedelta

import nayul
from nayul import NayulCore

class AboutBot(commands.Cog):
    """Classe que contém os comandos de utilidade do bot."""

    def __init__(self, nayul: NayulCore):
        self.nayul = nayul

    @app_commands.command(name='ping', description='Mostra informações sobre a latência do bot.')
    async def ping(self, inter: discord.Interaction[NayulCore]):
        """Comando que verifica a latência do bot."""

        start = time.perf_counter()
        await inter.response.send_message('🏓 | Ping...')
        end = time.perf_counter()

        ws_latency = round(inter.client.latency * 1000)
        api_latency = round((end - start) * 1000)

        await inter.edit_original_response(
            content=f'🏓 | Pong!\n'
                    f'**Latência do WebSocket:** {ws_latency}ms\n'
                    f'**Latência da API:** {api_latency}ms\n'
                    )

    @app_commands.command(name='botinfo', description='Mostra informações sobre o bot.')
    async def botinfo(self, inter: discord.Interaction[NayulCore]):
        """Comando que mostra informações sobre o bot."""

        embed = discord.Embed(title=f'Informações sobre {inter.client.user.name}', color=discord.Color.blurple())
        embed.description = (
            f'```yaml\n'
            f'SO:               {platform.system()} {platform.release()}\n'
            f'Python:           {platform.python_version()}\n'
            f'Discord.py:       {discord.__version__}\n'
            f'Versão:           {nayul.__version__}\n'
            f'```'
        )
        embed.set_thumbnail(url=inter.client.user.display_avatar.url)

        embed.add_field(
            name='📊 Estatísticas',
            value=(
                f'**Servidores:** `{len(inter.client.guilds)}`\n'
                f'**Usuários:** `{len(set(inter.client.users))}`\n'
                f'**Comandos:** `{len(inter.client.tree.get_commands())}`\n'
            ),
            inline=False
        )
        embed.add_field(
            name='⚙️ Desempenho',
            value=(
                f'**Uptime:** `{str(timedelta(seconds=int(time.time() - inter.client.uptime)))}`\n'
                f'**Latência:** `{round(inter.client.latency * 1000)}ms`\n'
                f'**CPU:** `{psutil.cpu_percent()}%`\n'
                f'**Memória:** `{round(psutil.virtual_memory().percent, 2)}%`'
            ),
            inline=False
        )

        owner = inter.client.get_user(list(inter.client.owner_ids)[0])

        embed.set_footer(
            text=f'Desenvolvida por {owner.name} ({owner.id})',
            icon_url=owner.display_avatar.url
        )

        await inter.response.send_message(embed=embed)

async def setup(nayul: NayulCore):
    await nayul.add_cog(AboutBot(nayul))