import discord
from discord.ext import commands

import os
import logging
import asyncio
import aiohttp
from time import time
from dotenv import load_dotenv

from env import ENV
from .emoji_manager import EmojiManager
from .word_manager import WordManager
from .cog_manager import CogManager
from .restrict_help import RestrictedHelpCommand
from database import DatabaseClient

log = logging.getLogger(__name__)
load_dotenv()
os.environ.update(
    {
        'JISHAKU_NO_UNDERSCORE': 'True', # Desativa o prefixo de sublinhado para os comandos do Jishaku
        'JISHAKU_NO_DM_TRACEBACK': 'True', # Desativa o envio de mensagens de erro por DM
        'JISHAKU_HIDE': 'True', # Esconde os comandos do Jishaku na lista de comandos disponíveis
        'JISHAKU_FORCE_PAGINATOR': 'True', # Força o uso do paginador do Jishaku
    }
)

class NayulCore(commands.AutoShardedBot):
    """
    Esta classe é responsável por inicializar o bot, carregar as extensões e gerenciar os eventos.
    """
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True  # Necessário para ler o conteúdo das mensagens
        intents.members = True # Necessário para acessar informações dos membros
        super().__init__(
            command_prefix=commands.when_mentioned_or(ENV.PREFIX),
            intents=intents,
            help_command=RestrictedHelpCommand(),
        )
        #------- atributos do bot -------#
        self.owner_ids = set()
        self.uptime = time()

        #------- classes de configuração do bot -------#
        self.db: DatabaseClient = None
        self.session = aiohttp.ClientSession()
        self.cog_manager = CogManager()
        self.emoji_manager = EmojiManager()
        self.word_manager = WordManager()

        #Adicionando os IDs dos proprietários definidos no .env.
        for owner_id in ENV.OWNER_IDS:
            try:
                self.owner_ids.add(owner_id)
            except ValueError:
                log.warning(f'ID de proprietário inválido: {owner_id}')
                    
    async def setup_hook(self):
            """Método chamado enquanto o bot está inicinado."""
            try:
                self.db = await DatabaseClient.connect()
            except Exception:
                await self.close()

            await self.word_manager.load_words(self)
            await self.emoji_manager.config_emojis(self)
            await self.cog_manager.load_cogs(self)
            await self.load_extension('jishaku')

    async def on_ready(self):
            """Método chamado quando o bot está pronto."""
            log.info(f'Conectado como {self.user} ({self.user.id}).')
            log.info(f'Latência: {round(self.latency * 1000)}ms.')
            log.info(f'discord.py: {discord.__version__}.')
            log.info(f'Python: {os.sys.version.split()[0]}.')
            log.info(f'Servidores: {len(self.guilds)}.')
            log.info("Proprietários: " + ", ".join(f"{u.name} ({u.id})" if u else f"Desconhecido ({oid})" for u, oid in zip(await asyncio.gather(*[self.fetch_user(oid) for oid in self.owner_ids], return_exceptions=True), self.owner_ids)))

    async def start(self, token, *, reconnect = True):
        """Método chamado para iniciar o bot."""
            
        return await super().start(token, reconnect=reconnect)
    
    async def close(self):
        """Método chamado quando o bot é fechado."""
        log.info('Desconectando...')
        await self.session.close()
        await super().close()
        log.info('🔴 Bot desconectado.')