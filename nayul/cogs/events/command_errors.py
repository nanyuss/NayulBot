import discord
import logging
from discord.ext import commands
from discord.app_commands.errors import (
	BotMissingPermissions,
	MissingPermissions,
)

from nayul import NayulCore
from nayul.utils.emojis import Emoji
from nayul.utils.others import Permissions


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class GlobalErrorHandler(commands.Cog):
	def __init__(self, nayul: NayulCore):
		"""Classe que trata os erros dos comandos do bot."""
		self.nayul = nayul
		self.nayul.tree.on_error = self.on_app_command_error
		
	async def on_app_command_error(self, inter: discord.Interaction[NayulCore], error: Exception):
		"""Função que trata os erros dos comandos do bot"""
		_P = Permissions()
		
		if inter.command is not None: #Verifica se o comando existe (para não dar erro 404)
			if inter.command._has_any_error_handlers():
				return None
		
		if isinstance(error, MissingPermissions): #Tratamento do erro de permissão do usuário.
			perms = '\n'.join(sorted([_P.get(name) for name in error.missing_permissions if _P.get(name)]))
			
			if len(perms) == 1:
				message = (
					f'{Emoji.error} Permissão insuficiente!Você precisa da seguinte permissão para executar este comando:\n'
					f'**{perms}**'
				)
			else:
				message = (
					f'{Emoji.error} Permissão insuficiente!Você precisa das seguintes permissões para executar este comando:\n'
					f'**{perms}**'
				)
		
		elif isinstance(error, BotMissingPermissions): #Tratamento do erro de permissão dos bots.
			perms = '\n'.join(sorted([_P.get(name) for name in error.missing_permissions if _P.get(name)]))
			
			if len(perms)==1:
				message = (
					f'{Emoji.error} Preciso da seguinte permissão para esse comando:\n'
					f'**{perms}**'
				)
			else:
				message = (
					f'{Emoji.error} Preciso das seguintes permissões para esse comando:\n'
					f'**{perms}**'
				)
		
		else: #Caso o erro não tenha um tratamento.
			message = (
				f"{Emoji.error} Ocorreu um erro inesperado ao executar.\n"
        		f"-# Se o problema persistir, reporte ao desenvolvedor.\n"
        		f"```{error}```"
			)
			log.exception('Erro no comando:', exc_info=error)
			
		if inter.response.is_done(): #Verifica se o comando já foi respondido.
			await inter.followup.send(message, ephemeral=True)
		else:
			await inter.response.send_message(message, ephemeral=True)

	@commands.Cog.listener()
	async def on_command_error(self, ctx: commands.Context, error: Exception):
		"""Função que trata os erros dos comandos do bot"""
		if isinstance(error, commands.NotOwner):
			log.info(f'{ctx.author.name} ({ctx.author.id}) tentou usar um comando de desenvolvedor.')
			return
		
async def setup(nayul: NayulCore):
	await nayul.add_cog(GlobalErrorHandler(nayul))