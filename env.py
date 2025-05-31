import os
import sys
from dotenv import load_dotenv
from typing import List
from dataclasses import dataclass

load_dotenv()  # Carrega variáveis do .env

def _str_to_list_of_ints(value: str) -> List[int]:
    return [int(v.strip()) for v in value.split(",") if v.strip().isdigit()]


def _validate_required(var_name: str, validator=lambda x: bool(x)) -> str:
    value = os.getenv(var_name)
    if not value or not validator(value):
        print(f"[ENV] Erro: a variável obrigatória '{var_name}' está ausente ou inválida.")
        sys.exit(1)
    return value


@dataclass
class Env:
    """
    Classe para armazenar as variáveis de ambiente do bot.
    """
    # Obrigatórios
    TOKEN: str
    OWNER_IDS: List[int]
    GITHUB_API_URL: str
    GITHUB_RAW_BASE: str

    # Opcionais (com valores padrão)
    PREFIX: str = ",,"
    MONGO: str = 'mongodb://localhost:27017/'

    @classmethod
    def load(cls) -> "Env":
        return cls(
            TOKEN=_validate_required("TOKEN"),
            OWNER_IDS=_str_to_list_of_ints(_validate_required("OWNER_IDS")),
            GITHUB_API_URL=_validate_required("GITHUB_API_URL"),
            GITHUB_RAW_BASE=_validate_required("GITHUB_RAW_BASE"),
            PREFIX=os.getenv("PREFIX", ",,"),
            MONGO=os.getenv("MONGO")
        )

ENV = Env.load()