import os
import asyncio
import requests
import datetime
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from main import get_weather

load_dotenv()
dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer('Привет, крипочек! Напиши мне название города и я пришлю сводку погоды!')


@dp.message()
async def get_weather1(message: types.Message):
        
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={os.getenv('WEATHER_TOKEN')}&units=metric"
    )
        data = r.json()


        city = data['name']
        cur_weather = data['main']['temp']
        weather_discription = data['weather'][0]['main']
        if weather_discription in code_to_smile:
            wd = code_to_smile[weather_discription]
        else:
            wd = 'Посмотри в окно, не пойму что там за погода!'
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        lenth_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])
        
        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}С° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {lenth_of_the_day}\n"
              f"***Хорошего дня, а Дима скуф !***"
              )
    except:
        await message.reply('\U00002620 Проверьте название города \U00002620')
    


async def main():
    bot = Bot(token=os.getenv('TG_TOKEN'))
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())