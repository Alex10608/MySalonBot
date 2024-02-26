from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import CallbackQuery, Message
from lexicon.lexicon_ru import GREETING
from filters.filters import CorrectPhoneFilter, CorrectDateFilter
from keyboards.sex_kb import sex_markup
from keyboards.cancel_kb import cancel_markup


router = Router()
user_dict = {}


class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_birthday = State()
    fill_sex = State()


@router.message(CommandStart())
async def process_start_cmd(message: Message):
    await message.answer(text=GREETING)


@router.message(Command('showdata'), StateFilter(default_state))
async def process_showdata_cmd(message: Message):
    if message.from_user.id in user_dict:
        await message.answer(
            f'Имя: {user_dict[message.from_user.id]["name"]}\n'
            f'Телефон: {user_dict[message.from_user.id]["phone"]}'
            f'Дата рождения: {user_dict[message.from_user.id]["birthday"]}\n'
            f'Пол: {user_dict[message.from_user.id]["sex"]}\n'
        )
    else:
        await message.answer(
            text='Вы еще не заполняли анкету. Чтобы приступить - введите номер телефона'
        )


@router.message(~CorrectPhoneFilter(), StateFilter(default_state))
async def incorrect_phone(message: Message):
    await message.answer(f'Проверьте корректность номера, возможно там не хватает цифр или есть лишние.')
    await message.answer(f'Пожалуйста, введите номер телефона.')


@router.callback_query(F.data == 'cancel')
async def process_calcel_cmd(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Вы вышли из анкеты. Для работы с ботом введите номер телефона')
    await state.clear()


@router.message(CorrectPhoneFilter(), StateFilter(default_state))
async def process_phone_cmd(message: Message, state: FSMContext, phone_number):
    """Хэндлер на проверку корректности номера. Дальше нужно проверить,
    есть ли телефон в базе. Если нет, запускать анкету"""
    await state.update_data(phone=phone_number)
    await message.answer(text=f'Пожалуйста, введите ваше имя.', reply_markup=cancel_markup)
    await state.set_state(FSMFillForm.fill_name)


@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text='Спасибо!\n\nА теперь введите вашу дату рождения в формате ДД.ММ.ГГГГ',
        reply_markup=cancel_markup
    )
    await state.set_state(FSMFillForm.fill_birthday)


@router.message(StateFilter(FSMFillForm.fill_name))
async def incorrect_name(message: Message):
    await message.answer(text=f'Введено некорректное имя.'
                         f'Имя должно состоять только из букв.'
                         f'Пожалуйста, введите ваше имя.',
                         reply_markup=cancel_markup
    )


@router.message(StateFilter(FSMFillForm.fill_birthday), CorrectDateFilter())
async def process_birthday_sent(message: Message, state: FSMContext):
    await state.update_data(birthday=message.text)
    await message.answer(
        text='Спасибо!\n\nУкажите ваш пол',
        reply_markup=sex_markup
    )
    await state.set_state(FSMFillForm.fill_sex)


@router.message(StateFilter(FSMFillForm.fill_birthday))
async def incorrect_date(message: Message):
    await message.answer(
        text='Введена некорректная дата. Попробуйте еще раз',
        reply_markup=cancel_markup
    )


@router.callback_query(StateFilter(FSMFillForm.fill_sex), F.data.in_(['male', 'female']))
async def process_sex_sent(callback: CallbackQuery, state: FSMContext):
    await state.update_data(sex=callback.data)

    user_dict[callback.from_user.id] = await state.get_data()
    await state.clear()
    await callback.message.answer(
        text='Спасибо! Ваши данные сохранены!\nЧтобы посмотреть анкету, отправьте команду /showdata'
    )
    await callback.answer()


@router.message(StateFilter(FSMFillForm.fill_sex))
async def incorrect_data(message: Message):
    await message.answer(
        text='Пожалуйста, воспользуйтесь кнопками!'
    )



