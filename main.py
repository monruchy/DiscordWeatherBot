import discord
import asyncio
import requests
from discord.ext import commands
from datetime import datetime  # เพิ่มการนำเข้า datetime

DISCORD_TOKEN = ''
WEATHER_API_KEY = ''
CHANNEL_ID =   

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def get_weather():
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q=Saraburi,TH&units=metric&appid={WEATHER_API_KEY}"
    forecast_url = f"http://api.openweathermap.org/data/2.5/onecall?lat=14.5289&lon=100.9100&exclude=minutely,hourly,alerts&units=metric&appid={WEATHER_API_KEY}"
    air_quality_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat=14.5289&lon=100.9100&appid={WEATHER_API_KEY}"

    
    weather_response = requests.get(weather_url)
    forecast_response = requests.get(forecast_url)
    air_quality_response = requests.get(air_quality_url)

   
    weather_data = weather_response.json() if weather_response.status_code == 200 else None
    forecast_data = forecast_response.json() if forecast_response.status_code == 200 else None
    air_quality_data = air_quality_response.json() if air_quality_response.status_code == 200 else None

    
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    embed = discord.Embed(
        title="🌤️ สภาพอากาศในจังหวัดสระบุรี",
        description=f"ข้อมูล ณ วันที่ {current_time}",
        color=0x1E90FF  
    )

    if weather_data:
        weather = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        wind_deg = weather_data['wind']['deg']
        pressure = weather_data['main']['pressure']
        sunrise = weather_data['sys']['sunrise']
        sunset = weather_data['sys']['sunset']

        sunrise_time = datetime.fromtimestamp(sunrise).strftime('%H:%M:%S')
        sunset_time = datetime.fromtimestamp(sunset).strftime('%H:%M:%S')

        embed.add_field(name="🌡️ อุณหภูมิ", value=f"{temp}°C", inline=True)
        embed.add_field(name="💧 ความชื้น", value=f"{humidity}%", inline=True)
        embed.add_field(name="🌬️ ความเร็วลม", value=f"{wind_speed} m/s", inline=True)
        embed.add_field(name="🧭 ทิศทางลม", value=f"{wind_deg}°", inline=True)
        embed.add_field(name="📊 ความกดอากาศ", value=f"{pressure} hPa", inline=True)
        embed.add_field(name="🌅 พระอาทิตย์ขึ้น", value=sunrise_time, inline=True)
        embed.add_field(name="🌇 พระอาทิตย์ตก", value=sunset_time, inline=True)
    else:
        embed.add_field(name="🌡️ สภาพอากาศ", value="Error", inline=True)

    if forecast_data:
        tomorrow = forecast_data['daily'][1]
        forecast_temp_day = tomorrow['temp']['day']
        forecast_temp_night = tomorrow['temp']['night']
        forecast_weather = tomorrow['weather'][0]['description']

        embed.add_field(
            name="📅 พยากรณ์อากาศวันพรุ่งนี้",
            value=(
                f"- สภาพอากาศ: {forecast_weather}\n"
                f"- อุณหภูมิกลางวัน: {forecast_temp_day}°C\n"
                f"- อุณหภูมิกลางคืน: {forecast_temp_night}°C"
            ),
            inline=False
        )
    else:
        embed.add_field(name="📅 พยากรณ์อากาศวันพรุ่งนี้", value="Error", inline=False)

    if air_quality_data:
        pm2_5 = air_quality_data['list'][0]['components']['pm2_5']
        pm10 = air_quality_data['list'][0]['components']['pm10']

        embed.add_field(name="🌫️ ค่าฝุ่น PM2.5", value=f"{pm2_5} µg/m³", inline=True)
        embed.add_field(name="🌫️ ค่าฝุ่น PM10", value=f"{pm10} µg/m³", inline=True)
    else:
        embed.add_field(name="🌫️ ค่าฝุ่น PM2.5", value="Error", inline=True)
        embed.add_field(name="🌫️ ค่าฝุ่น PM10", value="Error", inline=True)

    embed.set_footer(text="ข้อมูลจาก OpenWeatherMap")
    return embed

async def weather_update():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    message = None 
    while not bot.is_closed():
        weather_info = get_weather()
        if isinstance(weather_info, discord.Embed):  
            if message is None:
                message = await channel.send(embed=weather_info)
            else:
                await message.edit(embed=weather_info)
        else:
            if message is None:
                message = await channel.send(weather_info)
            else:
                await message.edit(content=weather_info)
        await asyncio.sleep(300)  #(300 วินาที)

class WeatherBot(commands.Bot):
    async def setup_hook(self):
        self.loop.create_task(weather_update())

bot = WeatherBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

bot.run(DISCORD_TOKEN)