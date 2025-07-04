import os
import logging
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from src import NayulCore

log = logging.getLogger(__name__)

class CogManager:
    """ Classe responsável por gerenciar as extensões (cogs) do bot. """
    def __init__(self, path: str = 'src/cogs'):
        self.path = path
        self.extensions: Dict[str, str] = {} # Armazena as extensões como um dicionário

    async def load_cogs(self, nayul: 'NayulCore'):
        """ Carrega todas as extensões do bot. """
        for root, _, files in os.walk(self.path): # Caminho para as extensões
            # Ignora qualquer diretório que contenha '_internal' no caminho
            if '_internal' in root.split(os.path.sep):
                continue
            for file in files: # Percorre os arquivos no diretório
                if file.endswith('.py'): # Verifica se o arquivo é um arquivo python
                    rel_path = os.path.relpath(os.path.join(root, file), start=os.path.dirname(os.path.dirname(__file__)))
                    # Garante que sempre começa com 'nayul.'
                    if rel_path.startswith('cogs' + os.path.sep):
                        rel_path = 'src' + os.path.sep + rel_path

                    module = rel_path[:-3].replace(os.path.sep, '.')
                    self.extensions[file[:-3]] = module # Adiciona a extensão ao dicionário de extensões
                    try:
                        await nayul.load_extension(module) # Carrega a extensão
                        log.info(f'✅ Carregado {file!r} de {root[9:]!r}.')
                    except Exception:
                        log.exception(f'Erro ao carregar a extensão {file}:')
                        continue

    async def reload_cogs(self, nayul: 'NayulCore'):
        """ Recarrega todas as extensões do bot. """
        for key, module in self.extensions.items():
            try:
                await nayul.reload_extension(module)
                log.debug(f'🔄 Recarregado {key!r}.')
            except Exception:
                log.exception(f'Erro ao recarregar a extensão {key!r}:')
                continue

    async def unload_cogs(self, nayul: 'NayulCore'):
        """ Descarrega as extensões do bot. """
        for key, module in self.extensions.items():
            try:
                await nayul.reload_extension(module)
                log.debug(f'❌ Descarregado Recarregado {key!r}')
            except Exception:
                log.exception(f'Erro ao descarregar a extensão {key!r}:')
                continue
    
    async def reload_cog_one(self, nayul: 'NayulCore', extension: str):
        """ Recarrega uma extensão do bot. """
        try:
            module = self.extensions[extension]
            await nayul.reload_extension(module)
            log.debug(f'🔄 Recarregado {extension!r}.')
        except Exception:
            log.exception(f'Erro ao recarregar a extensão {extension!r}:')

    async def load_cog_one(self, nayul: 'NayulCore', extension: str):
        """ Carrega uma extensão do bot. """
        try:
            module = self.extensions[extension]
            await nayul.reload_extension(module)
            log.debug(f'✅ Carregado {extension!r}.')
        except Exception:
            log.exception(f'Erro ao carregar a extensão {extension!r}:')
    
    async def unload_cog_one(self, nayul: 'NayulCore', extension: str):
        """ Descarrega uma extensão do bot. """
        try:
            module = self.extensions[extension]
            await nayul.reload_extension(module)
            log.debug(f'❌ Descarregado {extension!r}.')
        except Exception:
            log.exception(f'Erro ao descarregar a extensão {extension}:')