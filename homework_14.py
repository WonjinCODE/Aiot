import cv2  # OpenCV 라이브러리 임포트
from gpiozero import Buzzer
import time

buzzerPin = Buzzer(16)  # 부저 핀 설정              

def main():
    camera = cv2.VideoCapture(-1)  # 카메라 초기화
    camera.set(3,640)  # 너비 설정
    camera.set(4,480)  # 높이 설정
    
    face_xml = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'  # 얼굴 검출 모델 경로
    eye_xml = cv2.data.haarcascades + 'haarcascade_eye.xml'  # 눈 검출 모델 경로
    face_cascade = cv2.CascadeClassifier(face_xml)  # 얼굴 검출 모델 로드
    eye_cascade = cv2.CascadeClassifier(eye_xml)  # 눈 검출 모델 로드
    
    while( camera.isOpened() ):  # 카메라가 열려있는 동안 반복
        _, image = camera.read()  # 카메라에서 이미지 읽기
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 이미지를 흑백으로 변환
        
        faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(100,100),flags=cv2.CASCADE_SCALE_IMAGE)  # 얼굴 검출
        print("faces detected Number: " + str(len(faces)))  # 검출된 얼굴 수 출력
    camera = cv2.VideoCapture(-1)   # 카메라 초기화
    camera.set(3,640)   # 너비 설정
    camera.set(4,480)   # 높이 설정
    
    face_xml = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'   # 얼굴 검출 모델 경로
    eye_xml = cv2.data.haarcascades + 'haarcascade_eye.xml'   # 눈 검출 모델 경로
    face_cascade = cv2.CascadeClassifier(face_xml)   # 얼굴 검출 모델 로드
    eye_cascade = cv2.CascadeClassifier(eye_xml)   # 눈 검출 모델 로드
    
    while( camera.isOpened() ):   # 카메라가 열려있는 동안 반복
        _, image = camera.read()   # 카메라에서 이미지 읽기
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)   # 이미지를 흑백으로 변환

        faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(100,100),flags=cv2.CASCADE_SCALE_IMAGE)   # 얼굴 검출    
        print("faces detected Number: " + str(len(faces)))   # 검출된 얼굴 수 출력

        if len(faces):
            for (x,y,w,h) in faces:
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)   # 얼굴 윤곽선 그리기
                
                face_gray = gray[y:y+h, x:x+w]   # 얼굴 영역을 흑백으로 변환
                face_color = image[y:y+h, x:x+w]   # 얼굴 영역을 컬러로 변환
                
                eyes = eye_cascade.detectMultiScale(face_gray,scaleFactor=1.1,minNeighbors=5)   # 눈 검출
                
                if len(eyes) <= 1:   # 눈이 1개 이하인 경우
                    buzzerPin.on()   # 부저 켜기
                    buzzerPin.on()
                else:   # 눈이 2개 이상인 경우
                    buzzerPin.off()   # 부저 끄기
                    buzzerPin.off()
                
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(face_color, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)   # 눈 윤곽선 그리기
        
        cv2.imshow('result', image)   # 결과 이미지 표시
        
        if cv2.waitKey(1) == ord('q'):
            break   # 'q' 키를 누르면 종료
    
    cv2.destroyAllWindows()   # 모든 창 닫기
    buzzerPin.off()   # 부저 끄기   

if __name__ == '__main__':
    main()   # 메인 함수 실행
