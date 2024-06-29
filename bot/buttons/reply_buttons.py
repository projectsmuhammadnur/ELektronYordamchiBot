import json

import requests
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.buttons.text import back_main_menu, adverts, none_advert, forward_advert, back_admin_menu, back_main_menu_ru, \
    choice_language, choice_language_ru, sell, buy, offer, complaint, sell_ru, buy_ru, offer_ru, complaint_ru, partner, \
    partner_ru, yes, no, business_card, business_card_ru, directory_ru, directory


async def main_menu_buttons(chat_id: int):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/telegram-users/chat_id/{chat_id}/").content)
    if tg_user['language'] == 'uz':
        design = [
            [sell, buy],
            [partner, business_card],
            [directory],
            [offer, complaint],
            [choice_language]
        ]
    else:
        design = [
            [sell_ru, buy_ru],
            [directory_ru],
            [partner_ru, business_card_ru],
            [offer_ru, complaint_ru],
            [choice_language_ru]
        ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def back_main_menu_button(chat_id: int):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/telegram-users/chat_id/{chat_id}/").content)
    if tg_user['language'] == 'uz':
        design = [[back_main_menu]]
    else:
        design = [[back_main_menu_ru]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def back_admin_menu_button():
    design = [[back_admin_menu]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def admin_menu_buttons():
    design = [
        [adverts],
        [back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def advert_menu_buttons():
    design = [
        [none_advert, forward_advert],
        [back_admin_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def partner_buttons():
    design = [
        [no, yes]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def location_buttons(chat_id: int):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/telegram-users/chat_id/{chat_id}/").content)
    if tg_user['language'] == 'uz':
        design = [
            [KeyboardButton(text="JOYLASHUV 📍", request_location=True)],
            [back_main_menu]
        ]
    else:
        design = [
            [KeyboardButton(text="РАСПОЛОЖЕНИЕ 📍", request_location=True)],
            [back_main_menu_ru]
        ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
