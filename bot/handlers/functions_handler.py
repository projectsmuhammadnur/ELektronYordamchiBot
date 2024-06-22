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
    Bu yerda siz:
    Xo'jalik mollari
    Qurilish mahsulotlari 
    Maishiy texnikalar
    Mebel va uy jihozlari
    Telefon va aksessuarlar 
    Ishlatishga yaroqli barcha buyumlaringizni sotish imkoniga egasiz
    *faqatgina uy va avtomobil old-sotdisi bundan mustasno
    Tovarlarni sotish jarayonida har ikki tomondan halollik va savdo qonun-qoidalarga bo'ysunish talab etiladi""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))
    else:
        await msg.answer(text="""
    Вот ты:
    Домашние товары
    Строительная продукция 
    Бытовая техника
    Мебель и бытовая техника
    Телефон и аксессуары 
    Вы можете продать все свои полезные предметы
    *кроме предварительной продажи дома и автомобиля
    В процессе реализации товаров требуется честность и соблюдение торгового законодательства с обеих сторон.""",
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
    Bu yerdan siz yangi xo'jalik va qurilish mollarini, turli xildagi aksessuarlarni xarid qilishingiz mumkin. 
    Buning uchun sizdan mahsulot nomi yoki suratini ilova qilgan holda izlash talab etiladi
    Bot orqali xarid qilish jarayonida har ikki tomondan halollik va savdo qonun-qoidalariga rioya qilish talab etiladi. Mahsulot sotib olayotganda sotuvchidan chek talab qilishni unutmang!""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))
    else:
        await msg.answer(text="""
    Здесь вы можете купить новые товары для дома и строительства, различные аксессуары. 
    Для этого попросите выполнить поиск по названию продукта или прикрепленному изображению.
    Требуйте честности и справедливой торговой практики от обеих сторон процесса совершения покупок с помощью ботов. При покупке товара запросите у продавца чек!""",
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
    Bu yerda siz o'z takliflaringizni qoldirishingiz mumkin. 
    Bot foydalanuvchilariga o'z xizmatingizni taklif qilishni istasangiz, shu yerda murojaat qoldirasiz. Biz esa sizning xizmatingizni mijozlarga taqdim etamiz.
    Buning uchun vizitka bo'limiga o'tib, o'zingiz uchun vizitka olishingiz shart


    Taklifingizni matn formatida yuboring 📄""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))
    else:
        await msg.answer(text="""
    Здесь вы можете оставить свои предложения. 
    Если вы хотите предложить свою услугу пользователям ботов, вы можете оставить заявку здесь. И мы предоставляем ваши услуги клиентам.
    Для этого вам необходимо зайти в раздел визитки и приобрести визитку себе.
        
    Отправьте ваше предложение в текстовом формате 📄""",
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
    Bu yerda siz o'z shikoyatlaringizni qoldirishingiz mumkin. 
    Qonun-qoidalarga amal qilmagan har qanday sotuvchi yoki xaridor darhol qora ro'yxatga kiritilib, bloklanadi. Bloklangan raqam orqali botdan qayta foydalana olmaydi
    Har bir foydalanuvchi asosli shikoyat qoldirish huquqiga ega.

    Shikoyatingizni matn formatida yuboring 📄""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))
    else:
        await msg.answer(text="""
    Здесь вы можете оставить свои жалобы. 
    Любой продавец или покупатель, не соблюдающий правила, будет немедленно занесен в черный список и заблокирован. Не могу снова использовать бота из-за заблокированного номера
    Каждый пользователь имеет право подать обоснованную жалобу.

    Отправьте жалобу в текстовом формате 📄""",
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
    Botimizda o'z xizmat va mahsulotlarini taklif qiluvchi har bir a'zosi o'z vizitkasiga ega bo'lishi shart.
    Buning uchun pastda o'z ma'lumotlaringizni qoldirasiz va biz sizga shaxsiy tashrif qog'ozini tayyorlab beramiz

    Joylashuvingizni tugma orqali yuboring 👇""",
                         reply_markup=await location_buttons(msg.from_user.id))
    else:
        await msg.answer(text="""
    Каждый участник, предлагающий свои услуги и продукты с помощью нашего бота, должен иметь собственную визитную карточку.
    Для этого вы оставляете свои данные ниже и мы подготовим для вас персональную визитку

    Укажите свое местоположение через кнопку 👇""",
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
