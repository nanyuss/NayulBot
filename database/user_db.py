import discord
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Union, Literal
from datetime import datetime
from zoneinfo import ZoneInfo

from database.models.user import UserData

class UsersDB:
    def __init__(self, client: AsyncIOMotorClient):
        self.collection = client['global']['users']

    async def create_user_account(self, user: Union[discord.Member, discord.User]):
        """
        Cria uma conta de usuário no banco de dados.

        Args:
            user (`Union[discord.Member, discord.User]`): O usuário para criar a conta.
        """
        await self.collection.insert_one(
            UserData(id=user.id).model_dump(by_alias=True)
        )

    #---------- Get info ----------#

    async def get_user(self, user: Union[discord.Member, discord.User]) -> UserData:
        """
        Obtém os dados de um usuário do banco de dados.

        Args:
            user (`Union[discord.Member, discord.User]`): O usuário para obter os dados.

        Returns:
            UserData: Os dados do usuário.
        """
        data: Optional[dict] = await self.collection.find_one({'_id': user.id})
        if data is None:
            return UserData(id=user.id)
        return UserData(**data)
    
    #---------- Delete Info ----------#

    async def delete_user(self, user: Union[discord.Member, discord.User]) -> None:
        """
        Exclui um usuário do banco de dados.

        Args:
            user (`Union[discord.Member, discord.User]`): O usuário a ser excluído.
        """
        await self.collection.delete_one({'_id': user.id})
    
    #---------- Update info ----------#
    
    async def update_user(self, user: Union[discord.Member, discord.User], *, query: dict) -> None:
        """
        Atualiza os dados de um usuário no banco de dados.

        Args:
            user (`Union[discord.Member, discord.User`]): O usuário para atualizar os dados.
            query (`dict`): Os dados a serem atualizados.
        """
        await self.collection.update_one({'_id': user.id}, query)

    async def update_ban(self, user: Union[discord.Member, discord.User], banned: bool, banned_by: Optional[int] = None, expired_in: Optional[datetime] = None, reason: Optional[str] = None) -> None:
        """
        Atualiza o status de banimento de um usuário no banco de dados.

        Args:
            user (`Union[discord.Member, discord.User]`): O usuário para atualizar o status de banimento.
            banned (`bool`): Indica se o usuário está banido.
            banned_by (`Optional[int]`): ID do usuário que realizou o banimento.
            expired_in (`Optional[datetime]`): Data de expiração do banimento.
            reason (`Optional[str]`): Motivo do banimento.
        """
        user_data = await self.get_user(user)
        user_dict = user_data.model_dump(by_alias=True)

        user_dict['ban']['banned'] = banned
        user_dict['ban']['bannedBy'] = banned_by
        user_dict['ban']['bannedAt'] = None if not banned else datetime.now(tz=ZoneInfo('America/Sao_Paulo'))
        user_dict['ban']['expiresAt'] = expired_in
        user_dict['ban']['reason'] = reason

        await self.update_user(user, query={'$set': user_dict})

    async def update_skin(self, user: Union[discord.Member, discord.User], action: Literal['add', 'remove'], skin: str) -> None:
        """
        Atualiza a skin de um usuário no banco de dados.

        Args:
            user (`Union[discord.Member, discord.User]`): O usuário para atualizar a skin.
            acction (`Literal['add', 'remove']`): A ação a ser realizada.
            skin (`str`): A nova skin.
        """
        
        user_data = await self.get_user(user)
        user_dict = user_data.model_dump(by_alias=True)

        match action:
            case 'add':
                if skin not in user_dict['profile']['skins']: #Checa se a skin não está na lista de skins do usuário
                    user_dict['profile']['skins'].append(skin) #Adiciona a skin na lista de skins do usuário
            case 'remove':
                if skin in user_dict['profile']['skins']: #Checa se a skin está na lista de skins do usuário
                    user_dict['profile']['skins'].remove(skin) #Remove a skin da lista de skins do usuário
                    if user_dict['profile']['skin_now'] == skin: #Checa se a skin atual é a mesma que foi removida
                        user_dict['profile']['skin_now'] = 'default' #Se for, muda a skin atual para a padrão


        await self.update_user(user, query={'$set': user_dict})

    async def update_about_me(self, user: Union[discord.Member, discord.User], about_me: str) -> None:
        """
        Atualiza a descrição pessoal de um usuário no banco de dados.

        Args:
            user (`Union[discord.Member, discord.User]`): O usuário para atualizar a descrição pessoal.
            about_me (`str`): A nova descrição pessoal.
        """

        user_data = await self.get_user(user)
        user_dict = user_data.model_dump(by_alias=True)

        user_dict['profile']['aboutMe'] = about_me

        await self.update_user(user, query={'$set': user_dict})

    async def update_pearls(self, user: Union[discord.Member, discord.User], action: Literal['add', 'remove', 'set'], pearls: int) -> None:
        """
        Atualiza as perólas de um usuário no banco de dados.

        Args:
            user (`Union[discord.Member, discord.User]`): O usuário para atualizar as perólas.
            action (`Literal['add', 'remove', 'set']`): A ação a ser realizada.
            pearls (`int`): A nova quantidade de perólas.
        """

        user_data = await self.get_user(user)
        user_dict = user_data.model_dump(by_alias=True)

        match action:
            case 'add':
                user_dict['pearls'] += pearls
            case 'remove':
                user_dict['pearls'] -= pearls
            case 'set':
                user_dict['pearls'] = pearls

        await self.update_user(user, query={'$set': user_dict})

    async def update_experience(self, user: Union[discord.Member, discord.User], action: Literal['add', 'remove'], experience: float) -> None:
        """
        Atualiza a experiência de um usuário no banco de dados.

        Args:
            user (`Union[discord.Member, discord.User]`): O usuário para atualizar a experiência.
            action (`Literal['add', 'remove']`): A ação a ser realizada.
            experience (`float`): A nova experiência.
        """

        user_data = await self.get_user(user)
        user_dict = user_data.model_dump(by_alias=True)

        match action:
            case 'add':
                user_dict['experience'] += experience
            case 'remove':
                user_dict['experience'] -= experience

        await self.update_user(user, query={'$set': user_dict})

    async def update_reputation(self, user: Union[discord.Member, discord.User], action: Literal['add', 'remove'], reputation: int) -> None:
        """
        Atualiza a reputação de um usuário no banco de dados.

        Args:
            user (`Union[discord.Member, discord.User]`): O usuário para atualizar a reputação.
            action (`Literal['add', 'remove']`): A ação a ser realizada.
            reputation (`int`): A nova reputação.
        """

        user_data = await self.get_user(user)
        user_dict = user_data.model_dump(by_alias=True)

        match action:
            case 'add':
                user_dict['reputation'] += reputation
            case 'remove':
                user_dict['reputation'] -= reputation

        await self.update_user(user, query={'$set': user_dict})

    async def update_cai_uuid(self, user: Union[discord.Member, discord.User], cai_uuid: str) -> None:
        """
        Atualiza o UUID do usuário no banco de dados.

        Args:
            user (`Union[discord.Member, discord.User]`): O usuário para atualizar o cai UUID.
            cai_uuid (`str`): O novo UUID.
        """

        user_data = await self.get_user(user)
        user_dict = user_data.model_dump(by_alias=True)

        user_dict['caiUUID'] = cai_uuid

        await self.update_user(user, query={'$set': user_dict})

    async def update_married(self,
                    user: Union[discord.Member, discord.User],
                    married_with: Union[discord.Member, discord.User],
                    married: bool, division_of_assets: Optional[bool] = None, since: Optional[datetime] = None) -> None:
        """
        Atualiza o status de casamento de um usuário no banco de dados.

        Args:
            user (`Union[discord.Member, discord.User]`): O usuário para atualizar as informações de casamento. 
            married_with (`Union[discord.Member, discord.User]`): O usuário com o qual o usuário está casado.
            married (`bool`): Indica se o usuário está casado.
            division_of_assets (`Optional[bool]`): Indica se há divisão de bens no casamento.
            since (`Optional[datetime]`): Data do casamento.
        """
        user_data = await self.get_user(user)
        user_dict = user_data.model_dump(by_alias=True)

        married_with_data = await self.get_user(married_with)
        married_with_dict = married_with_data.model_dump(by_alias=True)

        if married:
            user_dict['married']['married'] = married
            user_dict['married']['marriedWith'] = married_with.id
            user_dict['married']['since'] = datetime.now(tz=ZoneInfo('America/Sao_Paulo'))
            user_dict['married']['divisionOfAssets'] = division_of_assets

            married_with_dict['married']['married'] = married
            married_with_dict['married']['marriedWith'] = user.id
            married_with_dict['married']['since'] = datetime.now(tz=ZoneInfo('America/Sao_Paulo'))
            married_with_dict['married']['divisionOfAssets'] = division_of_assets

            await self.update_shared_pearls(user, married_with)

        else:
            user_dict['married']['married'] = married
            user_dict['married']['marriedWith'] = None
            user_dict['married']['since'] = None
            user_dict['married']['divisionOfAssets'] = None

            married_with_dict['married']['married'] = False
            married_with_dict['married']['marriedWith'] = None
            married_with_dict['married']['since'] = married
            married_with_dict['married']['divisionOfAssets'] = None

        await self.update_user(user, query={'$set': user_dict})
        await self.update_user(married_with, query={'$set': married_with_dict})


    async def update_shared_pearls(self, user1: Union[discord.Member, discord.User], user2: Union[discord.Member, discord.User], division: bool = False) -> None:
        """
        Atualiza a quantidade de perólas compartilhadas dos noivos no banco de dados.

        Args:
            user1 (`Union[discord.Member, discord.User]`): O primeiro usuário.
            user2 (`Union[discord.Member, discord.User]`): O segundo usuário.
            division (`bool`): Indica se a divisão de perólas deve ser realizada.
        """

        user1_data = await self.get_user(user1)
        user1_dict = user1_data.model_dump(by_alias=True)

        user2_data = await self.get_user(user2)
        user2_dict = user2_data.model_dump(by_alias=True)

        total_shared_pearls = user1_dict['pearls'] + user2_dict['pearls']
        division_shared_perals = total_shared_pearls // 2

        if division:
            await self.update_pearls(user1, 'set', division_shared_perals)
            await self.update_pearls(user2, 'set', division_shared_perals)

        user1_dict['married']['sharedPearls'] = total_shared_pearls
        user2_dict['married']['sharedPearls'] = total_shared_pearls

        await self.update_user(user1, query={'$set': user1_dict})
        await self.update_user(user2, query={'$set': user2_dict})

    async def update_cooldowns(self, user: Union[discord.Member, discord.User],
                        cooldown: Literal['daily', 'reputation', 'married', 'premium_expiration'],
                        datetime_now: datetime) -> None:
        """
        Atualiza os cooldowns de um usuário no banco de dados.

        Args:
            user (`Union[discord.Member, discord.User]`): O usuário para atualizar os cooldowns.
            cooldown (`Literal['daily', 'reputation', 'married', 'premium_expiration']`): O cooldown a ser atualizado.
            timestamp (`datetime`): O novo timestamp do cooldown.
        """
        user_data = await self.get_user(user)
        user_dict = user_data.model_dump(by_alias=True)
        user_dict['cooldowns'][cooldown] = datetime_now
        await self.update_user(user, query={'$set': user_dict})