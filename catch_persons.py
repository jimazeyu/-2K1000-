###摄像机人流统计

import cv2
import numpy as np
import math

test=cv2.VideoCapture('test.mp4')
centers=[]#圆心的列表
peo_num=0


while True:
    ret,img=test.read()
    cv2.imshow("video2",img)
    cv2.waitKey(1)
    img = cv2.resize(img, None, fx=0.35, fy=0.35, interpolation=cv2.INTER_AREA)
    img = cv2.bilateralFilter(img,0,280,15)
    
    #img_gauss=cv2.GaussianBlur(img,(5,5),1)#高斯滤波  
    
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    ret,img_erzhi = cv2.threshold(img_gray,30,255,cv2.THRESH_BINARY)
    
    cv2.imshow("video1",img_erzhi)
    cv2.waitKey(1)
    
    
    
    cimage=img_erzhi
    
    #霍夫圆
    circles = cv2.HoughCircles(cimage,cv2.HOUGH_GRADIENT,1.7,15,

                            param1=50,param2=30,minRadius=0,maxRadius=0)
    if circles is None:
        continue
    else:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:

        # 画出圆的边缘

            cv2.circle(cimage,(i[0],i[1]),i[2],(0,0,255),2)

        # 画出圆心

            cv2.circle(cimage,(i[0],i[1]),2,(0,0,255),2)
        print(circles[0, : ])
    #圆心追踪
   
        for i in circles[0,:]:
            if centers == []:
                centers.append(i)
            else:
                dis=1000000
                k=[0,0]
                for j in centers:
                    if (math.pow((i[0]-j[0]),2)+math.pow((i[1]-j[1]),2))<dis:
                        dis=math.pow((i[0]-j[0]),2)+math.pow((i[1]-j[1]),2)
                        k[0]=j[0]
                        k[1]=j[1]
                for l in range(len(centers)):
                    if centers[l]==k:
                        centers[l]=i
                i_pre=k
    
    #判断人是否通过中间的分界线
        for i in centers:
            if centers==[]:
                peo_num=0
            else:
            
                if (i[1]>960) and (i_pre[1]<=960):    #如果上一帧圆心在分界线左边切下一帧在分界线右边
                    peo_num=peo_num+1    #k是上一帧对应的圆心
    
    #cv2.imshow("img", img_erzhi)  

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()    
        exit(0)