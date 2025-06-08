from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Literal

from database.models.skin import ProfileSkin

class SkinDB:
    def __init__(self, client: AsyncIOMotorClient):
        self.collection = client['nayul']['skins']

    async def get_skins(self) -> list[ProfileSkin]:
        """
        Obtém as skins de perfil do banco de dados.

        Returns:
            list[ProfileSkin]: As skins de perfil.
        """
        data: Optional[list[dict]] = await self.collection.find().to_list(length=None)
        if data is None:
            return []
        return [ProfileSkin(**skin) for skin in data]
    
    async def get_skin(self, skin_id: str) -> Optional[ProfileSkin]:
        """
        Obtém uma skin de perfil do banco de dados.

        Args:
            skin_id (`str`): O ID da skin a ser obtida.

        Returns:
            ProfileSkin: A skin de perfil.
        """
        data: Optional[dict] = await self.collection.find_one({'_id': skin_id})
        if data is None:
            return None
        return ProfileSkin(**data)
    
    async def remove_skin(self, skin_id: str) -> None:
        """
        Remove uma skin de perfil do banco de dados.

        Args:
            skin_id (`str`): O ID da skin a ser removida.
        """
        await self.collection.delete_one({'_id': skin_id})

    async def add_skin(self, skin_id: str, name: str, rarity: Literal[0, 1, 2, 3, 4], price: int, description: str, url: str) -> None:
        """
        Adiciona uma nova skin de perfil ao banco de dados.

        Args:
            skin_id (`str`): O ID da nova skin.
            name (`str`): Nome da skin.
            price (`int`): Preço da skin em pérolas.
            rarity (`Literal[0, 1, 2, 3, 4]`): Raridade da skin.
            description (`Optional[str]`): Descrição da skin.
            url (`str`): URL da imagem da skin.
        """
        await self.collection.insert_one({'_id': skin_id, 'name': name, 'price': price, 'rarity': rarity, 'description': description, 'url': url})

    async def update_skin(self, skin_id: str, *, name: Optional[str] = None, rarity: Optional[Literal[0, 1, 2, 3, 4]] = None, price: Optional[int] = None, description: Optional[str] = None, url: Optional[str] = None) -> None:
        """
        Atualiza uma skin de perfil no banco de dados.

        Args:
            skin_id (`str`): O ID da skin a ser atualizada.
            name (`Optional[str]`): Novo nome da skin.
            price (`Optional[int]`): Novo preço da skin em pérolas.
            rarity (`Optional[Literal[0, 1, 2, 3, 4]]`): Nova raridade da skin.
            description (`Optional[str]`): Nova descrição da skin.
            url (`Optional[str]`): Nova URL da imagem da skin.

        Raises:
            ValueError: Se nenhum valor for fornecido para atualização.
            ValueError: Se a skin não for encontrada com o ID fornecido.
        """
        
        update_data = {k: v for k, v in {
            'name': name,
            'rarity': rarity,
            'price': price,
            'description': description,
            'url': url
        }.items() if v is not None}

        if not update_data:
            raise ValueError('Pelo menos um valor deve ser fornecido para atualização.')

        if await self.get_skin(skin_id) is None:
            raise ValueError('Skin não encontrada com o ID fornecido.')

        await self.collection.update_one({'_id': skin_id}, {'$set': update_data})