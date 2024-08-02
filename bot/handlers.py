import requests
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

API_URL = "http://web/api/v1/msg/"


# API_URL = "http://127.0.0.1:8000/api/v1/msg/"


class State_(StatesGroup):
    wait_for_message = State()  # Переименуйте для ясности


router = Router()


# Приветствие
@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply("Welcome!\n"
                        "Use /messages to get messages,\n"
                        "/create to create a message.")


# Получение всех сообщений
@router.message(Command("messages"))
async def get_messages(message: Message):
    response = requests.get(API_URL)
    if response:
        messages = response.json()
        await message.reply("\n".join([f"{msg['content']}" for msg in messages]))
    else:
        await message.reply("Сервис недоступен, попробуйте позже")


# Создание сообщения
@router.message(Command("create"))
async def create_message(message: Message, state: FSMContext):
    await message.reply("Please write your message.")
    await state.set_state(State_.wait_for_message)


@router.message(State_.wait_for_message)
async def add(msg: Message, state: FSMContext):
    data = msg.text
    response = requests.post(API_URL, json={"content": data})
    if response:
        await msg.reply("Message sent to the API.")
        await state.clear()
    else:
        await msg.reply("Сервис недоступен, попробуйте позже")
        await state.clear()


# Ответ на любое полученное сообщение от пользователя
@router.message()
async def any_msg(message: Message):
    await send_welcome(message)
