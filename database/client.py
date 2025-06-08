import logging
from motor.motor_asyncio import AsyncIOMotorClient

from env import ENV
from database.user_db import MongoUserDB
from database.skin_db import SkinDB
from database.settings_db import SettingsDB

log = logging.getLogger(__name__)

class DatabaseClient:
    """
    Gerencia a conexão com o banco de dados MongoDB.
    """
    def __init__(self, **kwargs):
        self.user: MongoUserDB = kwargs.get('user')
        self.skin: SkinDB = kwargs.get('skin')
        self.settings: SettingsDB = kwargs.get('settings')


    @classmethod
    async def connect(cls) -> 'DatabaseClient':
        """
        Conecta ao banco de dados MongoDB.

        Returns:
            DatabaseClient: Uma instância da classe DatabaseClient.
        """
        try:
            client = AsyncIOMotorClient(ENV.MONGO)
            return cls(
                user=MongoUserDB(client),
                skin=SkinDB(client),
                settings=SettingsDB(client)
            )
        except Exception:
            log.critical('Não foi possível conectar ao MongoDB.', exc_info=True)
            raise ConnectionError('Não foi possível conectar ao MongoDB.')