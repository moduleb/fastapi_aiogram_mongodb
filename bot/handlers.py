import logging

import requests
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

API_URL = "http://web/api/v1/messages/"

class State_(StatesGroup):
    wait_for_message = State()


router = Router()

@router.message(Command("start"))
async def send_welcome(message: Message):
    """Приветствие"""
    await message.reply("Welcome!\n"
                        "You can use /messages to view messages,\n"
                        "and /create to add a new message.")


@router.message(Command("messages"))
async def get_messages(message: Message):
    """Получение всех сообщений"""
    response = requests.get(API_URL)
    if response:
        messages = response.json()
        for msg in messages:
            await message.reply(
                "\n".join(f"{key}: {value}" for key, value in msg.items())
            )
    else:
        await message.reply("Service unavailable. Please try again later.")
        logging.error("No response from {}".format(API_URL))


@router.message(Command("create"))
async def create_message(message: Message, state: FSMContext):
    """Создание сообщения"""
    await message.reply("Please enter your message")
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
        await msg.reply("Service unavailable. Please try again later.")
        logging.error("No response from {}".format(API_URL))


@router.message()
async def any_msg(message: Message):
    """Ответ на любое полученное сообщение от пользователя"""
    await send_welcome(message)
