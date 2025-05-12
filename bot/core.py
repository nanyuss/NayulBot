import discord
from discord.ext import commands

import os
import re
import logging
import asyncio
from dotenv import load_dotenv

log = logging.getLogger(__name__)
load_dotenv()
os.environ.update(
    {
        'JISHAKU_NO_UNDERSCORE': 'True', # Desativa o prefixo de sublinhado para os comandos do Jishaku
        'JISHAKU_NO_DM_TRACEBACK': 'True', # Desativa o envio de mensagens de erro por DM
        'JISHAKU_HIDE': 'True', # Esconde os comandos do Jishaku na lista de comandos disponíveis
    }
)

class BotSetup:
    """
    Classe de configuração que contém a lógica para carregar emojis e outras configurações do bot.
    """
    def __init__(self):
        self.db = None

    async def load_cogs(self, bot: commands.AutoShardedBot, path: str):
        """Carrega as extensões (cogs) do bot."""
        for root, _, files in os.walk(path.replace('/', os.path.sep)): 
            for file in files:
                if file.endswith('.py'):
                    try:
                        await bot.load_extension(os.path.join(root, file)[:-3].replace(os.path.sep, '.'))
                        log.debug(f'✅Carregado {file!r} de {root[9:]!r}.')
                    except Exception:
                        log.exception(f"Erro ao carregar a extensão {file}:")
                        continue
    
    async def config_emojis(self, bot: commands.AutoShardedBot, path_emojis: str, emojis_yml: str):
        """Configura os emojis do bot."""
        log.warning('Iniciando configuração dos emojis...')
        existing_emojis = {emoji.name: emoji for emoji in await bot.fetch_application_emojis()}
        formats = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
        emojis_data = {}

        if os.path.exists(path_emojis):
            for image in os.listdir(path_emojis):
                if os.path.isfile(os.path.join(path_emojis, image)) and image.lower().endswith(formats):
                    emoji_name = image.lower().split('.')[0]

                    if emoji_name in existing_emojis:
                        emoji = existing_emojis[emoji_name]
                        emoji_mention = f'<a:{emoji.name}:{emoji.id}>' if emoji.animated else f'<:{emoji.name}:{emoji.id}>'
                        emojis_data[emoji.name] = emoji_mention
                        continue
                    
                    try:
                        with open(os.path.join(path_emojis, image), 'rb') as file:
                            emoji_created = await bot.create_application_emoji(name=emoji_name, image=file.read())
                            emojis_data[emoji_created.name] = f'<a:{emoji_created.name}:{emoji_created.id}>' if emoji_created.animated else f'<:{emoji_created.name}:{emoji_created.id}>'
                            log.info(f'✨ Emoji criado com sucesso: {emoji_created.name}')

                        await asyncio.sleep(3)
                    except Exception:
                        log.error(f'❌ Erro ao criar emoji: {emoji_name}', exc_info=True)
        
        self.generate_emoji_class(emojis_data)
        log.info('😄 Configuração dos emojis concluida.')

    def generate_emoji_class(self, emojis: dict):
        """
        Gera uma classe ou atualiza a classe de emojis automaticamente.
        """
        output_path = os.path.join('bot', 'utils', 'others.py')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        class_lines = [
            '@dataclass',
            'class Emoji:',
            '    """Classe para armazenar os emojis do bot."""',
        ]
        for key, value in emojis.items():
            class_lines.append(f'    {key}: str = "{value!r}"')
        new_class = '\n'.join(class_lines)

        with open(output_path, 'r', encoding='utf-8') as file:
            original_content = file.read()
            
        updated_content = re.sub(
            r'@dataclass\s+class Emoji:.*?(?=^@|\Z)',
            new_class,
            original_content,
            flags=re.DOTALL | re.MULTILINE
        )

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        log.info('📦 Classe de emojis atualizada com sucesso.')

class BotCore(commands.AutoShardedBot, BotSetup):
    """
    Esta classe é responsável por inicializar o bot, carregar as extensões e gerenciar os eventos.
    """
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(os.getenv('PREFIX', '..')),
            intents=discord.Intents.all(),
            help_command=None,
        )

    async def setup_hook(self):
            """Método chamado enquanto o bot está inicinado."""
            await self.load_cogs(self, 'bot/cogs')
            await self.config_emojis(self, 'emojis-files', 'bot/utils/resources/emojis.yml')
            await self.load_extension('jishaku')

    async def on_ready(self):
            """Método chamado quando o bot está pronto."""
            log.info(f'Conectado como {self.user} ({self.user.id}).')
            log.info(f'Latência: {round(self.latency * 1000)}ms.')
            log.info(f'discord.py: {discord.__version__}.')
            log.info(f'Python: {os.sys.version.split()[0]}.')
            log.info(f'Guilds: {len(self.guilds)}.')

    async def start(self, token, *, reconnect = True):
        """Método chamado para iniciar o bot."""
        #self.db = None
        return await super().start(token, reconnect=reconnect)
    
    async def close(self):
        """Método chamado quando o bot é fechado."""
        log.info('Desconectando...')
        await super().close()
        log.info('🔴 Bot desconectado.')