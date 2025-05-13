import discord
import logging
from discord.ext import commands
from discord.app_commands.errors import (
	BotMissingPermissions,
	MissingPermissions,
)

from bot import BotCore
from bot.utils.others import Permissions, Emoji

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class CommandHandler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.tree.on_error = self.on_app_command_error
		
	async def on_app_command_error(self, inter: discord.Interaction[BotCore], error: Exception): #Função que trata erros nos comandos slash.
		_P = Permissions()
		
		if inter.command is not None: #Verifica se o comando existe (para não dar erro 404)
			if inter.command._has_any_error_handlers():
				return None
		
		if isinstance(error, MissingPermissions): #Tratamento do erro de permissão do usuário.
			perms = '\n'.join(sorted([_P.get(name) for name in error.missing_permissions if _P.get(name)]))
			
			if len(perms) == 1:
				message = f'{Emoji.error}┃Você precisa da seguinte permissão para esse comando:\n**{perms}**'
			else:
				message = f'{Emoji.error}┃Você precisa das seguintes permissões para esse comando:\n**{perms}**'
		
		elif isinstance(error, BotMissingPermissions): #Tratamento do erro de permissão dos bots.
			perms = '\n'.join(sorted([_P.get(name) for name in error.missing_permissions if _P.get(name)]))
			
			if len(perms)==1:
				message = f'{Emoji.error}┃Preciso da seguinte permissão para esse comando:\n**{perms}**'
			else:
				message = f'{Emoji.error}┃Preciso das seguintes permissões para esse comando:\n**{perms}**'
		
		else: #Caso o erro não tenha um tratamento.
			message = f'{Emoji.error}┃Erro desconhecido ao executar o comando!\n```{error}```'
			log.exception('Erro no comando:', exc_info=error)
			
		if inter.response.is_done(): #Verifica se o comando já foi respondido.
			await inter.followup.send(message, ephemeral=True)
		else:
			await inter.response.send_message(message, ephemeral=True)
		
async def setup(bot: commands.Bot):
	await bot.add_cog(CommandHandler(bot))