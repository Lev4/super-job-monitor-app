import logging
from aiogram.dispatcher import FSMContext
from states.vacancies import Vacancies, previous_current_next, VacNavigator
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from utils.db_api.dbutils import get_num_vacancies, get_first_vacancy_id, get_vacancy_obj,get_vacancies
from dbsrc import VacancyMessage
from keyboards.inline.choice_buttons import choice, second_choice
from loader import dp



@dp.message_handler(Command("get_vacancies"))
async def show_items(message: Message, state: FSMContext):
    num_vacancies = get_num_vacancies()
    list_of_vacs = get_vacancies()
    if list_of_vacs:

        Vacancies.Q2_current.set()

        await state.update_data(current_vacancy_id = list_of_vacs[0])
        await state.update_data(all_vacs = list_of_vacs)

        list_of_tups = list(previous_current_next(list_of_vacs))
        await state.update_data(all_vacs_tuples = list_of_tups)
        vac_navigators = [VacNavigator(tup) for tup in list_of_tups]
        vac_navigators_dict = {v.current_id: v for v in vac_navigators}
        await state.update_data(vac_nav_dict = vac_navigators_dict)
        await Vacancies.next()
        await message.answer(text=f" У нас нашлось {num_vacancies} вакасний", reply_markup=choice)
    else:
        await message.answer(text = f"Поэтому запросу ничего не удалось найти", reply_markup=None)


# Попробуйем отловить по встроенному фильтру, где в нашем call.data содержится "look"
@dp.callback_query_handler(text_contains="look")
async def take_a_look(call: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    cur_vacancy_id = data.get("current_vacancy_id")
    vac_nav_dict = data.get("vac_nav_dict")

    callback_data = call.data
    logging.info(f"{callback_data} {cur_vacancy_id}")

    new_vacancy = vac_nav_dict[cur_vacancy_id].next_id()
    await state.update_data(current_vacancy_id = new_vacancy)

    vobj = get_vacancy_obj(cur_vacancy_id)
    vmessage = VacancyMessage(vobj)
    vtitle, vbody, vid = vmessage.make_message()
    await call.message.answer(f'{vtitle}')
    await call.message.answer(f'{vbody}', reply_markup=second_choice)


# Попробуйем отловить по встроенному фильтру, где в нашем call.data содержится "next"
@dp.callback_query_handler(text_contains="next")
async def step_forward(call: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    cur_vacancy_id = data.get("current_vacancy_id")
    vac_nav_dict = data.get("vac_nav_dict")

    callback_data = call.data
    logging.info(f"{callback_data} {cur_vacancy_id}")

    new_vacancy = vac_nav_dict[cur_vacancy_id].next_id()
    await state.update_data(current_vacancy_id = new_vacancy)

    vobj = get_vacancy_obj(cur_vacancy_id)
    vmessage = VacancyMessage(vobj)
    vtitle, vbody, vid = vmessage.make_message()
    await call.message.answer(f'{vtitle}')
    await call.message.answer(f'{vbody}', reply_markup = second_choice)



# Попробуйем отловить по встроенному фильтру, где в нашем call.data содержится "back"
@dp.callback_query_handler(text_contains="back")
async def step_back(call: CallbackQuery, state:FSMContext):

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


