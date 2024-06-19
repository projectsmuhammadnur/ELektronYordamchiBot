import json

import requests
from aiogram.dispatcher import FSMContext
from bot.buttons.reply_buttons import main_menu_buttons, back_main_menu_button, location_buttons
from bot.buttons.text import sell, sell_ru, buy, buy_ru, offer, offer_ru, complaint, \
    complaint_ru, business_card, business_card_ru
from bot.dispatcher import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import Text

from bot.handlers import geolocator

sell_group_id = -4229963929
buy_group_id = -4181477016
offer_group_id = -4251053177
complaint_group_id = -4280972803
partner_group_id = -4234344396
business_card_id = -4271582747


@dp.message_handler(Text(equals=[sell, sell_ru]))
async def sell_function(msg: types.Message, state: FSMContext):
    await state.set_state("sell")
    if msg.text == sell:
        await msg.answer(text="""
Bu tugmacha orqali siz 
b/u
Qurilish materiallari 
Mebel 
Har xil turdagi bitavoy texnikalar
Turliy xil Telefonlar 
Barca eski nima tavarlaringiz yoki texnikangiz bo'lsa barchasini shu tugmacha orqaliy botimizga foto suratlari bilan joylashtirish savdoga qo'yish imkoniga egasiz.

Sotmoqchi bo'lgan maxsulotingizni rasm yoki video formatda tashlang 📷""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))
    else:
        await msg.answer(text="""
С помощью этой кнопки вы 
б/у
Строительные материалы 
Мебель 
Различные виды примитивных техник
Разные телефоны 
Барса, у вас есть возможность выставить на продажу все свои старые товары или технику на нашем боте с фотографиями, используя эту кнопку.

Разместите товар, который хотите продать, в формате изображения или видео 📷""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))


@dp.message_handler(state="sell", content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO])
async def sell_function_2(msg: types.Message, state: FSMContext):
    await state.finish()
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/telegram-users/chat_id/{msg.from_user.id}/").content)
    caption = f"""
Yangi ariza🆕
ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Username: @{msg.from_user.username}
Ism-Familiya: {tg_user['full_name']}
Telefon raqam: {tg_user['phone_number']}"""
    if msg.content_type == types.ContentType.PHOTO:
        await bot.send_photo(chat_id=sell_group_id, photo=msg.photo[-1].file_id, caption=caption,
                             parse_mode='HTML')
    else:
        await bot.send_video(chat_id=sell_group_id, video=msg.video.file_id, caption=caption, parse_mode='HTML')
    if tg_user['language'] == 'uz':
        await msg.answer("Ariza yuborildi.\nTez orada aloqaga chiqamiz 😊",
                         reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer("Заявка отправлена.\nМы скоро свяжемся с вами 😊",
                         reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.message_handler(Text(equals=[buy, buy_ru]))
async def buy_function(msg: types.Message, state: FSMContext):
    await state.set_state("buy")
    if msg.text == buy:
        await msg.answer(text="""
Bu tugmacha orqaliy siz
Yangi Qurilish Mollari va Xo'jalik Molarini Topishingiz Mumkin Bo'ladi
Buning uchun siz tavar nomi imkon bo'sa foto suratlarini ilova qilgan holda izlash imkoniga egasiz.

Sotib olmoqchi bo'lgan maxsulotingizni text, rasm yoki video formatda tasvirlang ℹ️""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))
    else:
        await msg.answer(text="""
Вы находитесь через эту кнопку
Вы можете найти новые строительные товары и товары для дома
Для этого у вас есть возможность поиска по названию товара, если это возможно, с прикрепленными фотографиями.
        
Опишите продукт, который вы хотите купить, в текстовом, графическом или видеоформате ℹ️""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))


@dp.message_handler(state="buy",
                    content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO, types.ContentType.TEXT])
async def buy_function_2(msg: types.Message, state: FSMContext):
    await state.finish()
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/telegram-users/chat_id/{msg.from_user.id}/").content)
    caption = f"""
Yangi ariza🆕
ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Username: @{msg.from_user.username}
Ism-Familiya: {tg_user['full_name']}
Telefon raqam: {tg_user['phone_number']}"""
    if msg.content_type == types.ContentType.PHOTO:
        await bot.send_photo(chat_id=buy_group_id, photo=msg.photo[-1].file_id, caption=caption,
                             parse_mode='HTML')
    elif msg.content_type == types.ContentType.VIDEO:
        await bot.send_video(chat_id=buy_group_id, video=msg.video.file_id, caption=caption, parse_mode='HTML')
    else:
        await bot.send_message(chat_id=buy_group_id, text=f"{caption}\nAriza:\n{msg.text}", parse_mode='HTML')
    if tg_user['language'] == 'uz':
        await msg.answer("Ariza yuborildi.\nTez orada aloqaga chiqamiz 😊",
                         reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer("Заявка отправлена.\nМы скоро свяжемся с вами 😊",
                         reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.message_handler(Text(equals=[offer, offer_ru]))
async def offer_function(msg: types.Message, state: FSMContext):
    await state.set_state("offer")
    if msg.text == offer:
        await msg.answer(text="Taklifingizni matn formatida yuboring 📄",
                         reply_markup=await back_main_menu_button(msg.from_user.id))
    else:
        await msg.answer(text="Отправьте ваше предложение в текстовом формате 📄",
                         reply_markup=await back_main_menu_button(msg.from_user.id))


@dp.message_handler(state="offer")
async def offer_function_2(msg: types.Message, state: FSMContext):
    await state.finish()
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/telegram-users/chat_id/{msg.from_user.id}/").content)
    await bot.send_message(chat_id=offer_group_id, text=f"""
Yangi Taklif🆕
ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Username: @{msg.from_user.username}
Ism-Familiya: {tg_user['full_name']}
Telefon raqam: {tg_user['phone_number']}\n\n
Taklif:\n{msg.text}""", parse_mode='HTML')
    if tg_user['language'] == 'uz':
        await msg.answer("Taklifingiz yuborildi.",
                         reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer("Ваше предложение отправлено.",
                         reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.message_handler(Text(equals=[complaint, complaint_ru]))
async def complaint_function(msg: types.Message, state: FSMContext):
    await state.set_state("complaint")
    if msg.text == complaint:
        await msg.answer(text="Shikoyatingizni matn formatida yuboring 📄",
                         reply_markup=await back_main_menu_button(msg.from_user.id))
    else:
        await msg.answer(text="Отправьте жалобу в текстовом формате 📄",
                         reply_markup=await back_main_menu_button(msg.from_user.id))


@dp.message_handler(state="complaint")
async def complaint_function_2(msg: types.Message, state: FSMContext):
    await state.finish()
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/telegram-users/chat_id/{msg.from_user.id}/").content)
    await bot.send_message(chat_id=complaint_group_id, text=f"""
Yangi shikoyat🆕
ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Username: @{msg.from_user.username}
Ism-Familiya: {tg_user['full_name']}
Telefon raqam: {tg_user['phone_number']}\n\n
Shikoyat:\n{msg.text}""", parse_mode='HTML')
    if tg_user['language'] == 'uz':
        await msg.answer("Shikoyatingiz yuborildi.",
                         reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer("Ваша жалоба отправлена.",
                         reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.message_handler(Text(equals=[business_card, business_card_ru]))
async def business_card_function(msg: types.Message, state: FSMContext):
    await state.set_state("business_card")
    if msg.text == business_card:
        await msg.answer(text="Joylashuvingizni tugma orqali yuboring 👇",
                         reply_markup=await location_buttons(msg.from_user.id))
    else:
        await msg.answer(text="Укажите свое местоположение через кнопку 👇",
                         reply_markup=await location_buttons(msg.from_user.id))


@dp.message_handler(state='business_card', content_types=types.ContentTypes.LOCATION)
async def business_card_function_2(msg: types.Message, state: FSMContext):
    await state.finish()
    lat = msg.location.latitude
    lon = msg.location.longitude
    location = geolocator.reverse((lat, lon), exactly_one=True)
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/telegram-users/chat_id/{msg.from_user.id}/").content)
    await bot.send_message(chat_id=business_card_id, text=f"""
Yangi vizitka uchun ariza🆕
ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Username: @{msg.from_user.username}
Ism-Familiya: {tg_user['full_name']}
Telefon raqam: {tg_user['phone_number']}
Manzil: {location}""", parse_mode='HTML')
    await bot.send_location(chat_id=business_card_id, latitude=lat, longitude=lon)
    if tg_user['language'] == 'uz':
        await msg.answer("Ariza yuborildi.\nTez orada aloqaga chiqamiz 😊",
                         reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer("Заявка отправлена.\nМы скоро свяжемся с вами 😊",
                         reply_markup=await main_menu_buttons(msg.from_user.id))
