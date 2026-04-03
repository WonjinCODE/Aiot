from gpiozero import Buzzer, DigitalInputDevice
import time  #프로그램의 실행을 잠시 멈추는(Delay) sleep() 함수를 사용하기 위해 가져옵니다.

bz = Buzzer(18)     #18번 핀에 부저 연결
gas = DigitalInputDevice(17) #17번 핀에 가스 센서 연결

try:
    while True:    #무한 반복
        if gas.value == 0:    # 0 = 가스 감지 (LOW)
            print("가스 감지됨")
            bz.on()    #부저 켜기
        else:                 # 1 = 정상 (HIGH)
            print("정상")
            bz.off()    #부저 끄기

        time.sleep(0.2)    #0.2초 대기

except KeyboardInterrupt:
    pass    #Ctrl+C 입력 시 예외 처리

bz.off()    #부저 끄기
