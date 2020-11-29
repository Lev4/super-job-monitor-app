import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from utils.db_api.dbutils import get_vacancy_obj, get_vacancies_by_key_words
from dbsrc import VacancyMessage
from keyboards.inline.choice_buttons import choice, second_choice
from loader import dp


@dp.message_handler(Command("get_vacancies"))
async def show_items(message: Message, state: FSMContext):
    list_of_vacs = get_vacancies_by_key_words()
    num_vacancies = len(list_of_vacs)

    if list_of_vacs:
        async with state.proxy() as data:
            data["current_vacancy_id"] = list_of_vacs[0]
            data["all_vacs"] = list_of_vacs

        data = await state.get_data()

        await message.answer(text = f" У нас нашлось {num_vacancies} вакасний", reply_markup = choice)
    else:
        await message.answer(text = f"Поэтому запросу ничего не удалось найти", reply_markup = None)


# Попробуйем отловить по встроенному фильтру, где в нашем call.data содержится "look"
@dp.callback_query_handler(text = "look")
async def take_a_look(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cur_vacancy_id = data.get("current_vacancy_id")
    list_of_vacs = data.get("all_vacs")
    cur_vac_ix = list_of_vacs.index(cur_vacancy_id)

    callback_data = call.data
    logging.info(f"{callback_data} {cur_vacancy_id}")
    #
    # new_vacancy = vac_nav_dict[cur_vacancy_id].next_id()
    # await state.update_data(current_vacancy_id = new_vacancy)
    #
    vobj = get_vacancy_obj(cur_vacancy_id)
    vmessage = VacancyMessage(vobj)
    vtitle, vbody, vid = vmessage.make_message()

    if cur_vac_ix < len(list_of_vacs):
        async with state.proxy() as data:
            data["next_vacancy_id"] = list_of_vacs[cur_vac_ix + 1]

    await call.message.answer(f'{vtitle}')
    if isinstance(vbody, list):
        for el in vbody:
            await call.message.answer(f'{el}')
        await call.message.answer('Конец описания вакансии', reply_markup = second_choice)
    else:
        await call.message.answer(f'{vbody}', reply_markup = second_choice)



#
# Попробуйем отловить по встроенному фильтру, где в нашем call.data содержится "next"
@dp.callback_query_handler(text_contains = "next")
async def step_forward(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cur_vacancy_id = data.get("next_vacancy_id")
    list_of_vacs = data.get("all_vacs")
    cur_vac_ix = list_of_vacs.index(cur_vacancy_id)
    next_vacancy_id = None
    if cur_vac_ix < len(list_of_vacs):
        next_vacancy_id = list_of_vacs[cur_vac_ix + 1]

    async with state.proxy() as data:
        data["next_vacancy_id"] = next_vacancy_id
        data["previous_vacancy_id"] = cur_vacancy_id

    callback_data = call.data
    logging.info(f"{callback_data} {cur_vacancy_id} {next_vacancy_id}")

    vobj = get_vacancy_obj(cur_vacancy_id)
    vmessage = VacancyMessage(vobj)
    vtitle, vbody, vid = vmessage.make_message()

    logging.info(f"{vtitle} {vbody} {vid}")

    await call.message.answer(f'{vtitle}')
    if isinstance(vbody, list):
        for el in vbody:
            await call.message.answer(f'{el}')
        await call.message.answer('Конец описания вакансии', reply_markup = second_choice)
    else:
        await call.message.answer(f'{vbody}', reply_markup = second_choice)


#
#
#
# Попробуйем отловить по встроенному фильтру, где в нашем call.data содержится "back"
@dp.callback_query_handler(text_contains = "back")
async def step_back(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    cur_vacancy_id = data.get("previous_vacancy_id")
    if cur_vacancy_id:
        list_of_vacs = data.get("all_vacs")
        cur_vac_ix = list_of_vacs.index(cur_vacancy_id)

        next_vacancy_id = None
        if cur_vac_ix < len(list_of_vacs):
            next_vacancy_id = list_of_vacs[cur_vac_ix + 1]

        previous_vacancy_id = None
        if cur_vac_ix > 0:
            previous_vacancy_id = list_of_vacs[cur_vac_ix - 1]

        async with state.proxy() as data:
            data["next_vacancy_id"] = next_vacancy_id
            data["previous_vacancy_id"] = previous_vacancy_id

        callback_data = call.data
        logging.info(f"{callback_data} {cur_vacancy_id} {previous_vacancy_id}")

        vobj = get_vacancy_obj(cur_vacancy_id)
        vmessage = VacancyMessage(vobj)
        vtitle, vbody, vid = vmessage.make_message()
        logging.info(f"{vtitle} {vbody} {vid}")

        await call.message.answer(f'{vtitle}')

        if isinstance(vbody, list):
            for el in vbody:
                await call.message.answer(f'{el}')
            await call.message.answer('Конец описания вакансии', reply_markup = second_choice)
        else:
            await call.message.answer(f'{vbody}', reply_markup = second_choice)

    else:
        await call.message.answer(f'Предыдущих вакансий нет')


@dp.callback_query_handler(text = "cancel")
async def cancel_buying(call: CallbackQuery, state: FSMContext):
    # Ответим в окошке с уведомлением!
    await call.answer("Вы все отменили!", show_alert = True)

    # Вариант 1 - Отправляем пустую клваиатуру изменяя сообщение, для того, чтобы ее убрать из сообщения!
    await call.message.edit_reply_markup(reply_markup = None)
    await state.reset_state()
