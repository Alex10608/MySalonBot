from aiogram.filters import BaseFilter
from aiogram.types import Message
from datetime import date


class CorrectDateFilter(BaseFilter):
    async def __call__(self, message: Message):
        try:
            d, m, y = [int(i) for i in message.text.split('.')]
            is_correct_date = date(year=y, month=m, day=d)
            return {'birthday': is_correct_date}
        except:
            return False


class CorrectPhoneFilter(BaseFilter):
    async def __call__(self, message: Message):
        number = ''.join(filter(lambda x: x.isdigit(), message.text))
        if len(number) == 10:
            correct_number = f'8{number}'
        elif len(number) == 11 and int(number[0]) in (7, 8):
            correct_number = f'8{number[1:]}'
        else:
            return False
        return {'phone_number': correct_number}

        


