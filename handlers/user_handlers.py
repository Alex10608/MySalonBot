from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message, KeyboardButton, MessageEntity, Contact
from lexicon.lexicon_ru import GREETING

router = Router()


@router.message(CommandStart())
async def process_start_cmd(message: Message):
    await message.answer(text=GREETING)


@router.message(F.text)
async def process_phone_cmd(message: Message):

    pass