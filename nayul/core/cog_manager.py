import os
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nayul import NayulCore

log = logging.getLogger(__name__)

class CogManager:
    """ Classe responsável por gerenciar as extensões (cogs) do bot. """
    def __init__(self, path: str = 'nayul/cogs'):
        self.path = path

    async def load_cogs(self, nayul: 'NayulCore'):
        """ Carrega todas as extensões do bot. """
        for root, _, files in os.walk(self.path): # Caminho para as extensões
            # Ignora qualquer diretório que contenha 'internal' no caminho
            if 'internal' in root.split(os.path.sep):
                continue
            for file in files: # Percorre os arquivos no diretório
                if file.endswith('.py'): # Verifica se o arquivo é um arquivo python
                    rel_path = os.path.relpath(os.path.join(root, file), start=os.path.dirname(os.path.dirname(__file__)))
                    # Garante que sempre começa com 'nayul.'
                    if rel_path.startswith('cogs' + os.path.sep):
                        rel_path = 'nayul' + os.path.sep + rel_path

                    module = rel_path[:-3].replace(os.path.sep, '.')
                    try:
                        await nayul.load_extension(module) # Carrega a extensão
                        log.info(f'✅ Carregado {file!r} de {root[11:]!r}.')
                    except Exception:
                        log.exception(f'Erro ao carregar a extensão {file}:')
                        continue

    async def reload_cogs(self, nayul: 'NayulCore'):
        """ Recarrega todas as extensões do bot. """
        for root, _, files in os.walk(self.path):
            if 'internal' in root.split(os.path.sep):
                continue
            for file in files:
                if file.endswith('.py'):
                    rel_path = os.path.relpath(os.path.join(root, file), start=os.path.dirname(os.path.dirname(__file__)))
                    if rel_path.startswith('cogs' + os.path.sep):
                        rel_path = 'nayul' + os.path.sep + rel_path

                    module = rel_path[:-3].replace(os.path.sep, '.')
                    try:
                        await nayul.reload_extension(module)
                        log.debug(f'🔄 Recarregado {file!r} de {root[11:]!r}.')
                    except Exception:
                        log.exception(f'Erro ao recarregar a extensão {file}:')
                        continue

    async def unload_cogs(self, nayul: 'NayulCore'):
        """ Descarrega as extensões do bot. """
        for root, _, files in os.walk(self.path):
            if 'internal' in root.split(os.path.sep):
                continue
            for file in files:
                if file.endswith('.py'):
                    rel_path = os.path.relpath(os.path.join(root, file), start=os.path.dirname(os.path.dirname(__file__)))
                    if rel_path.startswith('cogs' + os.path.sep):
                        rel_path = 'nayul' + os.path.sep + rel_path

                    module = rel_path[:-3].replace(os.path.sep, '.')
                    try:
                        await nayul.reload_extension(module)
                        log.debug(f'❌ Descarregado Recarregado {file!r} de {root[11:]!r}.')
                    except Exception:
                        log.exception(f'Erro ao descarregar a extensão {file}:')
                        continue
    
    async def reload_cog_one(self, nayul: 'NayulCore', extension: str):
        """ Recarrega uma extensão do bot. """
        try:
            await nayul.reload_extension(extension)
            log.debug(f'🔄 Recarregado {extension!r}.')
        except Exception:
            log.exception(f'Erro ao recarregar a extensão {extension}:')

    async def load_cog_one(self, nayul: 'NayulCore', extension: str):
        """ Carrega uma extensão do bot. """
        try:
            await nayul.load_extension(extension)
            log.debug(f'✅ Carregado {extension!r}.')
        except Exception:
            log.exception(f'Erro ao carregar a extensão {extension}:')
    
    async def unload_cog_one(self, nayul: 'NayulCore', extension: str):
        """ Descarrega uma extensão do bot. """
        try:
            await nayul.unload_extension(extension)
            log.debug(f'❌ Descarregado {extension!r}.')
        except Exception:
            log.exception(f'Erro ao descarregar a extensão {extension}:')

    async def extensions_list(self) -> list[str]:
        """ Lista todas as extensões do bot. """
        extensions = []
        for root, _, files in os.walk(self.path):
            if 'internal' in root.split(os.path.sep):
                continue
            for file in files:
                if file.endswith('.py'):
                    rel_path = os.path.relpath(os.path.join(root, file), start=os.path.dirname(os.path.dirname(__file__)))
                    if rel_path.startswith('cogs' + os.path.sep):
                        rel_path = 'nayul' + os.path.sep + rel_path

                    extensions.append(rel_path[:-3].replace(os.path.sep, '.'))
        return extensions