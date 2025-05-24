import discord
from discord.ext import commands

import os
import re
import logging
import asyncio
import aiohttp
from time import time
from dotenv import load_dotenv

from bot.utils.others import reload_emojis

__version__ = '0.2.0-alpha'
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

class BotSetup:
    """
    Classe de configuração que contém a lógica para carregar emojis e outras configurações do bot.
    """
    def __init__(self):
        self.db = None
        self.session = aiohttp.ClientSession()
        self._github_api_url = os.getenv('GITHUB_API_URL')
        self._github_raw_base = os.getenv('GITHUB_RAW_BASE')

        # Shiritori
        self.valid_words = set()
        self.invalid_words = set()

    async def load_cogs(self, bot: commands.AutoShardedBot, path: str):
        """Carrega as extensões (cogs) do bot."""
        for root, _, files in os.walk(path.replace('/', os.path.sep)):  # Caminho para as extensões
            for file in files: # Percorre os arquivos no diretório
                if file.endswith('.py'): # Verifica se o arquivo é um arquivo Python
                    try:
                        await bot.load_extension(os.path.join(root, file)[:-3].replace(os.path.sep, '.')) # Carrega a extensão
                        log.debug(f'✅Carregado {file!r} de {root[9:]!r}.')
                    except Exception:
                        log.exception(f"Erro ao carregar a extensão {file}:")
                        continue
    
    async def config_emojis(self, bot: commands.AutoShardedBot, path_emojis: str):
        """Configura os emojis do bot."""
        log.warning('Iniciando configuração dos emojis...')
        existing_emojis = {
            emoji.name: emoji
            for emoji in await bot.fetch_application_emojis()
        } # Obtém os emojis existentes na aplicação
        formats = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
        emojis_data = {}

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self._github_api_url}/{path_emojis}') as response:
                if response.status != 200:
                    log.error(f'Erro ao acessar a URL: {response.status}')
                    return
                
                files = await response.json()
                for file in files:
                    name, ext = os.path.splitext(file['name']) # Separa o nome do arquivo e a extensão
                    if ext.lower() not in formats: # Verifica se o arquivo é uma imagem
                        log.warning(f'Formato inválido: {file["name"]}')
                        continue

                    emoji_name = name.lower()
                    if emoji_name in existing_emojis: # Verifica se o emoji já existe se o emoji já existe, não precisa baixar novamente e é adicionado à lista
                        emoji = existing_emojis[emoji_name]
                        emoji_mention = f'<a:{emoji.name}:{emoji.id}>' if emoji.animated else f'<:{emoji.name}:{emoji.id}>'
                        emojis_data[emoji_name] = emoji_mention
                        continue

                    emoji_url = f'{self._github_raw_base}/{path_emojis}/{file["name"]}'
                    async with session.get(emoji_url) as img_response:
                        if img_response.status != 200: # Verifica se a URL do emoji está acessível
                            log.error(f'Erro ao baixar o emoji: {img_response.status}')
                            continue

                        image_bytes = await img_response.read()
                        try:
                            emoji_created = await bot.create_application_emoji(
                                name=emoji_name,
                                image=image_bytes
                            ) # Cria o emoji
                            emojis_data[emoji_name] = f'<a:{emoji_created.name}:{emoji_created.id}>' if emoji_created.animated else f'<:{emoji_created.name}:{emoji_created.id}>' # Verifica se o emoji é animado ou não e adiciona o emoji à lista
                            log.info(f'✨ Emoji criado: {emoji_created.name}')
                            await asyncio.sleep(3)
                        except Exception:
                            log.error(f'Erro ao criar o emoji: {emoji_name}', exc_info=True)

        self.generate_emoji_class(emojis_data)
        log.info('😄 Emojis configurados com sucesso.')

    def generate_emoji_class(self, emojis: dict):
        """
        Gera uma classe ou atualiza a classe de emojis automaticamente.
        """

        output_path = os.path.join('bot', 'utils', 'others.py')
        os.makedirs(os.path.dirname(output_path), exist_ok=True) # Cria o diretório se não existir

        class_lines = [
            '@dataclass',
            'class Emoji:',
            '    """Classe para armazenar os emojis do bot."""',
        ]
        for key, value in emojis.items(): # Adiciona os emojis à classe
            class_lines.append(f'    {key} = {value!r}')

        class_lines += [
            '',
            '    @classmethod',
            '    def as_dict(cls) -> dict:',
            '        """Retorna os emojis como um dicionário."""',
            '        return {k: v for k, v in cls.__dict__.items() if not k.startswith("__") and not callable(v) and not k == "as_dict"}',
        ]
        new_class = '\n'.join(class_lines)

        with open(output_path, 'r', encoding='utf-8') as file:
            original_content = file.read()
            
        updated_content = re.sub(
            r'@dataclass\s+class Emoji:.*?(?=^@|\Z)',
            new_class,
            original_content,
            flags=re.DOTALL | re.MULTILINE
        ) # Substitui a classe existente ou adiciona a nova

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        log.info('📦 Classe de emojis atualizada com sucesso.')
        reload_emojis()

class BotCore(commands.AutoShardedBot, BotSetup):
    """
    Esta classe é responsável por inicializar o bot, carregar as extensões e gerenciar os eventos.
    """
    def __init__(self):
        BotSetup.__init__(self)
        super().__init__(
            command_prefix=commands.when_mentioned_or(os.getenv('PREFIX', '..')),
            intents=discord.Intents.all(),
            help_command=None,
        )
        self.owner_ids = set()
        self.uptime = time()
        self.__version__ = __version__

        #Adicionando os IDs dos proprietários definidos no .env.
        for owner_id in os.getenv('OWNER_IDS', '').split(','):
            try:
                self.owner_ids.add(int(owner_id.strip()))
            except ValueError:
                log.warning(f'ID de proprietário inválido: {owner_id.strip()}')
                    
    async def setup_hook(self):
            """Método chamado enquanto o bot está inicinado."""
            await self.load_cogs(self, 'bot/cogs')
            await self.config_emojis(self, 'media/emojis')
            await self.load_extension('jishaku')

    async def on_ready(self):
            """Método chamado quando o bot está pronto."""
            log.info(f'Conectado como {self.user} ({self.user.id}).')
            log.info(f'Latência: {round(self.latency * 1000)}ms.')
            log.info(f'Versão: {__version__}.')
            log.info(f'discord.py: {discord.__version__}.')
            log.info(f'Python: {os.sys.version.split()[0]}.')
            log.info(f'Servidores: {len(self.guilds)}.')

    async def start(self, token, *, reconnect = True):
        """Método chamado para iniciar o bot."""
        #self.db = None
        return await super().start(token, reconnect=reconnect)
    
    async def close(self):
        """Método chamado quando o bot é fechado."""
        log.info('Desconectando...')
        await self.session.close()
        await super().close()
        log.info('🔴 Bot desconectado.')