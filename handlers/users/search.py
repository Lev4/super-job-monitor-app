import logging

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from utils.db_api.dbutils import get_num_vacancies, get_first_vacancy_id
from keyboards.inline.choice_buttons import choice, second_choice
from loader import dp


@dp.message_handler(Command("get_vacancies"))
async def show_items(message: Message):
    num_vacancies = get_num_vacancies()

    await message.answer(text=f" У нас есть {num_vacancies} вакасний", reply_markup=choice)


# Попробуйем отловить по встроенному фильтру, где в нашем call.data содержится "look"
@dp.callback_query_handler(text_contains="look")
async def take_a_look(call: CallbackQuery):

    callback_data = call.data
    logging.info(f"{callback_data}")
    first_vacancy_id = get_first_vacancy_id()
    # num_vacancies = get_num_vacancies()
    await call.message.answer(f'OK {first_vacancy_id}')
    await call.message.answer(f"ОК идем вперед",
                              reply_markup=second_choice)

# Попробуйем отловить по встроенному фильтру, где в нашем call.data содержится "next"
@dp.callback_query_handler(text_contains="next")
async def step_forward(call: CallbackQuery):

    await call.answer(cache_time=10)
    callback_data = call.data

    logging.info(f"{callback_data}")

    # next_vacancy_id = get_next_vacancy_id()

    await call.message.answer("ОК идем вперед.",
                              reply_markup=second_choice)



# Попробуйем отловить по встроенному фильтру, где в нашем call.data содержится "back"
@dp.callback_query_handler(text_contains="back")
async def step_forward(call: CallbackQuery):

    await call.answer(cache_time=10)
    callback_data = call.data

    logging.info(f"{callback_data}")

    # next_vacancy_id = get_next_vacancy_id()

    await call.message.answer("ОК идем назад.",
                              reply_markup=second_choice)



@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: CallbackQuery):
    # Ответим в окошке с уведомлением!
    await call.answer("Вы все отменили!", show_alert=True)

    # Вариант 1 - Отправляем пустую клваиатуру изменяя сообщение, для того, чтобы ее убрать из сообщения!
    await call.message.edit_reply_markup(reply_markup=None)


