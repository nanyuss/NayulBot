from pydantic import BaseModel, Field

from typing import Optional, Literal

class ProfileSkin(BaseModel):
    """
    Representa uma skin de perfil.

    Attributes:
        id (`str`): ID único da skin.
        name (`str`): Nome da skin.
        price (`int`): Preço da skin em pérolas.
        rarity (`Literal[0, 1, 2, 3, 4]`): Raridade da skin.
        description (`Optional[str]`): Descrição da skin.
        url (`str`): URL da imagem da skin.
    """
    id: str = Field(alias='_id')
    name: str
    price: int
    rarity: Literal[0, 1, 2, 3, 4]
    description: Optional[str] = None
    url: str

    class Config:
        frozen = True
        validate_by_name = True