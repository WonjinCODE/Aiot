from flask import Flask, request, render_template #flask 라이브러리 임포트 
from gpiozero import LED #gpiozero 라이브러리 임포트

app = Flask(__name__)

red_led = LED(21)   #LED 객체 생성

@app.route('/') #루트 경로 설정
def home():
   return render_template("index.html")

@app.route('/data', methods = ['POST']) #data 경로 설정
def data():
    data = request.form['led'] #data 값 가져오기
    
    if(data == 'on'): #data 값이 on일 때 LED 켜기       
        red_led.on() #LED 켜기      
        return home() #home 페이지로 이동

    elif(data == 'off'): #data 값이 off일 때 LED 끄기
        red_led.off() #LED 끄기
        return home() #home 페이지로 이동

if __name__ == '__main__': #main 함수 설정
   app.run(host = '0.0.0.0', port = '80') #app 실행 80번 포트로 실행
