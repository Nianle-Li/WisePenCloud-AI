from abc import ABC, abstractmethod
from typing import List

from beanie import PydanticObjectId

from chat.domain.entities.provider import Provider

class ProviderRepository(ABC):

    @abstractmethod
    async def get_provider(self, user_id: Optional[str] = None, provider_id: PydanticObjectId) -> Provider: pass

    @abstractmethod
    async def list_providers(self, user_id: Optional[str] = None) -> List[Provider]: pass

    @abstractmethod
    async def create_provider(self, user_id: Optional[str] = None, provider: Provider) -> Provider: pass

    @abstractmethod
    async def update_provider(self, user_id: Optional[str] = None, provider: Provider) -> Provider: pass

    @abstractmethod
    async def remove_provider(self, user_id: Optional[str] = None, provider_id: PydanticObjectId) -> None: pass
