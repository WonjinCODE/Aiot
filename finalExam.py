import cv2  # 카메라 영상 처리
import time
import datetime
import requests  # 텔레그램 메시지 전송

# =========================
# 텔레그램 설정
# =========================
TELEGRAM_BOT_TOKEN = "Enter your bot token here"  # 텔레그램 봇 토큰
TELEGRAM_CHAT_ID = "Enter your chat ID here"  # 텔레그램 채팅 ID

# =========================
# 서비스 설정
# =========================
ABSENCE_SECONDS = 5  # 이탈 감지 시간(원활한 실험을 위해 5초로 설정)
SEND_RETURN_MESSAGE = True
SHOW_CAMERA_WINDOW = True  # 카메라 영상 표시 여부


def send_telegram_message(message):  # 텔레그램 메시지 전송 함수   
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"  # 텔레그램 메시지 전송 URL

    data = {
        "chat_id": TELEGRAM_CHAT_ID,  # 텔레그램 채팅 ID
        "text": message  # 텔레그램 메시지 내용
    }

    try:
        response = requests.post(url, data=data, timeout=5)  # 텔레그램 메시지 전송 요청

        if response.status_code == 200:
            print("텔레그램 알림 전송 성공")
        else:
            print("텔레그램 알림 전송 실패:", response.text)

    except Exception as e:
        print("텔레그램 전송 오류:", e)


def main():
    face_xml = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"  # 얼굴 감지 모델 경로
    face_cascade = cv2.CascadeClassifier(face_xml)  # 얼굴 감지 모델 로드

    if face_cascade.empty():
        print("얼굴 감지 모델을 불러오지 못했습니다.")
        return

    camera = cv2.VideoCapture(0)  # 카메라 열기

    if not camera.isOpened():
        print("웹캠을 열 수 없습니다.")
        print("cv2.VideoCapture(0)의 숫자를 1 또는 -1로 바꿔보세요.")
        return

    camera.set(3, 640)  # 카메라 가로 해상도 설정
    camera.set(4, 480)  # 카메라 세로 해상도 설정

    last_seen_time = time.time()  # 마지막 감지 시간    
    is_absent = False  # 이탈 상태 변수

    print("치매 어르신 실내 이탈 감지 알림 서비스 시작")
    print(f"{ABSENCE_SECONDS}초 이상 사람이 감지되지 않으면 텔레그램 알림을 전송합니다.")
    print("종료하려면 q 키를 누르세요.")

    try:
        while True:
            ret, frame = camera.read()  # 카메라 프레임 읽기

            if not ret:
                print("카메라 프레임을 읽지 못했습니다.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 카메라 프레임 흑백 변환

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,  # 얼굴 감지 모델 스케일 팩터
                minNeighbors=5,
                minSize=(100, 100)  # 얼굴 감지 모델 최소 크기
            )

            now = time.time()
            person_detected = len(faces) > 0  # 사람 감지 여부

            for (x, y, w, h) in faces:
                cv2.rectangle(  # 얼굴 감지 모델 결과 출력
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

            if person_detected:
                last_seen_time = now
                status_text = "DETECTED"  # 사람 감지 상태 텍스트

                if is_absent:
                    is_absent = False
                    return_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 사람 감지 시간
                    print("사람이 다시 감지되었습니다.")

                    if SEND_RETURN_MESSAGE:
                        send_telegram_message(  # 텔레그램 메시지 전송
                            "[복귀 감지 알림]\n"
                            "실내에서 사람이 다시 감지되었습니다.\n"
                            f"감지 시간: {return_time}"  # 사람 감지 시간
                        )

            else:
                absence_time = now - last_seen_time  # 사람 감지 시간

                if absence_time >= ABSENCE_SECONDS:
                    status_text = "NOT DETECTED"  # 사람 감지 상태 텍스트

                    if not is_absent:
                        is_absent = True
                        alert_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 사람 감지 시간

                        message = (  # 텔레그램 메시지 내용
                            "[실내 이탈 의심 알림]\n"
                            f"{ABSENCE_SECONDS}초 이상 사람이 감지되지 않았습니다.\n"
                            "보호자의 확인이 필요합니다.\n"
                            f"감지 시간: {alert_time}"  # 사람 감지 시간
                        )

                        print(message)  # 텔레그램 메시지 내용 출력
                        send_telegram_message(message)

                else:
                    status_text = f"CHECKING... {int(absence_time)}s"  # 사람 감지 상태 텍스트

            cv2.putText(  # 카메라 프레임 텍스트 출력
                frame,
                status_text,  # 사람 감지 상태 텍스트
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,  # 텍스트 폰트
                1,
                (0, 0, 255),  # 텍스트 색상
                2
            )

            if SHOW_CAMERA_WINDOW:
                cv2.imshow("Indoor Absence Alert Service", frame)  # 카메라 프레임 출력

                if cv2.waitKey(1) == ord("q"):
                    break  # 프로그램 종료

            else:
                time.sleep(0.1)  # 0.1초 대기

    except KeyboardInterrupt:
        print("프로그램 종료")

    finally:
        camera.release()  # 카메라 해제
        cv2.destroyAllWindows()  # 창 닫기  


if __name__ == "__main__":
    main()  # 프로그램 실행
