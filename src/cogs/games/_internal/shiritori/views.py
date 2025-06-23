import discord
from discord import ui

from typing import TYPE_CHECKING, Dict

from src import NayulCore
from .utils import configure_player_button
from .types import PlayerStats
from src.utils.emojis import Emoji
from src.utils import nayul_decorators

if TYPE_CHECKING:
    from .components import MainView

class ConfirmPlayer(ui.Button):
    """Botão de confirmação do jogador na partida.
    Args:
        view (`MainView`): View principal da partida.
        player_id (`int`): ID do jogador.
    """
    def __init__(self, view: 'MainView', player_id: int):
        super().__init__(style=discord.ButtonStyle.gray, label='Aceitar', custom_id=str(player_id))
        self.view_instance = view
        self.player_id = player_id
    
    @nayul_decorators.check_user_banned()
    async def callback(self, inter: discord.Interaction[NayulCore]):
        # Garante que apenas o jogador correto pode confirmar
        if inter.user.id != self.player_id:
            return await inter.response.send_message(
                f'{Emoji.error} Apenas <@{self.player_id}> pode confirmar esta participação na partida.',
                ephemeral=True
            )
        
        # Marca o botão do jogador como confirmado
        for item in self.view_instance.container.children:
            if isinstance(item, ui.Section) and isinstance(item.accessory, ConfirmPlayer):
                if item.accessory.player_id == inter.user.id:
                    configure_player_button(item.accessory)
                    break
        
        # Adiciona o jogador à lista de confirmados e atualiza a view
        self.view_instance.confirmed_players.add(inter.user)
        await inter.response.send_message('✅ Você confirmou sua participação na partida! Aguarde o início do jogo.', ephemeral=True)
        await inter.message.edit(view=self.view_instance, allowed_mentions=discord.AllowedMentions(
            users=False,
            everyone=False,
            roles=False
        ))

class ConfirmStartGame(ui.Button):
    """Botão para o autor iniciar a partida
    Args:
        view (`MainView`): View principal da partida.
    """
    def __init__(self, view: 'MainView'):
        super().__init__(style=discord.ButtonStyle.blurple, label='Iniciar Partida')
        self.view_instance = view
    
    @nayul_decorators.check_user_banned()
    async def callback(self, inter: discord.Interaction[NayulCore]):
        # Garante que apenas o autor pode iniciar a partida
        if inter.user != self.view_instance.author:
            return await inter.response.send_message(f'{Emoji.error} Apenas {self.view_instance.author.mention} (criador da partida) pode iniciar o jogo.'
, ephemeral=True)
        # Somente pode iniciar se 2 jogadores ou mais estiverem confirmado
        elif len(self.view_instance.confirmed_players) < 2:
            return await inter.response.send_message('⚠️ Você precisa de pelo menos 2 jogadores confirmados para iniciar a partida.', ephemeral=True)
        
        await self.view_instance.disable_all_items()
        self.view_instance.auto_start = False

        await inter.response.edit_message(view=self.view_instance, allowed_mentions=discord.AllowedMentions(
            users=False,
            everyone=False
        ))
        await self.view_instance.start_game(self.view_instance, inter)
        
class SelectPlayers(ui.UserSelect):
    """Menu de seleção de jogadores para o shiritori.
    Args:
        view (`MainView`): View principal da partida.
    """
    def __init__(self, view: 'MainView'):
        super().__init__(placeholder='Selecione ou remova jogadores aqui…', max_values=25)
        self.view_instance = view

    @nayul_decorators.check_user_banned()
    async def callback(self, inter: discord.Interaction[NayulCore]):
        # Garante que apenas o autor pode gerenciar os jogadores
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
        
        # Atualiza o container com a nova lista de jogadores
        from .components import Container # Evitar importação circular

        self.view_instance.container = Container(self.view_instance)

        self.view_instance.clear_items()
        self.view_instance.add_item(self.view_instance.container)
        self.view_instance.add_item(ui.ActionRow(self.view_instance.confirm_button))

        await inter.response.edit_message(view=self.view_instance, allowed_mentions=discord.AllowedMentions(
            users=False,
            everyone=False
        ))

class PlayerStatusSelect(ui.Select):
    """
    Select que mostra os jogadores e, ao selecionar, exibe o status do jogador escolhido.\n
    Ordena do que ficou mais tempo na partida para o menor.
    Recebe diretamente a lista de stats dos jogadores.
    Args:
        players_stats (`Dict[int, PlayerStats]`): Dicionário com as estatísticas dos jogadores.
    """
    def __init__(self, players_stats: Dict[int, PlayerStats]):
        # Ordena os jogadores pelo tempo de permanência (maior para menor)
        emojis = ['🥇', '🥈', '🥉']
        stats = players_stats
        players = [s['player'] for s in stats.values()]
        def get_time(player):
            s = stats.get(player.id)
            if s and s.get('end') and s.get('start'):
                return (s['end'] - s['start']).total_seconds()
            return 0
        players.sort(key=get_time, reverse=True)
        options = [
            discord.SelectOption(
                label=f'#{i+1} - {player.display_name}',
                emoji=emojis[i] if i < 3 else Emoji.icon_user,
                value=str(player.id),
            ) for i, player in enumerate(players)
        ]
        super().__init__(placeholder='Veja a estatística de um jogador...', options=options)
        self.players_stats = players_stats

    @nayul_decorators.check_user_banned()
    async def callback(self, inter: discord.Interaction[NayulCore]):
        player_id = int(self.values[0])
        s = self.players_stats.get(player_id)
        if not s:
            return await inter.response.send_message(f'{Emoji.error} Nenhum dado encontrado para este jogador.', ephemeral=True)
        words = s.get('words_list', [])
        long = max(words, key=len) if words else '-'
        short = min(words, key=len) if words else '-'
        time = '-'
        if s.get('end') and s.get('start'):
            time = str(s['end'] - s['start']).split('.')[0]
        embed = discord.Embed(
            title=f'{Emoji.icon_user} Estatísticas de {s['player'].display_name}',
            color=discord.Color.blurple()
        ).set_thumbnail(url=s['player'].display_avatar.url)
        embed.add_field(name='📝 Palavras válidas', value=f'```{len(words)}```', inline=False)
        embed.add_field(name='🪶Menor palavra', value=f'```{short}```', inline=False)
        embed.add_field(name='🏆Maior palavra', value=f'```{long}```', inline=False)
        embed.add_field(name='⏳ Tempo na partida', value=f'```{time}```', inline=False)
        await inter.response.send_message(embed=embed, ephemeral=True)

class PlayerStatusSelectView(ui.View):
    def __init__(self, players_stats: Dict[int, PlayerStats]):
        super().__init__(timeout=300)
        self.add_item(PlayerStatusSelect(players_stats))