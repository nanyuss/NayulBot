from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field

from typing import Optional, List

class UserProfile(BaseModel):
    """
    Representa o perfil do usuário.

    Atributos:
        skin_now (`str`): Skin atual do usuário.
        skins (`List[str]`): Lista de skins desbloqueadas.
        experience (`float`): Experiência acumulada.
        reputation (`int`): Pontuação de reputação.
        about_me (`Optional[str]`): Descrição pessoal do usuário.
    """
    skin_now: str = 'default'
    skins: List[str] = ['default']
    experience: float = 0.0
    reputation: int = 0
    about_me: Optional[str] = None

    class Config:
        frozen = True

class UserCooldowns(BaseModel):
    """
    Gerencia os tempos de espera (cooldowns) do usuário.

    Atributos:
        daily (`Optional[datetime]`): Cooldown diário.
        reputation (`Optional[datetime]`): Cooldown de reputação.
        premium_expiration (`Optional[datetime]`): Data de expiração do status premium.
    """
    daily: Optional[datetime] = None
    reputation: Optional[datetime] = None
    premium_expiration: Optional[datetime] = None

    class Config:
        frozen = True

class UserBan(BaseModel):
    """
    Representa o status de banimento do usuário.

    Atributos:
        banned (`bool``): Indica se o usuário está banido.
        banned_at (`Optional[datetime]`): Data do banimento.
        expires_at (`Optional[datetime]`): Data de expiração do banimento.
        reason (`Optional[str]`): Motivo do banimento.
    """
    banned: bool = False
    banned_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    reason: Optional[str] = None

    class Config:
        frozen = True

class UserData(BaseModel):
    """
    Modelo principal de dados do usuário.

    Atributos:
        id (`int`): Identificador único do usuário (mapeado de `_id` no MongoDB).
        shells (`int`): Quantidade de conchas do usuário.
        pearls (`int`): Quantidade de pérolas do usuário.
        cai_uuid (`Optional[str]`): UUID do usuário.
        profile (`UserProfile`): Perfil do usuário.
        cooldowns (`UserCooldowns`): Cooldowns do usuário.
        ban (`UserBan`): Status de banimento do usuário.
    """
    id: int = Field(alias='_id')
    shells: int = 0
    pearls: int = 0
    cai_uuid: Optional[str] = None
    profile: UserProfile = UserProfile()
    cooldowns: UserCooldowns = UserCooldowns()
    ban: UserBan = UserBan()

    class Config:
        validate_by_name = True
        frozen = True