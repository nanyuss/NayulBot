import discord
from typing import TYPE_CHECKING, List, Dict, Literal, Any
from datetime import datetime

import re
from nayul.utils.others import Emoji
from .types import PlayerStats
from nayul import NayulCore

if TYPE_CHECKING:
    from .views import ConfirmPlayer


def configure_player_button(button: 'ConfirmPlayer'):
    """Desa
    """
    button.disabled = True
    button.style = discord.ButtonStyle.green
    button.label = None
    button.emoji = Emoji.check

def validate_word_shiritori(word: str, inter: discord.Interaction[NayulCore]) -> bool:
    if len(word) < 3 or not re.search(r'[aeiou].$|.[aeiou]$', word):
        return False
    
    return word in inter.client.word_manager.shiritori_words

def get_time_limit(used_words_count: int) -> int:
    if used_words_count <= 50:
        return 60
    elif used_words_count <= 100:
        return 30
    else:
        return 15

def get_phase_message(time_limit: int, ends_at: int) -> str:
    if time_limit == 60:
        return f'⏱ Tempo para responder: **60 segundos** (<t:{ends_at}:R>)'
    elif time_limit == 30:
        return f'⚠️ Atenção! Tempo reduzido para **30 segundos** (<t:{ends_at}:R>)'
    else:
        return f'🔥 Morte Súbita! Tempo crítico: **15 segundos** (<t:{ends_at}:R>)'
    
def create_stats_dict(players: List[discord.Member]) -> Dict[int, PlayerStats]:
    """
    Cria e retorna um dicionário de estatísticas para cada jogador do Shiritori.
    O dicionário tem a seguinte estrutura:
    ```
    {
        player_id: {
            'player': discord.Member,
            'words': int,
            'start': datetime,
            'end': datetime,
            'words_list': List[str]
        }
    }
    ```
    Args:
        players (List[discord.Member]): Lista de jogadores do Shiritori.
    """
    stats: Dict[int, PlayerStats] = {}
    for player in players:
        stats[player.id] = {
            'player': player,
            'start': datetime.now(),
            'end': None,
            'words_list': []
        }
    return stats

def update_player_stats(
    stats: Dict[int, PlayerStats],
    player_id: int,
    action: Literal['end', 'words_list'],
    value: Any = None
) -> None:
    """
    Atualiza um campo específico das estatísticas de um jogador.

    Args:
        stats: Dicionário de estatísticas dos jogadores.
        player_id: ID do jogador a ser atualizado.
        action: Campo a ser atualizado ('end', 'words_list').
        value: Valor a ser usado na atualização.
            - 'end': define o campo 'end' (value deve ser datetime ou None)
            - 'words_list': adiciona uma palavra (value deve ser str)
    """
    player_stats = stats.get(player_id)
    if not player_stats:
        return

    if action == 'end':
        player_stats['end'] = value if value is not None else datetime.now()
    elif action == 'words_list' and isinstance(value, str):
        player_stats['words_list'].append(value)