import discord
from discord import ui
from discord.ext import commands
from discord import app_commands

import re
import asyncio
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime
from unidecode import unidecode

from bot import BotCore
from bot.utils.others import Emoji

class ShiritoriGame(commands.Cog):
    '''Classe que contém o comando do jogo Shiritori.'''

    def __init__(self, bot: BotCore):
        self.bot = bot
    
    @app_commands.guild_only()
    @app_commands.command(name='shiritori', description='Inicia uma partida de Shiritori.')
    @app_commands.checks.bot_has_permissions(
        embed_links=True,
        send_messages=True,
        read_messages=True,
        add_reactions=True
    )
    async def shiritori(self, inter: discord.Interaction[BotCore]):
        players = [inter.user]
        
        view = LayoutView(inter.user, players)
        await inter.response.send_message(view=view, allowed_mentions=discord.AllowedMentions(
            users=False,
            everyone=False
        ))
        await view.start_time(inter)

async def setup(bot: BotCore):
    await bot.add_cog(ShiritoriGame(bot))

class SelectPlayers(ui.UserSelect):
    def __init__(self, view: 'LayoutView'):
        super().__init__(placeholder='Selecione ou remova jogadores aqui…', max_values=25)
        self.view_instance = view

    async def callback(self, inter: discord.Interaction[BotCore]):
        if self.view_instance.author != inter.user:
            return await inter.response.send_message(
                f'⚠️ Apenas {self.view_instance.author.mention} (criador da partida) pode gerenciar os jogadores.',
                ephemeral=True, delete_after=10)
        
        for player in self.values:
            if player.bot or player == self.view_instance.author:
                continue
            if player not in self.view_instance.players:
                if len(self.view_instance.players) < 25:
                    self.view_instance.players.append(player)
            elif player in self.view_instance.players:
                self.view_instance.players.remove(player)

            if player in self.view_instance.confirmed_players and player not in self.view_instance.players:
                self.view_instance.confirmed_players.remove(player)

        self.view_instance.container = Container(self.view_instance)

        self.view_instance.clear_items()
        self.view_instance.add_item(self.view_instance.container)
        self.view_instance.add_item(ui.ActionRow(self.view_instance.confirm_button))

        await inter.response.edit_message(view=self.view_instance, allowed_mentions=discord.AllowedMentions(
            users=False,
            everyone=False
        ))

class ConfirmPlayer(ui.Button):
    def __init__(self, view: 'LayoutView', player_id: int):
        super().__init__(style=discord.ButtonStyle.gray, label='Aceitar', custom_id=str(player_id))
        self.view_instance = view
        self.player_id = player_id

    async def callback(self, inter: discord.Interaction[BotCore]):
        if inter.user.id != self.player_id:
            return await inter.response.send_message(
                f'❌ Apenas <@{self.player_id}> pode confirmar esta participação na partida.',
                ephemeral=True
            )

        for item in self.view_instance.container.children:
            if isinstance(item, ui.Section) and isinstance(item.accessory, ConfirmPlayer):
                if item.accessory.player_id == inter.user.id:
                    item.accessory.disabled = True
                    item.accessory.style = discord.ButtonStyle.green
                    item.accessory.label = None
                    item.accessory.emoji = Emoji.check
                    break

        self.view_instance.confirmed_players.add(inter.user)
        await inter.response.send_message('✅ Você confirmou sua participação na partida! Aguarde o início do jogo.', ephemeral=True)
        await inter.message.edit(view=self.view_instance, allowed_mentions=discord.AllowedMentions(
            users=False,
            everyone=False
        ))

class ConfirmStart(ui.Button):
    def __init__(self, view: 'LayoutView'):
        super().__init__(style=discord.ButtonStyle.blurple, label='Iniciar Partida')
        self.view_instance = view

    async def callback(self, inter: discord.Interaction[BotCore]):
        if inter.user != self.view_instance.author:
            return await inter.response.send_message(f'❌ Apenas {self.view_instance.author.mention} (criador da partida) pode iniciar o jogo.'
, ephemeral=True)
        elif len(self.view_instance.confirmed_players) < 2:
            return await inter.response.send_message('⚠️ Você precisa de pelo menos 2 jogadores confirmados para iniciar a partida.', ephemeral=True)
        
        await self.view_instance.disable_all()
        self.view_instance.auto_start = False

        await inter.response.edit_message(view=self.view_instance, allowed_mentions=discord.AllowedMentions(
            users=False,
            everyone=False
        ))
        await self.view_instance.start_game(inter)

class Container(ui.Container):
    def __init__(self, view: 'LayoutView'):
        super().__init__(accent_colour=16775930)

        self.add_item(ui.TextDisplay(
            ''.join(
                [
                    '### Shiritori╺╸Jogo de Palavras\n\n',
                    'Os jogadores devem digitar uma palavra que comece com as duas últimas letras da palavra dita pelo jogador anterior. Irei verifica se a palavra é válida e continua o jogo. Aqui está um exemplo:\n',
                    '> Abel**ha** -> **Ha**mister\n\n'
                ]
            )))
        
        self.add_item(ui.Separator())

        self.add_item(ui.TextDisplay(
            ''.join(
                [
                    '### Instruções do Jogo:\n',
                    '`1.` O primeiro jogador irá começar dizendo uma palavra qualquer.\n',
                    '`2.` A próxima palavra deve começar com as duas últimas letras da palavra anterior.\n',
                    '`3.` Não repita palavras já ditas ou perderá a partida.\n',
                    '`4.` O tempo para responder será de **60 segundos** até 70 palavras válidas usadas, **30 segundos** da palavra válida 71 até a 120, e **15 segundos** a partir da palavra válida 121.\n'
                    '`5.` O jogador que não conseguir pensar em uma palavra dentro do tempo perde a partida.\n'
                ]
            )))
        
        self.add_item(ui.Separator())

        self.add_item(ui.TextDisplay(f'### Jogadores ({len(view.players)}/25)\n-# **{view.author.display_name}** convidou você para uma partida de Shiritori.\n-# Clique em **Aceitar** para confirmar sua participação!'))
        
        for player in view.players:
            display_name = f'{Emoji.crown} {player.mention}' if player == view.author else f'{Emoji.icon_user} {player.mention}'
            confirmed = player in view.confirmed_players

            button = ConfirmPlayer(view, player.id)
            if confirmed:
                button.disabled = True
                button.style = discord.ButtonStyle.green
                button.label = None
                button.emoji = Emoji.check

            self.add_item(
                ui.Section(
                    f'{display_name} - `{player.id}`',
                    accessory=button
                ))
            
        self.add_item(ui.Separator())
            
        self.add_item(ui.ActionRow(SelectPlayers(view)))

        self.add_item(ui.TextDisplay(
            f'-# ⏳ Os jogadores têm até <t:{view.time_start}:T> (<t:{view.time_start}:R>) para confirmar sua participação.'
        ))


class LayoutView(ui.LayoutView):
    def __init__(self, author: discord.Member, players: list[discord.Member]):
        super().__init__(timeout=300)
        self.time_start = int(time.time()) + 120
        self.auto_start = True
        self.author = author
        self.players = players
        self.confirmed_players: set[discord.Member] = set()
        self.container = Container(self)
        self.add_item(self.container)

        self.confirm_button = ConfirmStart(self)
        self.add_item(ui.ActionRow(self.confirm_button))

    async def disable_all(self):
        # Desativar todos os botões na container
        for item in self.container.children:
            if isinstance(item, ui.Section) and isinstance(item.accessory, ConfirmPlayer):
                item.accessory.disabled = True
            elif isinstance(item, ui.ActionRow):
                for subitem in item.children:
                    if isinstance(subitem, SelectPlayers):
                        subitem.disabled = True

        # Desativar botão iniciar
        for child in self.children:
            if isinstance(child, ui.ActionRow):
                for subchild in child.children:
                    if isinstance(subchild, ConfirmStart):
                        subchild.disabled = True
            elif isinstance(child, ConfirmStart):
                child.disabled = True

    async def start_time(self, inter: discord.Interaction[BotCore]):
        self.bot_loop = inter.client.loop

        await asyncio.sleep(120)

        if not self.auto_start:
            return
        
        await self.disable_all()
        await inter.edit_original_response(view=self, allowed_mentions=discord.AllowedMentions(
            users=False,
            everyone=False
        ))

        if len(self.confirmed_players) < 2:
            await inter.followup.send('⏰ Tempo de espera esgotado! Não é possível iniciar a partida com menos de 2 jogadores.')
            return
        
        await self.start_game(inter)

    async def validate_word(self, word: str, inter: discord.Interaction[BotCore]) -> bool:
        if len(word) < 3 or not re.search(r'[aeiou].$|.[aeiou]$', word):
            inter.client.invalid_words.add(word)
            return False

        if word in inter.client.valid_words:
            return True
        if word in inter.client.invalid_words:
            return False

        url = f'https://www.dicio.com.br/{word}/'
        try:
            async with inter.client.session.get(url) as response:
                if response.status != 200:
                    inter.client.invalid_words.add(word)
                    return False

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                definition = soup.find('p', class_='significado')
                if not definition or len(definition.text.strip()) < 10:
                    inter.client.invalid_words.add(word)
                    return False

                word_class = soup.find('span', class_='cl')
                if word_class:
                    blocklist = {
                        'símbolo', 'abreviação', 'letra', 'sigla',
                        'sufixo', 'prefixo', 'onomatopeia',
                        'abreviado', 'interjeição'
                    }
                    if any(term in word_class.text.lower() for term in blocklist):
                        inter.client.invalid_words.add(word)
                        return False

        except Exception:
            return False

        inter.client.valid_words.add(word)
        return True

    async def start_game(self, inter: discord.Interaction):
        players = list(self.players)
        used_words = set()
        previous_word = None
        word_count = 0
        start_time = datetime.now()
        channel = inter.channel

        random.shuffle(players)

        players_str = ', '.join(p.mention for p in players)
        await channel.send(
            content=f'⚠️ A partida irá começar <t:{int(time.time()) + 10}:R>!\n🎮 Jogadores: {players_str}',
            delete_after=10
        )
        await asyncio.sleep(10)

        while len(players) > 1:
            for player in players.copy():
                if len(players) == 1:
                    break

                time_limit = 60 if len(used_words) < 70 else 30 if len(used_words) < 120 else 15
                start_turn = datetime.now()

                if previous_word:
                    phase_msg = (
                        '⏱ Tempo para responder: **60 segundos**' if word_count <= 50 else
                        '⚠️ Atenção! Tempo reduzido para **30 segundos**' if word_count <= 100 else
                        '🔥 Morte Súbita! Tempo crítico: **15 segundos**'
                        )
                    embed_waiting = discord.Embed(
                        description=(
                            f'Digite uma palavra que comece com as duas últimas letras de:\n'
                            f'### **{previous_word[:-2]}**__**{previous_word[-2:]}**__\n\n'
                            f'{phase_msg}'
                        ),
                        color=discord.Color.blurple()
                    )
                else:
                    embed_waiting = discord.Embed(
                        title='Início do Jogo',
                        description='Digite a primeira palavra para começar!',
                        color=discord.Color.blurple()
                    )
                
                message_player = await channel.send(content=player.mention, embed=embed_waiting)
                    
                while True:

                    def check(m):
                        return m.author == player and m.channel == channel

                    try:
                        remaining_time = time_limit - (datetime.now() - start_turn).total_seconds()
                        if remaining_time <= 0:
                            raise asyncio.TimeoutError()

                        message = await inter.client.wait_for('message', timeout=remaining_time, check=check)
                        word = unidecode(message.content.lower().strip())

                        if word in used_words:
                            embed = discord.Embed(
                                        title='Palavra Repetida!',
                                        description=f'❌ {player.mention}, a palavra **{word}** já foi usada. Você foi eliminado.',
                                        color=discord.Color.red()
                                        )
                            
                            await message_player.delete()
                            await channel.send(embed=embed)
                            players.remove(player)
                            break

                        if previous_word and not word.startswith(previous_word[-2:]):
                            continue

                        valid = await self.validate_word(word, inter)
                        if not valid:
                            continue

                        # Palavra válida!
                        used_words.add(word)
                        word_count += 1
                        previous_word = word
                        await message.add_reaction(Emoji.check)
                        await message_player.delete()
                        break  # Avança para o próximo jogador

                    except asyncio.TimeoutError:
                        embed_timeout = discord.Embed(
                            title='Tempo Esgotado!',
                            description=(
                                f'⏰ {player.mention} não respondeu a tempo (**{time_limit}s**).\n'
                                'Você foi eliminado.'
                            ),
                            color=discord.Color.red()
                        )
                        await message_player.delete()
                        await channel.send(embed=embed_timeout)
                        players.remove(player)
                        break

        # Final da partida
        winner = players[0]
        end_time = datetime.now()

        embed = discord.Embed(
            title='🏁 Resultado da Partida de Shiritori',
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=winner.display_avatar.url)
        embed.add_field(name='🏆 Vencedor:', value=winner.mention, inline=False)
        embed.add_field(name='📊 Palavras usadas:', value=f'```{word_count}```', inline=False)
        embed.add_field(name='⏱️ Duração da Partida:', value=f'```{str(end_time - start_time).split('.')[0]}```', inline=False)

        await inter.followup.send(embed=embed)