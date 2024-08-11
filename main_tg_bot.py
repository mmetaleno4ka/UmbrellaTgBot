import asyncio
import logging
import sys
import requests
from pprint import pprint
import datetime

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from dotenv import load_dotenv
import os

load_dotenv('config.env')

bot_token = os.getenv('BOT_TOKEN')
weather_token = os.getenv('WEATHER_TOKEN')

# Ініціалізація диспетчера та бота
dp = Dispatcher()
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Вітаємо, {html.bold(message.from_user.full_name)}!")
    await message.answer(
        f"Раді що ви вирішили скористатись 'Umbrella'!  Цей бот може допомогти дізнатись чи потрібна Вам сьогодні парасолька.\n"
        f"{html.bold('Яке місто Вас цікавить?')}"
    )

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        city_name = data["name"]
        humidity = data["main"]["humidity"]
        sky_condition = data["weather"][0]["main"]
        pressure = data["main"]["grnd_level"]

        if pressure < 1000:
            rain_chance = "Висока ймовірність дощу або грози  \U0001F327"
        elif 1000 <= pressure < 1010:
            rain_chance = "Помірна ймовірність дощу  \u2601"
        else:
            rain_chance = "Малоймовірно, що буде дощ  \u2600"

        return f"●○●○ На {datetime.datetime.now().strftime('%H:%M %d.%m.%Y')} ○●○●\n"\
               f"Вся інформація про місто {city_name}:\nВологість: {humidity}\n"\
               f"{rain_chance}\n"\
               f"Тиск: {pressure}\n"
    else:
        return "Неможливо знайти місто :("

# Обробник повідомлень для отримання погоди
@dp.message()
async def weather_info_handler(message: Message) -> None:
    city = message.text
    weather = get_weather(city)
    await message.answer(html.bold(weather))

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())