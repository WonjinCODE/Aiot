from gpiozero import LEDBoard
from time import sleep

leds = LEDBoard(2,3,4,20,21)

try:        # try를 사용하여 프로그램 실행중 발생할 수 있는 오류나 중단 신호를 안전하게 처리.
    while 1:        #  while True와 동실한 의미이고, 프로그램이 강제로 종료될 때까지 내부의 코드를 무한히 반복.
        leds.value = (0,0,1,1,0)    # 5개의 LED 상태를 튜플로 한 번에 설정하였고 0은 꺼짐(OFF)를 의미.
        sleep(3.0)
        leds.value = (0,1,0,1,0)
        sleep(1.0)
        leds.value = (1,0,0,0,1)
        sleep(3.0)
    
except KeyboardInterrupt:   # 사용자가 Ctrl + c를 눌러 프로그램을 강제 종료하려고 할 때 발생하는 신호를 잡아내고
                            # 에러메세지를 띄우며 비정상 종료되는 것을 막고 pass를 통해 다음 줄로 부드럽게 넘어감
    pass

leds.off() # 프로그램이 종료되기 직전, 켜져 있던 모든 LED를 끄는 명렁어이다. 없으면 프로그램이 종료되도 LED가 예속 켜져있음.
