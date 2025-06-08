from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field

from typing import Optional, List

class UserProfile(BaseModel):
    """
    Representa o perfil do usuário.

    Attributes:
        skin_now (`str`): Skin atual do usuário.
        skins (`List[str]`): Lista de skins desbloqueadas.
        about_me (`Optional[str]`): Descrição pessoal do usuário.
    """
    skin_now: str = Field(alias='skinNow', default='default')
    skins: List[str] = ['default']
    about_me: Optional[str] = Field(alias='aboutMe', default=None)

    class Config:
        frozen = True
        validate_by_name = True

class UserCooldowns(BaseModel):
    """
    Gerencia os tempos de espera (cooldowns) do usuário.

    Attributes:
        daily (`Optional[datetime]`): Cooldown diário.
        reputation (`Optional[datetime]`): Cooldown de reputação.
        married (`Optional[datetime]`): Cooldown para se casar novamente após o divorcio.
        premium_expiration (`Optional[datetime]`): Data de expiração do status premium.
    """
    daily: Optional[datetime] = None
    reputation: Optional[datetime] = None
    married: Optional[datetime] = None
    premium_expiration: Optional[datetime] = Field(alias='premiumExpiration', default=None)

    class Config:
        frozen = True
        validate_by_name = True

class UserMarried(BaseModel):
    """
    Representa as informações de casamento do usuário.

    Attributes:
        married (`bool`): Indica se o usuário está casado.
        division_of_assets (`Optional[bool]`): Indica se há divisão de bens no casamento.
        married_with (`Optional[int]`): Id do usuário com quem está casado.
        since (`Optional[datetime]`): Data do casamento.
    """
    married: bool = Field(alias='married', default=False)
    division_of_assets: Optional[bool] = Field(alias='divisionOfAssets', default=None)
    married_with: Optional[int] = Field(alias='marriedWith', default=None)
    since: Optional[datetime] = None
    shared_pearls: Optional[int] = Field(alias='sharedPearls', default=None)

    class Config:
        frozen = True
        validate_by_name = True

class UserBan(BaseModel):
    """
    Representa as informações de banimento do usuário.

    Attributes:
        banned (`bool``): Indica se o usuário está banido.
        banned_by (`Optional[int]`): Id do usuário que baniu o usuário.
        banned_at (`Optional[datetime]`): Data do banimento.
        expires_at (`Optional[datetime]`): Data de expiração do banimento.
        reason (`Optional[str]`): Motivo do banimento.
    """
    banned: bool = False
    banned_by: Optional[int] = Field(alias='bannedBy', default=None)
    banned_at: Optional[datetime] = Field(alias='bannedAt', default=None)
    expires_at: Optional[datetime] = Field(alias='expiresAt', default=None)
    reason: Optional[str] = None

    class Config:
        frozen = True
        validate_by_name = True


class UserData(BaseModel):
    """
    Modelo principal de dados do usuário.

    Attributes:
        id (`int`): Identificador único do usuário (mapeado de `_id` no MongoDB).
        pearls (`int`): Quantidade de pérolas do usuário.
        experience (`float`): Experiência do usuário.
        reputation (`int`): Reputação do usuário.
        cai_uuid (`Optional[str]`): UUID do usuário.
        profile (`UserProfile`): Perfil do usuário.
        cooldowns (`UserCooldowns`): Cooldowns do usuário.
        ban (`UserBan`): Status de banimento do usuário.
    """
    id: int = Field(alias='_id')
    pearls: int = 0
    experience: float = 0.0
    reputation: int = 0
    cai_uuid: Optional[str] = Field(alias='caiUUID', default=None)
    profile: UserProfile = UserProfile()
    married: UserMarried = UserMarried()
    cooldowns: UserCooldowns = UserCooldowns()
    ban: UserBan = UserBan()

    class Config:
        validate_by_name = True
        frozen = True