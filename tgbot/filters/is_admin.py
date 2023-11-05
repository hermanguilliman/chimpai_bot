from aiogram.filters import BaseFilter
from aiogram.types import Message


class AdminFilter(BaseFilter):
    def __init__(self, admin_list: list[int]):
        self.admin_list = admin_list

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_list