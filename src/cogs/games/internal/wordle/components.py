import discord
from discord import ui
from typing import List, Optional, Literal

from .views import GuessButton
from .utils import format_wordle_url
from src.utils.emojis import Emoji

class MainView(ui.LayoutView):
    def __init__(self, author: discord.User, word: str, guessed_words: List[Optional[str]] = [], **kwargs):
        """View principal do jogo Wordle."""
        super().__init__(timeout=300)
        self.kwargs = kwargs # Armazena os argumentos adicionais
        self.author = author # Usuário que usou o comando
        self.word = word # Palavra que o usuário tem que adivinhar
        self.guessed_words = guessed_words # Lista das tentativas do usuário.
        self.container = Container(self, word, guessed_words) 
        self.add_item(self.container) # Adicionando o container ao layout

    async def disable_all_items(self, edit_type: Literal['winner', 'loser', 'timeout']):
        """Desativa todos os botões da view.

        Args:
            edit_type (`Literal['winner', 'loser', 'timeout']`): Tipo de edição que será feita.
        """

        #Desativa todos os botões no container e edita caso o usuário tenha ganhado, perdido ou o tempo tenha expirado.
        for item in self.container.children:
            if isinstance(item, ui.ActionRow):
                for subitem in item.children:
                    if isinstance(subitem, GuessButton):
                        match edit_type:
                            case 'winner':
                                subitem.style = discord.ButtonStyle.green
                                subitem.disabled = True
                                subitem.emoji = Emoji.check
                                subitem.label = 'Você venceu!'
                            case 'loser':
                                subitem.style = discord.ButtonStyle.red
                                subitem.disabled = True
                                subitem.emoji = Emoji.error
                                subitem.label = f'Você perdeu! (palavra: {self.word})'
                            case 'timeout':
                                subitem.disabled = True
                                subitem.label = 'Tempo esgotado! (palavra: {self.word})'

    async def update_container(self):
        """Atualiza o container da view."""
        self.clear_items()
        self.container = Container(self, self.word, self.guessed_words)
        self.add_item(self.container)

    async def on_timeout(self):
        """Método chamado quando o tempo da view expira."""
        await self.disable_all_items('timeout')
        inter: discord.Interaction = self.kwargs.get('inter')
        await inter.edit_original_response(view=self)

class Container(ui.Container):
    def __init__(self, view: 'MainView', word: str, guessed_words: List[Optional[str]] = []):
        super().__init__()
        # Imagem do wordle
        self.add_item(
            ui.MediaGallery(
                discord.components.MediaGalleryItem(
                    media=format_wordle_url(word, guessed_words),
                ),
                row=0
            )
        )
        # Botão para adivinhar a palavra
        self.add_item(ui.ActionRow(GuessButton(view)))