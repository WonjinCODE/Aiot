import paho.mqtt.client as mqtt #paho는 MQTT 프로토콜을 사용하기 위한 파이썬 라이브러리 
import time
from gpiozero import LED #gpiozero는 GPIO 핀을 사용하기 위한 파이썬 라이브러리 선언

greenLed = LED(16) #GPIO 16번 핀을 사용하여 그린 LED 선언
blueLed = LED(20) #GPIO 20번 핀을 사용하여 블루 LED 선언
redLed = LED(21) #GPIO 21번 핀을 사용하여 레드 LED 선언

def on_message(client, userdata, msg): #MQTT 메시지를 수신할 때 호출되는 함수
    print(msg.topic+" "+str(msg.payload)) #MQTT 메시지의 토픽과 페이로드를 출력
    message = msg.payload.decode()
    print(message) #MQTT 메시지의 페이로드를 디코드하여 출력
    if message == "green_on": #MQTT 메시지의 페이로드가 green_on일 때 그린 LED 켜기
        greenLed.on()
    elif message == "green_off": #MQTT 메시지의 페이로드가 green_off일 때 그린 LED 끄기
        greenLed.off()
    elif message == "blue_on": #MQTT 메시지의 페이로드가 blue_on일 때 블루 LED 켜기
        blueLed.on()
    elif message == "blue_off": #MQTT 메시지의 페이로드가 blue_off일 때 블루 LED 끄기
        blueLed.off()
    elif message == "red_on": #MQTT 메시지의 페이로드가 red_on일 때 레드 LED 켜기       
        redLed.on()
    elif message == "red_off": #MQTT 메시지의 페이로드가 red_off일 때 레드 LED 끄기
        redLed.off()

client = mqtt.Client() #MQTT 클라이언트 생성
client.on_message = on_message #MQTT 메시지를 수신할 때 호출되는 함수 설정

broker_address="192.168.137.230" #MQTT 브로커 주소
client.connect(broker_address) #MQTT 브로커에 연결
client.subscribe("led",1) #MQTT 브로커에서 led 토픽을 구독하여 메시지를 수신

client.loop_forever() #MQTT 브로커에서 메시지를 수신하기 위한 루프 실행
