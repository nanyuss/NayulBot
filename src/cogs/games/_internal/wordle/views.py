import discord
from discord import ui
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .components import MainView

from src import NayulCore
from src.utils.emojis import Emoji
from src.utils import nayul_decorators

class ResponseModal(ui.Modal):
    def __init__(self, view: 'MainView'):
        super().__init__(title='Termo')
        self.view_instance = view
        self.guess = ui.TextInput(
            label='Qual a palavra?',
            style=discord.TextStyle.short,
            placeholder='Digite uma palavra...',
            min_length=5,
            max_length=5,
            required=True
        )
        self.add_item(self.guess)
    
    async def on_submit(self, inter: discord.Interaction[NayulCore]):
        word = self.guess.value.lower() # Pega a resposta do modal e deixa em minúscula

        # Verifica se a resposta não é somente palavras ou se a palavra está na lista
        if (not word.isalpha()) or (word not in inter.client.word_manager.five_letter_words) or (word not in inter.client.word_manager.words_list):
            await inter.response.send_message(f'{Emoji.error} A palavra fornecida não é válida ou não está na lista de palavras permitidas.', ephemeral=True)
            return
        
        # Verifica se a palavra já foi utilizada
        if word in self.view_instance.guessed_words:
            await inter.response.send_message(f'{Emoji.error} Você já utilizou essa palavra.', ephemeral=True)
            return
        
        self.view_instance.guessed_words.append(word) # Adiciona a palavra na lista de tentativas
        await self.view_instance.update_container() # Atualiza o container da view
        
        if word == self.view_instance.word: # Verifica se a palavra é a mesma que era para adivinhar
            await self.view_instance.disable_all_items('winner')
        elif len(self.view_instance.guessed_words) == 6: # Verifica se o usuário já gastou as 6 tentativas
            await self.view_instance.disable_all_items('loser')

        await inter.response.edit_message(
            view=self.view_instance,
        )

class GuessButton(ui.Button):
    def __init__(self, view: 'MainView'):
        super().__init__(label='Adivinhar', emoji=Emoji.icon_edit, style=discord.ButtonStyle.secondary)
        self.view_instance = view
    
    @nayul_decorators.check_user_banned()
    async def callback(self, inter: discord.Interaction[NayulCore]):
        if inter.user != self.view_instance.author: # Verifica se a pessoa que clicou no botão é a mesma que usou o comando
            await inter.response.send_message(f'{Emoji.error} Apenas {self.view_instance.author.mention} pode interagir com este botão.', ephemeral=True)
            return
        
        await inter.response.send_modal(ResponseModal(self.view_instance))