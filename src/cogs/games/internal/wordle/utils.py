from typing import List

BASE_URL = 'https://api.gamecord.xyz/wordle?word='

def format_wordle_url(word: str, guessed_words: List[str] = []) -> str:
    """Formata a URL da imagem do wordle.

    Args:
        word (`str`): Palavra que o author tem que adivinhar.
        guessed_words (`List[str]`): Lista das tentativas do author.

    Returns:
        `str`: URL da imagem do wordle.
    """
    if guessed_words == []:
        return BASE_URL + word
    return BASE_URL + word + '&text[&guessed=' + ','.join(guessed_words)