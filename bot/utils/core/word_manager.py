import logging

from discord.ext import commands

from bot.utils.env import ENV

log = logging.getLogger(__name__)

class WordManager:
    """Classe responsável por gerenciar as palavras do jogo Shiritori."""

    def __init__(self):
        self.shiritori_words = set()

    async def load_words(self, bot: commands.AutoShardedBot, path: str = 'archives/shiritori/pt.txt'):
        """Carrega as palavras do shiritori do bot."""

        print(ENV.GITHUB_RAW_BASE + path)
        log.warning('Iniciando configuração das palavras do shiritori...')
        async with bot.session.get(f'{ENV.GITHUB_RAW_BASE}/{path}') as response:
            if response.status != 200:
                log.critical(f'Erro ao acessar a URL: {response.status}')
                return
                
            text = await response.text()
            for line in text.splitlines():
                word = line.strip()
                if word:
                    self.shiritori_words.add(word)
        log.info('😄 Palavras do shiritori configuradas com sucesso.')