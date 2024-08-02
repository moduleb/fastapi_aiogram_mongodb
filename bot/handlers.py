import logging

import requests
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

API_URL = "http://web/api/v1/messages/"
# API_URL = "http://localhost/api/v1/messages/"

class State_(StatesGroup):
    wait_for_message = State()


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
        await message.reply("Service is not available, try again later")
        logging.error("Нет ответа от {}".format(API_URL))


# Создание сообщения
@router.message(Command("create"))
async def create_message(message: Message, state: FSMContext):
    await message.reply("Please write your message.")
    await state.set_state(State_.wait_for_message)


@router.message(State_.wait_for_message)
async def add(msg: Message, state: FSMContext):
    data = msg.text
    response = requests.post(API_URL, json={"content": data,
                                            "username":str(msg.from_user.username)})
    await state.clear()
    if response:
        await msg.reply("Message sent to the API.")
    else:
        await msg.reply("Service is not available, try again later")
        logging.error("Нет ответа от {}".format(API_URL))


# Ответ на любое полученное сообщение от пользователя
@router.message()
async def any_msg(message: Message):
    await send_welcome(message)
