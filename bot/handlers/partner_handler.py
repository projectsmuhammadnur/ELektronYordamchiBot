import json

import requests
from aiogram import types

from bot.buttons.reply_buttons import partner_buttons, main_menu_buttons
from bot.dispatcher import dp, bot
from aiogram.dispatcher.filters import Text
from bot.buttons.text import partner, partner_ru, yes
from bot.handlers import partner_group_id


@dp.message_handler(Text(equals=[partner, partner_ru]))
async def partner_function(msg: types.Message):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/telegram-users/chat_id/{msg.from_user.id}/").content)
    if tg_user['language'] == 'uz':
        await msg.answer(text="""
        
    Bu yerda siz sotuvchi yoki sotib oluvchi sifatida hamkorlikni yo'lga qo'yishingiz mumkin.

    Kiritilgan ma'lumotlar asosida biz sizga mijoz yoki xaridor topib berishga harakat qilamiz
""", reply_markup=await partner_buttons())
    else:
        await msg.answer(text="""
        
    Здесь вы можете наладить сотрудничество в качестве продавца или покупателя.
    
    На основании введенной информации мы постараемся найти Вам клиента или покупателя.""",
                         reply_markup=await partner_buttons())


@dp.message_handler(Text(yes))
async def partner_function_2(msg: types.Message):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/telegram-users/chat_id/{msg.from_user.id}/").content)
    await bot.send_message(chat_id=partner_group_id, text=f"""
Yangi ariza 🆕
ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Ism-Familia: {tg_user['full_name']}
Telefon raqam: {tg_user['phone_number']}
Username: @{msg.from_user.username}""", parse_mode="HTML")
    if tg_user['language'] == 'uz':
        await msg.answer(text="Arizangiz yuborildi ✅\n\nTez orada aloqaga chiqamiz😊",
                         reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer(text="Ваша заявка отправлена ✅\n\nМы скоро свяжемся с вами😊",
                         reply_markup=await main_menu_buttons(msg.from_user.id))
