import logging
from typing import TYPE_CHECKING, Set

if TYPE_CHECKING:
    from nayul import NayulCore

from env import ENV

log = logging.getLogger(__name__)

class WordManager:
    """Classe responsável por gerenciar as palavras do jogo Shiritori."""

    def __init__(self):
        self.words_list: Set[str] = set()

    async def load_words(self, bot: 'NayulCore'):
        """Carrega as palavras do shiritori do bot."""

        log.warning('Iniciando configuração das palavras...')
        async with bot.session.get(f'{ENV.INTERNAL_API}/words/pt.txt') as response:
            if response.status != 200:
                log.critical(f'Erro ao acessar a URL: {response.status}')
                return
                
            text = await response.text()
            for line in text.splitlines():
                word = line.strip()
                if word:
                    self.words_list.add(word)
        log.info('😄 Lista de palavras carregadas com sucesso.')
