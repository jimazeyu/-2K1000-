###通过排队论模型计算预计等待时间
###记录就餐情况


import time
import os
import threading
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import json
from PIL import Image
import  datetime
class data_analysis:
	def __init__(self):
		self.queue_num=6 #队列数目
		self.add=0 #每个队列增加人数
		self.left=0 #余下不足队列数目的人数，单独要插入的数目人数
		self.queue_list=[]#每个队列的人数
		self.enter_list=[]#进入人数情况的一个列表，每个数据为每次更新时获得的数据
		self.leave_list=[]#离开人数情况的一个列表，每个数据为每次更新时获得的数据
		self.all_list=[]#食堂总人数列表
		self.flag=1#一个循环数，从0-2，每10秒循环加1,0表示数据有更新
		self.average_time=30#记平均每个人打饭时间为30秒
		self.all_seats=1000#记总座位数为1000
		self.using_seats=0#已经被占用或预定占用的座位（我们认为在食堂但不在队列中的人都会去找一个座位）
		self.count_time=0#计算量，当count_time>average_time时，表示有人打完饭
		self.procpath=os.getcwd()#当前进程的目录
		self.dirpath=self.procpath+'\\'+'data'#存放各种数据的文件夹目录
		self.ntime=time.strftime('%Y-%m-%d %H:%M:%S')[0:10]#用于存放日期
		self.htime=time.strftime('%Y-%m-%d %H:%M:%S')[11:13]#记录当前的小时
		self.tflag='0' if int(self.htime)<9 else ('1' if int(self.htime)<15 else '2')#用于表明时间段，早上为0中午为1晚上为2
		self.stream=0#用来表示1秒进入人数
		self.renewtime=30#每30秒更新一次进入离开的人数
		self.xtime=time.strftime('%Y-%m-%d %H:%M:%S')[11:16]#用于存放当前的时刻
		self.xname=[]#一个存放时刻时间的列表，用于绘制表格
		self.jsonpath=self.procpath+'\\data\\json'#存放json文件的文件夹
		self.picpath=self.procpath+'\\data\\pic'#存放图片的文件夹
		'''
	函数说明：
	参数：void
	返回内容：void
	功能：删除7天前创建的文件夹
	'''
	def deleteOutdateFiles(self,path):
		current_time = time.strftime('%Y-%m-%d %H:%M:%S')[0:10]
		current_timeList = current_time.split("-")
		current_time_day = datetime.datetime(int(current_timeList[0]), int(current_timeList[1]), int(current_timeList[2]))        
		
		for root, dirs, files in os.walk(path):
			for item in files:
				file_path = os.path.join(root, item)
				create_time =  time.strftime("%Y-%m-%d", time.localtime((os.stat(path)).st_mtime))
				create_timeList = create_time.split("-")
				create_time_day = datetime.datetime(int(create_timeList[0]), int(create_timeList[1]), int(create_timeList[2]))
				time_difference = (current_time_day - create_time_day).days
				if time_difference > 7:
					os.remove(file_path)
	'''
	函数说明：
	参数：累计进入食堂人数sumenter，累计离开食堂人数sumleave,各队列情况queue_list,
	返回内容：预计等待时间 predict_time (单位：分钟),剩余可用座位seat_avail
	功能：计算预计等待时间，计算剩余座位，并将进入人数和离开人数存成列表,数据每10秒更新一次
	'''
	def calculation(self,enter,leave):
		if len(self.queue_list)==0:	#将队列情况初始化
			for i in range(0,self.queue_num):
				self.queue_list.append(0)
		self.count_time+=10#十秒更新一次数据，计时器加10
		leave_queue=0#离开队列的人数，初始化为0
		sum_people=enter-leave
		if self.flag==0:#数据有更新
			self.enter_list.append(enter)
			self.leave_list.append(leave)#进入，离开人数装填入列表
			if len(self.enter_list)>=2 and len(self.leave_list)>=2:#第二波更新数据后，上一段时间进出人数要减一下
				enter=self.enter_list[-1]-self.enter_list[-2]
				leave=self.leave_list[-1]-self.leave_list[-2]
			self.stream=enter/self.renewtime
			add=int(enter/self.queue_num)#分摊处理下，每个队列都要增加人数 
			self.left=enter%self.queue_num#分摊处理下，剩下的单独插入的人数
			for i in range(0,self.queue_num):
				if self.queue_list[i]>0 and self.count_time>=self.average_time:#队列非空并且有人打完饭   
					self.queue_list[i]-=1
					leave_queue+=1
				self.queue_list[i]+=add
			i=self.left
			j=0
			while i:
				if self.queue_list[j]==min(self.queue_list):#将剩余的要单独插入短队列的人插入短队列
					self.queue_list[j]+=1
					i-=1
				j=(j+1)%self.queue_num#队列列表下标循环加1
		else:#数据无更新，只需要考虑有无人离开队列
			for i in range(0,self.queue_num):
				if self.queue_list[i]>0 and self.count_time>=self.average_time:
					self.queue_list[i]-=1
					leave_queue+=1
		self.count_time%=self.average_time#计时器取余处理，便于与平均打饭时间比较
		predict_time=min(self.queue_list)*self.average_time
		#利用排队论模型计算考虑人流后的额外等待时间
		_lambda=self.stream
		s=self.queue_num
		mju=1/self.average_time
		k=30
		rou=_lambda/mju
		rou_s=rou/s
		p0=0
		for i in range(0,s):
			if rou_s!=1:
				p0+=(rou**i/(np.math.factorial(i))+(rou**s)*(1-rou_s**(k-s+1))/np.math.factorial(s)/(1-rou_s))
			else:
				p0+=(rou**i/(np.math.factorial(i)+(rou**s)*(k-s+1)/np.math.factorial(s)))
		p0=p0**-1
		if rou_s!=1:
			Lq=p0*(rou**s)*rou_s/(np.math.factorial(s)*((1-rou_s)**2))*(1-rou_s**(k-s+1)-(1-rou_s)*(k-s+1)*rou_s**(k-s))
		else:
			Lq=p0*(rou**s)*(k-s)*(k-s+1)/2/np.math.factorial(s)
		add_predict_time=Lq*self.average_time
		predict_time+=add_predict_time
		
		#时间处理成整数或整数+0.5的形式，向上处理
		if predict_time%60==0:
			predict_time=int(predict_time/60)
		else:
			if (predict_time/60)>int(predict_time/60)+0.5:
				predict_time=int(predict_time/60)+1
			else:
				predict_time=int(predict_time/60)+0.5
		#有人离开队列，使用座位数增加，有人离开食堂，使用座位数减少
		if self.flag==0:
			self.using_seats=self.using_seats-leave+leave_queue
		if self.using_seats>self.all_seats:#使用座位数介于0到总座位数
			 self.using_seats=self.all_seats
		elif self.using_seats<0:
			self.using_seats=0
		seat_avail=self.all_seats-self.using_seats
		self.flag=(self.flag+1)%(self.renewtime/10)#flag循环加1
		self.xtime=time.strftime('%Y-%m-%d %H:%M:%S')[11:16]#取更新时间的时刻，用于画折线图
		return predict_time,seat_avail,sum_people
	'''
	函数说明：
	参数：进入人数列表enter_list，离开人数leave_list
	返回内容:void
	计算当前时间点食堂总人数并以文件的形式存储
	'''
	def save_all_list(self):
		if len(self.enter_list)==0 or self.leave_list==0:#对于空列表，不执行本函数
			return
		if len(self.enter_list)>=1 and len(self.leave_list)>=1 and self.flag==0:#有数据更新
			allnow=self.enter_list[-1]-self.leave_list[-1]
			self.all_list.append(allnow)
			self.xname.append(self.xtime)
		if not(os.path.exists("data")):#创建一个用于存放所有文件的总文件夹
			os.mkdir("data")
		if not(os.path.exists(self.jsonpath)):
			os.mkdir(self.jsonpath)
		if not(os.path.exists(self.picpath)):
			os.mkdir(self.picpath)
		self.deleteOutdateFiles(self.picpath)#检查删除7天前的数据
		self.deleteOutdateFiles(self.jsonpath)
		json_name=self.ntime+'_'+self.tflag+'.json'
		json_savepath=self.jsonpath+'\\'+json_name
		with open(json_savepath,'w') as jsonfile:
			json.dump(self.all_list,jsonfile)
	'''
	函数说明
	参数：void
	返回内容：void
	功能：将当天食堂人数绘制成表
	'''	
	def drawchart_day(self):
		if len(self.all_list)==0:
			return
		y=self.all_list
		x=np.arange(0,len(y))
		plt.figure(figsize=(20,10),dpi=80)
		crowded_num=int(self.all_seats*0.75)
		y1=[]#y1是食堂人数较多时的点，可以修改
		x1=[]#x1存放相应的时间
		for i in range(0,len(y)):
			if y[i]>=crowded_num:
				y1.append(y[i])
				x1.append(x[i])
		i=0
		for y2 in y:
			if y2>=crowded_num:
				y1.append(y2)
				x1.append(i)
			i+=1
		font1 = {'family' : 'Times New Roman',
		'weight' : 'normal',
		'size'   : 20,}
		plt.scatter(x1,y1,label="crowded time")
		plt.legend(loc="upper left",prop=font1)
		plt.xticks(x[::4],self.xname[::4],rotation=45,size=20)
		plt.yticks(np.arange(min(y),max(y)+2)[::20],size=20)
		plt.xlabel("time",size=20)
		plt.ylabel("amount",size=20)
		plt.title("canteen",size=20)
		plt.plot(x,y,ms=10)
		figpath=self.picpath+'\\'+self.ntime+'.png'
		plt.savefig(figpath)
		plt.close()
	'''
	函数说明:
	参数：void
	返回内容：void
	功能:以直方图展示最近7天的数据（包括平均值，最高峰人数等，不足7天则只展示过去所有的数据）
	'''
	def drawhistory(self):
		y_name=['','','','','','','','']
		x=range(8)
		max_list=[0,0,0,0,0,0,0,0]
		avg_list=[0,0,0,0,0,0,0,0]
		i=0
		for root,dirs,files in os.walk(self.jsonpath):
			for jsonfile in files:
				path=os.path.join(root,jsonfile)
				with open(path) as json1:
					list1=json.load(json1)
					max_num=max(list1)
					list_sum=0
					for j in list1:
						list_sum+=int(j)
					list_len=len(list1)
					average_num=int(list_sum/list_len)+int(1)
					max_list[i]=max_num
					avg_list[i]=average_num
					y_name[i]=jsonfile[0:10]#存放日期
					i+=1
		plt.figure(figsize=(12,6),dpi=80)
		rect1=plt.barh(x,max_list,height=0.5,color='blue',label='max')
		rect2=plt.barh([i + 0.5 for i in x],avg_list,height=0.5,color='orange',label='average')
		plt.yticks([i+0.25 for i in x],y_name)
		plt.xlim(0,self.all_seats)
		plt.grid(alpha=0.4)
		plt.title("last 7 days")
		plt.legend(loc="upper right")
		figpath=self.picpath+'\\'+'history'+'.png'
		plt.savefig(figpath)
		plt.close()

if __name__ == "__main__":
	#以下是测试数据部分
	test_enter=[1, 10, 32, 47]####
	test_leave=[0, 0, 0, 0]###
	i1=0###
	calculation=data_analysis()
	enter=0
	leave=0
	while 1:
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
		calculation.drawchart_day()
		if(i1==len(test_enter)):###
			break###
		time.sleep(0.01)#
	#calculation.drawhistory()

