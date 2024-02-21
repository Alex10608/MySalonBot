from aiogram.filters import BaseFilter
from aiogram.types import Message
from datetime import date


class CorrectDateFilter(BaseFilter):
    async def __call__(self, message: Message):
        try:
            d, m, y = message.text.split('.')
            is_correct_date = date(year=y, month=m, day=d)
        except:
            return False
        return True


class CorrectPhoneFilter(BaseFilter):
    async def __call__(self, message: Message):
        number = list(filter(lambda x: x.isdigit(), message.text))
        
        return len(number) == 10 or (len(number) == 11 and number[0] in (7, 8))

