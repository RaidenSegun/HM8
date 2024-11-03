import asyncio 
import logging
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from bs4 import BeautifulSoup
import requests

from config import token

bot = Bot(token=token)

dp = Dispatcher()

conn = sqlite3.connect("user_requests.db")
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        request_text TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

@dp.message(CommandStart()) 
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.full_name}, хотите узнать курс валюты?") 
    await message.answer("Выберите:", reply_markup=start_keyboard1)
start_buttons1 = [
    [KeyboardButton(text="Да, хочу узнать"), KeyboardButton(text="Нет, мне это не нужно пока")],
]
start_keyboard1 = ReplyKeyboardMarkup(keyboard=start_buttons1, resize_keyboard=True)

@dp.message(F.text == "Да, хочу узнать")
async def parsing_comm(message: types.Message):
    global user_id 
    user_id = message.from_user.id 
    response = requests.get(url="https://www.nbkr.kg/index.jsp?lang=RUS")
    soup = BeautifulSoup(response.text, "lxml")

    # rub = soup.find_all("div", class_="col-md-4 col-sm-12 curval")

    # for name in zip(rub):
    #     text = name[0].text
    #     await message.answer(f"Курс валюты: {text}")
    
    doll = soup.find_all("div", class_="exchange-rates-body")

    for name in zip(doll):
        text = name[0].text
        await message.answer(f"Курс валюты: {text}")

    # euro = soup.find_all("div", class_="col-md-4 col-sm-12 curval")

    # for name in zip(euro):
    #     text = name[0].text
    #     await message.answer(f"Курс валюты: {text}")
    
    # cny = soup.find_all("div", class_="col-md-4 col-sm-12 curval")

    # for name in zip(cny):
    #     text = name[0].text
    #     await message.answer(f"Курс валюты: {text}")
        



    save_request(user_id, text)

@dp.message(F.text == "Да, хочу узнать")
def save_request(user_id, request_text):
    conn = sqlite3.connect("user_requests.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requests (user_id, request_text) VALUES (?, ?)
    ''', (user_id, request_text))
    
    
    conn.commit()
    conn.close()


@dp.message(F.text == "Нет, мне это не нужно пока") 
async def backend(message: Message):
    await message.answer("Ваш запрос принят")


@dp.message()
async def echo(message: types.Message):
    await message.answer("Я вас не понял")


async def main():
    logging.basicConfig(level="INFO")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
