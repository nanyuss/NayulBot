import discord
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Union

from database.models.user import UserData

log = logging.getLogger(__name__)

class MongoUserDB:
    def __init__(self, client: AsyncIOMotorClient):
        self.collection = client['global']['users']

    async def create_user_account(self, user: Union[discord.Member, discord.User]):
        """
        Cria uma conta de usuário no banco de dados.

        Args:
            user (Union[discord.Member, discord.User]): O usuário para criar a conta.
        """
        await self.collection.insert_one(
            UserData(id=user.id).model_dump(by_alias=True)
        )

    async def get_user(self, user: Union[discord.Member, discord.User]) -> UserData:
        """
        Obtém os dados de um usuário do banco de dados.

        Args:
            user (Union[discord.Member, discord.User]): O usuário para obter os dados.

        Returns:
            UserData: Os dados do usuário.
        """
        data: Optional[dict] = await self.collection.find_one({'_id': user.id})
        if data is None:
            return UserData(id=user.id)
        return UserData(**data)
    
    async def update_user(self, user: Union[discord.Member, discord.User], query: dict) -> None:
        """
        Atualiza os dados de um usuário no banco de dados.

        Args:
            user (Union[discord.Member, discord.User]): O usuário para atualizar os dados.
            query (dict): Os dados a serem atualizados.
        """
        await self.collection.update_one({'_id': user.id}, query)