import logging
from typing import TYPE_CHECKING, Set

if TYPE_CHECKING:
    from src import NayulCore

from env import ENV

log = logging.getLogger(__name__)

class WordManager:
    """Classe responsável por gerenciar as palavras do jogo Shiritori."""

    def __init__(self):
        self.words_list: Set[str] = set()
        self.five_letter_words: Set[str] = set()

    async def load_words(self, nayul: 'NayulCore'):
        """Carrega as palavras do shiritori do bot.
        Args:
            nayul (`NayulCore`): Instância do bot.
        """

        log.warning('Iniciando configuração das palavras...')

        wordle_words = await self.fetch_words(nayul, 'words/wordle/pt.txt') or set()
        all_words = await self.fetch_words(nayul, 'words/all/pt.txt') or set()

        # Atribui os resultados às variáveis da instância
        self.words_list = all_words or set()
        self.five_letter_words = wordle_words or set()
        log.info('😄 Lista de palavras carregadas com sucesso.')

    async def fetch_words(self, nayul: 'NayulCore', endpoint: str) -> Set[str]:
        """Busca as palavras do shiritori do bot.
        Args:
            nayul (`NayulCore`): Instância do bot.
            endpoint (str): Endpoint da API para buscar as palavras.
        """
        async with nayul.session.get(f'{ENV.INTERNAL_API}/{endpoint}') as response:
            if response.status != 200:
                log.critical(f'Erro ao acessar a URL: {response.status} {response.url}')
                return
                
            text = await response.text()
            return {line.strip() for line in text.splitlines() if line.strip()}