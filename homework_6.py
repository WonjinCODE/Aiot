import urllib.request, json, tkinter, tkinter.font #, time
 
API_KEY = "Enter your API key here" #https://home.openweathermap.org/api_keys API키는 실험을 할 때 넣어서 사용하였습니다.
 
def tick1Min(): #1분마다 날씨 정보를 가져와서 라벨에 표시하는 함수입니다.
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric" #서울의 날씨 정보를 가져오는 URL입니다. API_KEY를 넣어서 사용하시면 됩니다.
    with urllib.request.urlopen(url) as r:  #URL을 열어서 데이터를 가져옵니다.
        data = json.loads(r.read()) #가져온 데이터를 JSON 형식으로 파싱합니다.
    temp = data["main"]["temp"] #온도 정보를 가져옵니다.
    humi = data["main"]["humidity"] #습도 정보를 가져옵니다.
    label.config(text=f"{temp:.1f}C   {humi}%") #라벨에 온도와 습도를 표시합니다. 온도는 소수점 한 자리까지 표시합니다.
    window.after(60000, tick1Min)   #60000밀리초(1분) 후에 tick1Min 함수를 다시 호출하여 정보를 업데이트합니다.
 
window = tkinter.Tk()   #Tkinter 창을 생성합니다.
window.title("TEMP HUMI DISPLAY")   #창의 제목을 설정합니다.
window.geometry("400x100")  #창의 크기를 설정합니다. 너비 400픽셀, 높이 100픽셀로 설정하였습니다.
window.resizable(False, False)  #창의 크기를 고정합니다. 사용자가 창의 크기를 변경할 수 없도록 설정합니다.
font = tkinter.font.Font(size=30)   #글꼴의 크기를 설정합니다. 글꼴의 크기를 30으로 설정하였습니다.
label = tkinter.Label(window, text="", font=font)   #라벨을 생성합니다. 라벨은 창에 텍스트를 표시하는 위젯입니다. 초기 텍스트는 빈 문자열로 설정하고, 글꼴은 앞에서 설정한 font로 지정합니다.
label.pack()    #라벨을 창에 배치합니다. pack() 메서드는 라벨을 창에 추가하고, 자동으로 위치를 조정합니다.
tick1Min()  #tick1Min 함수를 호출하여 처음으로 날씨 정보를 가져와서 라벨에 표시합니다. 이후에는 tick1Min 함수가 1분마다 자동으로 호출되어 정보를 업데이트합니다.
window.mainloop()   #Tkinter 이벤트 루프를 시작합니다. 이 루프는 창이 닫힐 때까지 계속 실행되며, 사용자 입력과 같은 이벤트를 처리합니다.
