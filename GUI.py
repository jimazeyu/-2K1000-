###上位机界面

from mttkinter import mtTkinter as tk
import cv2
from PIL import Image,ImageTk
from update_data import*
from calculation_part import*
import os

def update(sum_people,predict_time,seat_avail):#更新数据
    lock=threading.Lock()
    lock.acquire()
    global persons  ##食堂目前人数
    global seats  ##食堂剩余座位数
    global time_to_wait ##等待时间    
    persons.set(sum_people)
    time_to_wait.set(predict_time)
    seats.set(seat_avail)
    lock.release()

def test():   #测试程序

    test_enter=[1, 10, 32, 47, 62, 85, 107, 140, 195, 244, 301, 390, 489, 611, 707]###
    test_leave=[0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 6, 11, 20, 30]###
    i1=0###
    calculation=data_analysis()
    enter=0
    leave=0
    while 1:
        lock=threading.Lock()
        lock.acquire()
        if calculation.flag==0: 
            enter=test_enter[i1]###
            leave=test_leave[i1]###
            i1+=1###
        predict_time,seat_avail,sum_people=calculation.calculation(enter,leave)
        print("进入食堂人数情况：{}".format(calculation.enter_list))
        print("离开食堂人数情况：{}".format(calculation.leave_list))
        print("食堂当前人数：{}".format(sum_people))
        print("各队列人数：{}".format(calculation.queue_list))
        print("剩余座位：{}".format(seat_avail))
        print("预计等待时间：{}分钟".format(predict_time))
        print()
        calculation.save_all_list()
        #calculation.drawchart_day()
        update(sum_people,predict_time,seat_avail)
        if(i1==len(test_enter)):###
            break###
        time.sleep(1)#
        lock.release()

def process_test():
    thread=threading.Thread(target=test)
    thread.start()

def show_day():#展示今天数据
    ntime=time.strftime('%Y-%m-%d %H:%M:%S')[0:10]
    src='data/pic/'+ntime+'.png'
    print(src)
    print(os.path.isfile(src))
    pic=cv2.imread(src)
    pic = cv2.resize(pic,None,fx=0.5,fy=0.5)
    cv2.imshow("today_fig",pic)
    cv2.waitKey(0)

def to_show_day():
    thread=threading.Thread(target=show_day)
    thread.start()

def show_history():#展示历史数据
    ntime=time.strftime('%Y-%m-%d %H:%M:%S')[0:10]
    src="data/pic/"+ntime+'.png'
    pic=cv2.imread(src)
    pic = cv2.resize(pic,None,fx=0.5,fy=0.5)
    cv2.imshow("今日情况",pic)
    cv2.waitKey(0)

def to_show_history():
    thread=threading.Thread(target=show_history)
    thread.start()

def video_loop(): #视频监控
    global camera
    global cap
    ret, img = cap.read()
    if ret:
        cv2.waitKey(50)
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)#转换颜色从BGR到RGBA
        current_image = Image.fromarray(cv2image)#将图像转换成Image对象
        imgtk = ImageTk.PhotoImage(image=current_image)
        panel.imgtk = imgtk
        panel.config(image=imgtk)
        window.after(1, video_loop)

class GUI():
    def __init__(self, window):
        self.initGUI(window)
    def initGUI(self, root):
        window.title("食堂监测")
        window.geometry('800x600')
        global persons  ##食堂目前人数
        global seats  ##食堂剩余座位数
        global time_to_wait ##等待时间
        label=tk.Label(window,text='食堂目前情况：',font=("Calibri",22))
        label.grid(row=1,column=1)

        label=tk.Label(window,text='食堂目前人数：',font=("Calibri",12))
        label.grid(row=2,column=1)
        e=tk.Entry(window,font=("Calibri",22),textvariable=persons,state="disabled")
        e.grid(row=2,column=2)

        label=tk.Label(window,text='食堂剩余座位数：',font=("Calibri",12))
        label.grid(row=3,column=1)
        e=tk.Entry(window,font=("Calibri",22),textvariable=seats,state="disabled")
        e.grid(row=3,column=2)

        label=tk.Label(window,text='需要等待时间：',font=("Calibri",12))
        label.grid(row=4,column=1)
        e=tk.Entry(window,font=("Calibri",22),textvariable=time_to_wait,state="disabled")
        e.grid(row=4,column=2)

        label=tk.Label(window,text='食堂温度：',font=("Calibri",12))
        label.grid(row=5,column=1)
        e=tk.Entry(window,font=("Calibri",22),textvariable=temp,state="disabled")
        e.grid(row=5,column=2)        

        label=tk.Label(window,text='食堂就餐分析：',font=("Calibri",22))
        label.grid(row=6,column=1)

        btn=tk.Button(window,text='今日就餐情况',command=to_show_day)
        btn.grid(row=7,column=1)
        btn=tk.Button(window,text='历史就餐情况',command=process_test)
        btn.grid(row=8,column=1)

        label=tk.Label(window,text='食堂监控：',font=("Calibri",22))
        label.grid(row=9,column=1)
        global panel
        panel.grid(row=9,column=2)
        window.config(cursor="arrow")
        video_loop()
        window.mainloop()

if __name__ == "__main__":
    total_seats=1000 ##总座位数
    window = tk.Tk()    
    persons = tk.StringVar()  ##食堂目前人数
    persons.set('0')
    seats = tk.StringVar()  ##食堂剩余座位数
    seats.set('1000')
    time_to_wait=tk.StringVar() ##等待时间
    time_to_wait.set('0')
    temp=tk.StringVar() ##食堂温度
    temp.set('23°C')
    lock=threading.Lock()
    cap = cv2.VideoCapture('test.mp4')
    camera = cv2.VideoCapture(0)    #摄像头
    panel = tk.Label(window)  #视频监控窗口
    myGUI = GUI(window)
