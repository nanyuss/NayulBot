from pydantic import BaseModel

from typing import List

class Settings(BaseModel):
    """
    Representa as configurações do bot.

    Args:
        staffs (`List[int]`): Lista de IDs dos staffs do bot.
    """
    _id: int = 0
    staffs: List[int] = []

    class Config:
        validate_by_name = True