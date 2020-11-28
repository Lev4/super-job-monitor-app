import logging

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from utils.db_api.dbutils import get_num_vacancies
from keyboards.inline.choice_buttons import choice, second_choice
from loader import dp


@dp.message_handler(Command("get_vacancies"))
async def show_items(message: Message):
    num_vacancies = get_num_vacancies()

    await message.answer(text=f" У нас есть {num_vacancies} вакасний", reply_markup=choice)


# Попробуйем отловить по встроенному фильтру, где в нашем call.data содержится "pear"
@dp.callback_query_handler(text_contains="Вперед")
async def buying_pear(call: CallbackQuery):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=10)

    callback_data = call.data

    # Отобразим что у нас лежит в callback_data
    # logging.info(f"callback_data='{callback_data}'")
    # В питоне 3.8 можно так
    logging.info(f"{callback_data}")

    await call.message.answer("ОК идем вперед.",
                              reply_markup=second_choice)


# Попробуем использовать фильтр от CallbackData
@dp.callback_query_handler(text_contains="Назад")
async def buying_apples(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)

    # Выведем callback_data и тут, чтобы сравнить с предыдущим вариантом.
    logging.info(f"{callback_data}")

    quantity = callback_data.get("quantity")
    await call.message.answer(f"Окей идем назад.",
                              reply_markup=second_choice)


@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: CallbackQuery):
    # Ответим в окошке с уведомлением!
    await call.answer("Вы все отменили!", show_alert=True)

    # Вариант 1 - Отправляем пустую клваиатуру изменяя сообщение, для того, чтобы ее убрать из сообщения!
    await call.message.edit_reply_markup(reply_markup=None)


