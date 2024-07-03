import json
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from bot.buttons.inline_buttons import language_buttons
from bot.buttons.reply_buttons import main_menu_buttons
from bot.buttons.text import back_main_menu, back_main_menu_ru, choice_language, choice_language_ru, no
from bot.dispatcher import dp, bot
from main import admins
from geopy import Nominatim

geolocator = Nominatim(user_agent="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")


@dp.message_handler(Text(equals=[back_main_menu, back_main_menu_ru]),
                    state=['sell', 'buy', 'offer', 'complaint', 'business_card', 'directory'])
async def back_main_menu_function_1(msg: types.Message, state: FSMContext):
    if msg.text == back_main_menu:
        await msg.answer(text=f"Asosiy menu🏠", reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer(text=f"Главное меню🏠", reply_markup=await main_menu_buttons(msg.from_user.id))
    await state.finish()


@dp.message_handler(Text(no))
async def back_main_menu_function(msg: types.Message):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/telegram-users/chat_id/{msg.from_user.id}/").content)
    if tg_user['language'] == 'uz':
        await msg.answer(text=f"Asosiy menu🏠", reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer(text=f"Главное меню🏠", reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.message_handler(Text(equals=[back_main_menu, back_main_menu_ru]))
async def back_admin_to_main_menu_function(msg: types.Message):
    await msg.answer(text=f"""
/start buyrug'ini yuboring ❗

----------------------------

Отправьте команду /start ❗""", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(CommandStart())
async def start_handler(msg: types.Message, state: FSMContext):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/telegram-users/chat_id/{msg.from_user.id}/").content)
    try:
        if tg_user['detail']:
            await state.set_state('language_1')
            await msg.answer(text="""
Tilni tanlang

-------------

Выберите язык""", reply_markup=await language_buttons())
            data = {
                "chat_id": str(msg.from_user.id),
                "username": msg.from_user.username,
                "full_name": msg.from_user.full_name,
                "language": 'uz'
            }
            requests.post(url=f"http://127.0.0.1:8000/telegram-users/create/", data=data)
    except KeyError:
        if tg_user.get('language') == 'uz':
            await msg.answer(text=f"Bot yangilandi ♻", reply_markup=await main_menu_buttons(msg.from_user.id))
        else:
            await msg.answer(text=f"Бот обновлен ♻", reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.callback_query_handler(Text(startswith='language_'), state='language_1')
async def language_function(call: types.CallbackQuery, state: FSMContext):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/telegram-users/chat_id/{call.from_user.id}/").content)
    data = {
        "chat_id": str(call.from_user.id),
        "username": call.from_user.username,
        "full_name": call.from_user.full_name,
        "language": call.data.split("_")[-1]
    }
    requests.put(url=f"http://127.0.0.1:8000/telegram-users/update/{tg_user['id']}/", data=data)
    await call.message.delete()
    await state.set_state('register_1')
    if call.data.split("_")[-1] == 'uz':
        await call.message.answer(text=f"Ism-Familiyangizni kiriting ✍️:")
    else:
        await call.message.answer(text=f"Введите свое имя и фамилию ✍️:")


@dp.message_handler(state='register_1')
async def register_function(msg: types.Message, state: FSMContext):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/telegram-users/chat_id/{msg.from_user.id}/").content)
    async with state.proxy() as data:
        data['full_name'] = msg.text
    k = KeyboardButton(text="TELEFON RAQAM📲", request_contact=True)
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb_client.add(k)
    await state.set_state("register_2")
    if tg_user.get('language') == 'uz':
        await msg.answer(text="Tugma orqali telefon raqamingizni yuboring 👇", reply_markup=kb_client)
    else:
        await msg.answer(text="Укажите свой номер телефона через кнопку 👇", reply_markup=kb_client)


@dp.message_handler(state='register_2', content_types=types.ContentTypes.CONTACT)
async def register_function_4(msg: types.Message, state: FSMContext):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/telegram-users/chat_id/{msg.from_user.id}/").content)
    async with state.proxy() as data:
        for admin in admins:
            await bot.send_message(chat_id=admin, text=f"""
Yangi user🆕
ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Username: @{msg.from_user.username}
Ism-Familiya: {data['full_name']}
Telefon raqam: {msg.contact.phone_number}""", parse_mode='HTML')
        data = {
            "chat_id": str(msg.from_user.id),
            "username": msg.from_user.username,
            "full_name": data['full_name'],
            "phone_number": msg.contact.phone_number,
        }
        requests.put(url=f"http://127.0.0.1:8000/telegram-users/update/{tg_user['id']}/", data=data)
    if tg_user.get('language') == 'uz':
        await msg.answer(text="Ro'yhatdan o'tdingiz ✅", reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer(text="Вы зарегистрированы ✅", reply_markup=await main_menu_buttons(msg.from_user.id))
    await state.finish()


@dp.message_handler(Text(equals=[choice_language, choice_language_ru]))
async def change_language_function_1(msg: types.Message):
    if msg.text == choice_language:
        await msg.answer(text="Tilni tanlang", reply_markup=await language_buttons())
    else:
        await msg.answer(text="Выберите язык", reply_markup=await language_buttons())


@dp.callback_query_handler(Text(startswith='language_'))
async def language_function_1(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/telegram-users/chat_id/{call.from_user.id}/").content)
    data = {
        "chat_id": str(call.from_user.id),
        "username": call.from_user.username,
        "full_name": call.from_user.full_name,
        "language": call.data.split("_")[-1]
    }
    requests.put(url=f"http://127.0.0.1:8000/telegram-users/update/{tg_user['id']}/", data=data)
    await call.message.delete()
    if call.data.split("_")[-1] == 'uz':
        await call.message.answer(text="Til o'zgartirildi 🇺🇿", reply_markup=await main_menu_buttons(call.from_user.id))
    else:
        await call.message.answer(text="Язык изменен 🇷🇺", reply_markup=await main_menu_buttons(call.from_user.id))
