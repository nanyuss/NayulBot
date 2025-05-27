import os
import logging
from discord.ext import commands

log = logging.getLogger(__name__)

class CogManager:
    """ Classe responsável por gerenciar as extensões (cogs) do bot. """
    def __init__(self, path: str = 'bot/cogs'):
        self.path = path

    async def load_cogs(self, bot: commands.AutoShardedBot):
        """ Carrega todas as extensões do bot. """

        for root, _, files in os.walk(self.path.replace('/', '.')): # Caminho para as extensões
            for file in files: # Percorre os arquivos no diretório
                if file.endswith('.py'): # Verifica se o arquivo é um arquivo python
                    try:
                        await bot.load_extension(
                                os.path.join(root, file)[:-3].replace(os.path.sep, '.')
                            ) # Carrega a extensão
                        log.debug(f'✅ Carregado {file!r} de {root[9:]!r}.')
                    except Exception:
                        log.exception(f'Erro ao carregar a extensão {file}:')
                        continue

    async def reload_cogs(self, bot: commands.AutoShardedBot):
        """ Recarrega todas as extensões do bot. """
        for root, _, files in os.walk(self.path.replace('/', '.')):
            for file in files:
                if file.endswith('.py'):
                    try:
                        await bot.reload_extension(
                                os.path.join(root, file)[:-3].replace(os.path.sep, '.')
                            )
                        log.debug(f'🔄 Recarregado {file!r} de {root[9:]!r}.')
                    except Exception:
                        log.exception(f'Erro ao recarregar a extensão {file}:')
                        continue

    async def unload_cogs(self, bot: commands.AutoShardedBot):
        """ Descarrega as extensões do bot. """
        for root, _, files in os.walk(self.path.replace('/', '.')):
            for file in files:
                if file.endswith('.py'):
                    try:
                        await bot.unload_extension(
                                os.path.join(root, file)[:-3].replace(os.path.sep, '.')
                            )
                        log.debug(f'❌Descarregado {file!r} de {root[9:]!r}.')
                    except Exception:
                        log.exception(f'Erro ao descarregar a extensão {file}:')
                        continue
    
    async def reload_cog_one(self, bot: commands.AutoShardedBot, extension: str):
        """ Recarrega uma extensão do bot. """
        try:
            await bot.reload_extension(extension)
            log.debug(f'🔄 Recarregado {extension!r}.')
        except Exception:
            log.exception(f'Erro ao recarregar a extensão {extension}:')

    async def load_cog_one(self, bot: commands.AutoShardedBot, extension: str):
        """ Carrega uma extensão do bot. """
        try:
            await bot.load_extension(extension)
            log.debug(f'✅ Carregado {extension!r}.')
        except Exception:
            log.exception(f'Erro ao carregar a extensão {extension}:')
    
    async def unload_cog_one(self, bot: commands.AutoShardedBot, extension: str):
        """ Descarrega uma extensão do bot. """
        try:
            await bot.unload_extension(extension)
            log.debug(f'❌ Descarregado {extension!r}.')
        except Exception:
            log.exception(f'Erro ao descarregar a extensão {extension}:')

    async def extensions_list(self) -> list[str]:
        """ Lista todas as extensões do bot. """
        extensions = []
        for root, _, files in os.walk(self.path.replace('/', '.')):
            for file in files:
                if file.endswith('.py'):
                    extensions.append(os.path.join(root, file)[:-3].replace(os.path.sep, '.'))
        return extensions