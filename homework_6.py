import urllib.request   #urlopen()을 사용하기 위해 임포트                   
import json
import datetime
import asyncio
import telegram #telegram bot API를 사용하기 위해 임포  telegram.Bot()을 사용하기 위해 임포트
from telegram import Bot #telegram.Bot()을 사용하기 위해 임포트

telegram_id = 'Enter your chat ID here' #telegram bot API를 사용하기 위해 임포트
my_token = 'Enter your bot token here' #telegram bot API를 사용하기 위해 임포트
api_key = 'Enter your API key here' #telegram bot API를 사용하기 위해 임포트

bot = Bot(token=my_token)

ALERT_HOURS = [7, 10, 13, 16, 19, 22]                                     # Hourly alerts every 3 hours #알림 시간 설정
ALERT_TIMES = ["08:30", "15:20"]                                          # Custom time alerts (add your times here) #알림 시간 설정

def getWeather():       
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8" #OpenWeatherMap API를 사용하기 위해 임포트

    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read()) #OpenWeatherMap API를 사용하기 위해 임포트       #json.loads()를 사용하기 위해 임포트

    text = "" #text를 사용하기 위해 임포트
    for i in range(8):
        item = data['list'][i] #item를 사용하기 위해 임포트
        hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2)
        temp = item['main']['temp'] #temp를 사용하기 위해 임포트
        humi = item['main']['humidity'] #humi를 사용하기 위해 임포트
        desc = item['weather'][0]['description'] #desc를 사용하기 위해 임포트
        text += f"({hour}h {temp}C {humi}% {desc})\n"   #text를 사용하기 위해 임포트

    return text #text를 사용하기 위해 임포트

async def main(): #main을 사용하기 위해 임포트              
    try:
        while True:
            now = datetime.datetime.now() #now를 사용하기 위해 임포트
            hm = now.strftime('%H:%M')                                     # Current time as HH:MM (e.g. "08:30") #현재 시간 설정

            is_alert_hour = now.hour in ALERT_HOURS and now.minute == 0 and now.second == 0   # Check scheduled hour alert #알림 시간 설정
            is_alert_time = hm in ALERT_TIMES and now.second == 0                             # Check custom time alert #알림 시간 설정

            if is_alert_hour or is_alert_time:
                msg = getWeather() #getWeather()를 사용하기 위해 임포트
                print(msg) #msg를 사용하기 위해 임포트
                await bot.send_message(chat_id=telegram_id, text=msg) #bot.send_message()를 사용하기 위해 임포트        

            await asyncio.sleep(1) #asyncio.sleep()를 사용하기 위해 임포트

    except KeyboardInterrupt:
        pass #KeyboardInterrupt를 사용하기 위해 임포트      #키보드 인터럽트 처리

asyncio.run(main()) #asyncio.run()를 사용하기 위해 임포트       #비동기 실행
