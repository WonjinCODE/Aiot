import speech_recognition as sr # 음성 인식 모듈 임포트
import requests # 웹 요청 모듈 임포트  
import re # 정규 표현식 모듈 임포트
import os # 운영 체제 모듈 임포트
import time # 시간 모듈 임포트

url = "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4139054000" # 기상청 날씨 정보 주소 

def speak(option, msg) :    # espeak 명령어를 사용하여 음성 출력
    os.system("espeak {} '{}'".format(option,msg))

try:
    while True :    # 무한 루프
        r = sr.Recognizer()    # 음성 인식 객체 생성
        
        with sr.Microphone() as source:    # 마이크 객체 생성
            print("Say something!")    # 음성 인식 대기
            audio = r.listen(source)    # 음성 인식
            
        try:
            text = r.recognize_google(audio, language='ko-KR')    # 음성 인식 결과
            print("You said: " + text)    # 음성 인식 결과 출력         
            if text in "날씨":    # 날씨 음성을 인식하였다면
                print("날씨 음성을 인식하였습니다.")
                response = requests.get(url)    # 웹 요청 결과
                temp = re.findall(r'<temp>(.+)</temp>',response.text)    # 기온 정보 추출
                humi = re.findall(r'<reh>(.+)</reh>',response.text)    # 습도 정보 추출
                
                msg = '    기온은 ' + temp[0].split('.')[0] + '도 습도는 ' + humi[0] + '퍼센트 입니다'    # 날씨 정보 메시지
                
                option = '-s 180 -p 50 -a 200 -v ko+f5'    # espeak 명령어 옵션
                speak(option,msg)    # 음성 출력
            
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")    # 음성 인식 불가 오류 출력
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))    # 음성 인식 요청 오류 출력

except KeyboardInterrupt:    # 키보드 인터럽트 오류 처리    
    pass    # 키보드 인터럽트 오류 처리
    print("프로그램을 종료합니다.")    # 프로그램 종료 메시지 출력

