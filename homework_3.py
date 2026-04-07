from gpiozero import MotionSensor   #GPIO 라이브러리 임포트
import time
from picamera2 import Picamera2   #카메라 라이브러리 임포트
import datetime   #시간 라이브러리 임포트

pirPin = MotionSensor(16)   #PIR 센서 핀 번호 16번

picam2 = Picamera2()   #카메라 객체 생성
camera_config = picam2.create_preview_configuration()   #카메라 설정
picam2.configure(camera_config)   #카메라 설정
picam2.start()   #카메라 시작

try:   #예외 처리
    while True:
        try:   #예외 처리
            sensorValue = pirPin.value
            if sensorValue == 1:   #PIR 센서 값이 1일 때
                now = datetime.datetime.now()
                print(now)   #현재 시간 출력
                fileName = now.strftime('%Y-%m-%d %H:%M:%S')   #현재 시간 파일 이름으로 저장
                picam2.capture_file(fileName + '.jpg')
                time.sleep(0.5)   #0.5초 대기
        except:   #예외 처리 
            pass

except KeyboardInterrupt:   #키보드 인터럽트 처리
    pass   #프로그램 종료
