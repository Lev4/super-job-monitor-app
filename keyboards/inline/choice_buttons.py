from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import buy_callback, back_callback, next_callback



# Первый чойс
choice = InlineKeyboardMarkup(row_width=2)
go_forward = InlineKeyboardButton(text="Вперед", callback_data=next_callback.new('next')),
choice.insert(go_forward)

cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
choice.insert(cancel_button)

#Второй чойс
second_choice = InlineKeyboardMarkup(row_width=3)
go_forward = InlineKeyboardButton(text="Вперед", callback_data=next_callback.new('next')),
second_choice.insert(go_forward)

go_back = InlineKeyboardButton(text="Назад", callback_data=back_callback.new('back')),
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
