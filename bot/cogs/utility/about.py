import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

import time
import psutil
import platform
from datetime import timedelta

from bot import BotCore

class SelectPatchNotes(ui.Select):
    """Classe que representa um select para as notas de versão do bot."""

    def __init__(self):
        options = [
            discord.SelectOption(label='Versão 0.1.0 (Atual)', value='v0.1.0', description='Atualizado em 01/10/2023'),
        ]
        super().__init__(placeholder='Selecione uma versão...', options=options)

    async def callback(self, inter: discord.Interaction[BotCore]):
        """Callback do select que mostra as notas de versão."""

        await inter.response.send_message('Nenhuma nota de versão encontrada.', ephemeral=True)

class PatchNotesView(ui.View):
    """Classe que representa uma view para as notas de versão do bot."""

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectPatchNotes())

    async def on_timeout(self):
        """Callback quando a view expira."""
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

class AboutBot(commands.Cog):
    """Classe que contém os comandos de utilidade do bot."""

    def __init__(self, bot: BotCore):
        self.bot = bot

    @app_commands.command(name='ping', description='Mostra informações sobre a latência do bot.')
    async def ping(self, inter: discord.Interaction[BotCore]):
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
    async def botinfo(self, inter: discord.Interaction[BotCore]):
        """Comando que mostra informações sobre o bot."""

        embed = discord.Embed(title=f'Informações sobre {inter.client.user.name}', color=discord.Color.blurple())
        embed.description = (
            f'```yaml\n'
            f'SO:               {platform.system()} {platform.release()}\n'
            f'Python:           {platform.python_version()}\n'
            f'Discord.py:       {discord.__version__}\n'
            f'Versão:           {inter.client.__version__}\n'
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
                f'**Uptime:** `{str(timedelta(seconds=int(time.time() - self.bot.uptime)))}`\n'
                f'**Latência:** `{round(inter.client.latency * 1000)}ms`\n'
                f'**CPU:** `{psutil.cpu_percent()}%`\n'
                f'**Memória:** `{round(psutil.virtual_memory().percent, 2)}%`'
            ),
            inline=False
        )
        embed.add_field(
            name='📌 Links',
            value=(
                '[discord.py](https://discordpy.readthedocs.io/en/stable/api.html)\n'
                '[MongoDB](https://www.mongodb.com/)\n'
                '[Nanyus (dev)](https://github.com/nanyuss)'
            ),
            inline=False
        )

        owner = inter.client.get_user(list(inter.client.owner_ids)[0])

        embed.set_footer(
            text=f'Desenvolvida por {owner.name} ({owner.id})',
            icon_url=owner.display_avatar.url
        )

        await inter.response.send_message(embed=embed)

async def setup(bot: BotCore):
    await bot.add_cog(AboutBot(bot))