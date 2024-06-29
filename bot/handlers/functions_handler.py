import json

import requests
from aiogram.dispatcher import FSMContext
from bot.buttons.reply_buttons import main_menu_buttons, back_main_menu_button, location_buttons
from bot.buttons.text import sell, sell_ru, buy, buy_ru, offer, offer_ru, complaint, \
    complaint_ru, business_card, business_card_ru, directory, directory_ru
from bot.dispatcher import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import Text

from bot.handlers import geolocator

directory_channel_id = -1002245492491
sell_group_id = -1002226699457
buy_group_id = -1002183558449
offer_group_id = -1002180481619
complaint_group_id = -1002166274930
partner_group_id = -1002206274820
business_card_id = -1002196387423


@dp.message_handler(Text(equals=[sell, sell_ru]))
async def sell_function(msg: types.Message, state: FSMContext):
    await state.set_state("sell")
    if msg.text == sell:
        await msg.answer(text="""
Hurmatli sotuvchi siz bu yerda oʻzingizni telefon maxsulotlaringizni soting.

Eslatma: Sotuvda savdo qoidalari va halollikka amal qiling!""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))
    else:
        await msg.answer(text="""
Уважаемый продавец, пожалуйста, продавайте здесь свои товары для телефонов.

Напоминание: При продаже соблюдайте правила торговли и честность!""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))


@dp.message_handler(state="sell",
                    content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO, types.ContentType.TEXT])
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
    elif msg.content_type == types.ContentType.VIDEO:
        await bot.send_video(chat_id=sell_group_id, video=msg.video.file_id, caption=caption, parse_mode='HTML')
    else:
        await bot.send_message(chat_id=sell_group_id, text=f"{caption}\nAriza:\n{msg.text}", parse_mode='HTML')
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
Hurmatli mijoz barcha turdagi va rusumdagi telefonlarni bizdan sotib olishingiz mumkun.

Eslatma: Kelishuvda savdo qoidalari va halollikka amal qiling! Chek, garatiya va karobka-dokumentni olishni unutmang!""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))
    else:
        await msg.answer(text="""
Уважаемый клиент, вы можете купить у нас телефоны всех видов и марок.

Напоминание: При заключении сделки соблюдайте правила торговли и честность! Не забудьте взять чек, гарантию и коробку с документами!""",
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
        await msg.answer(text="""
Faoliyatimizni yaxshilash uchun siz tomoningizdan berilgan takliflar biz uchun judayam muhim!

Marhamat, taklifingizni qoldiring:""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))
    else:
        await msg.answer(text="""
Для улучшения нашей деятельности ваши предложения для нас очень важны!

Пожалуйста, оставьте своё предложение:""",
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
        await msg.answer(text="""
Xizmat yoki maxsulotdan, haridordan koʻnglingiz toʻlmadimi? Bot orqali shikoyatingizni qoldiring. 

Eslatma: Shikoyat olgan sotuvchi yoki haridor albatta bloklanadi va nazoratga olinadi!!!""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))
    else:
        await msg.answer(text="""
Не довольны услугой или продуктом, покупателем? Оставьте свою жалобу через бота.

Напоминание: Продавец или покупатель, получивший жалобу, обязательно будет заблокирован и взят под контроль!!!""",
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
        await msg.answer(text="""
Biz bilan hamkorlik qilishni istaysizmi? Marhamat shaxsiy ma'lumotlaringizni joʻnating va bizdan roʻyxatdan oʻtib, oʻz vizitkangizga ega boʻling! 

Dastlab joylashuvingizni koʻrsating:""",
                         reply_markup=await location_buttons(msg.from_user.id))
    else:
        await msg.answer(text="""

Хотите сотрудничать с нами? Пожалуйста, отправьте свои личные данные и зарегистрируйтесь у нас, чтобы получить свою визитку!

Сначала укажите своё местоположение:""",
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


@dp.message_handler(Text(equals=[directory, directory_ru]))
async def sell_function(msg: types.Message, state: FSMContext):
    await state.set_state("directory")
    if msg.text == directory:
        await msg.answer(text="""
Hurmatli sotuvchi siz bu yerda oʻzingizni telefon maxsulotlaringizni kanalga joylang.

Eslatma: Sotuvda savdo qoidalari va halollikka amal qiling!

E'lon berish tartibi

⌚️📱💻🖥 Rasm
📲 Nomi:
💾 Xotirasi:
🎨 Rangi:
🔧 Xolati:
📦📄 bor/yo'q
💰 Narxi:
☎️ Telefon:
✍️ User bo'lsa: @
🇺🇿 Manzil:

Eloningiz: @telefonlar_elektron_yordamchi - shu kanalda elon qilinadi""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))
    else:
        await msg.answer(text="""
Уважаемый продавец, пожалуйста, разместите свои телефонные товары по следующему шаблону на канале:

⌚️📱💻🖥 Разм
📲 Название:
💾 Память:
🎨 Цвет:
🔧 Состояние:
📦📄 Есть/нет
💰 Цена:
☎️ Телефон:
✍️ Пользователь: @
🇺🇿 Адрес:

Ваш канал: @telefonlar_elektron_yordamchi - объявления размещаются на этом канале"
Не забывайте соблюдать правила торговли и честность!""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))


@dp.message_handler(state="directory",
                    content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO, types.ContentType.TEXT])
async def sell_function_2(msg: types.Message, state: FSMContext):
    await state.finish()
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/telegram-users/chat_id/{msg.from_user.id}/").content)
    caption = f"""
Yangi telefon🆕

Username: @{msg.from_user.username}
Ism-Familiya: {tg_user['full_name']}
Telefon raqam: {tg_user['phone_number']}"""
    if msg.content_type == types.ContentType.PHOTO:
        await bot.send_photo(chat_id=directory_channel_id, photo=msg.photo[-1].file_id, caption=caption,
                             parse_mode='HTML')
    elif msg.content_type == types.ContentType.VIDEO:
        await bot.send_video(chat_id=directory_channel_id, video=msg.video.file_id, caption=caption, parse_mode='HTML')
    else:
        await bot.send_message(chat_id=directory_channel_id, text=f"{caption}\nMa'lumot:\n{msg.text}", parse_mode='HTML')
    if tg_user['language'] == 'uz':
        await msg.answer("Ariza yuborildi.\nTez orada aloqaga chiqamiz 😊",
                         reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer("Заявка отправлена.\nМы скоро свяжемся с вами 😊",
                         reply_markup=await main_menu_buttons(msg.from_user.id))
