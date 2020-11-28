from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import buy_callback, back_callback, next_callback



# Первый чойс_выбираем
choice = InlineKeyboardMarkup(row_width=2)
go_look = InlineKeyboardButton(text="Посмотреть", callback_data="look")
choice.insert(go_look)

cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
choice.insert(cancel_button)

#Второй чойс
second_choice = InlineKeyboardMarkup(row_width=3)
go_forward = InlineKeyboardButton(text="Вперед", callback_data='next'),
second_choice.insert(go_forward)

go_back = InlineKeyboardButton(text="Назад", callback_data='back'),
second_choice.insert(go_back)

cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
second_choice.insert(cancel_button)





# # А теперь клавиатуры со ссылками на товары
# pear_keyboard = InlineKeyboardMarkup(inline_keyboard=[
#     [
#         InlineKeyboardButton(text="Купи тут", url="https://rozetka.com.ua/champion_a00225/p27223057")
#     ]
# ])
# apples_keyboard = InlineKeyboardMarkup(inline_keyboard=[
#     [
#         InlineKeyboardButton(text="Купи тут", url="https://freshmart.com.ua/product/yabloko-gala-116.html")
#     ]
# ])
