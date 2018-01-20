#!-*- coding:utf-8 -*-
from tkinter import *
import requests
import json
import time
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"}
#url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2018-02-04&leftTicketDTO.from_station=WHN&leftTicketDTO.to_station=BMH&purpose_codes=ADULT"
#surl = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2018-02-04&leftTicketDTO.from_station=WHN&leftTicketDTO.to_station=HFH&purpose_codes=ADULT'
class Check_ticket():
    def __init__(self):
        self.response=None
        self.string1 = StringVar()
        self.string2 = StringVar()
        self.root = Tk()
        self.root.geometry("760x400+200+200")
        self.root.resizable(False,False)
        self.train_num = Label(self.root,text = '车次',width = 8,font=2)
        self.from_station = Label(self.root,text = '出发站',width =8,font=2)
        self.to_station = Label(self.root,text = '终点站',width=8,font=2)
        self.start_time = Label(self.root,text = '出发时间',width=10,font=2)
        self.end_time = Label(self.root,text = '到达时间',width=10,font=2)
        self.duration = Label(self.root,text = '时长',width=6,font=2)
        self.second = Label(self.root,text = '二等座',width=8,font=2)
        self.first = Label(self.root,text = '一等座',width = 8, font=2)
        self.special = Label(self.root,text = '商务座',width = 8, font=2)
        
        self.box = Listbox(self.root,width=86,height=20)
        self.check_button = Button(self.root,text = '自动查询',height=1,widt=8)
        self.sel_check_button = Button(self.root,text='手动查询',height=1,width=8,command=self.write_info)
        self.exit = Button(self.root,text = '退出',height=1,width=8,command=self.root.quit)
        self.change_button = Button(self.root,text='交换始发站',width=10,command = self.change_)
        #添加菜单
        self.menu = Menu(self.root)
        self.fileMenu = Menu(self.menu,tearoff=0)

        #添加输入框
        self.start_label = Label(self.root,text='始发站',width=10)
        self.start_input = Entry(self.root,textvariable = self.string1,width=10)
        self.end_label = Label(self.root,text='终点站',width=10)
        self.end_input = Entry(self.root,textvariable = self.string2,width=10)
        self.trip_time = Label(self.root,text='出发日期',width=10)
        self.trip_input = Entry(self.root,w=15)

    def change_(self):
    	temp = self.start_input.get()
        temp2 = self.end_input.get()
        self.string1.set(temp2)
        self.string2.get(temp)
    	

    	#self.start_input.insert(0,temp2)
    	#self.end_input.insert(0,temp1)

    def get_url(self):
    	station = {'武汉':'WHN','蚌埠':'BMH'}
    	start_key = self.start_input.get()
    	end_key = self.end_input.get()
    	start_value = station[start_key]
    	end_value = station[end_key]
    	date = self.trip_input.get()
    	url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date='+date+'&leftTicketDTO.from_station='+start_value+'&leftTicketDTO.to_station='+end_value+'&purpose_codes=ADULT'
    	return url
    def get_info(self):
        url = self.get_url()
        self.response = requests.get(url,headers=headers,timeout=10)

        self.ret = json.loads(self.response.text.replace("\'\'","\"\"",100))
        
         # 获取站点及代号
        addr = self.ret['data']['map']

        # 获取所有车次信息
        infos = self.ret['data']['result']

        train_num = []

        for info in infos:
            temp = []
            info = info.split('|')
            if len(info) == 37:
                temp.append(info[3]) #车次 
                temp.append(addr[info[6]]) #起始站 
                temp.append(addr[info[7]]) #终点站
                temp.append(info[8]) #infotart time
                temp.append(info[9]) # end time
                temp.append(info[10]) # 时间段
                temp.append(info[30]) #二等座
                temp.append(info[31]) #一等座
                temp.append(info[32]) #商务座
                train_num.append(temp)               
        return train_num

    def write_info(self):
        self.box.delete(0,END)
        trains = self.get_info()
        for train in trains:
            data = ""
            for j in train:
           	    data = data +('%-15s' % j)
            self.box.insert(END,data)

   
    def main(self):
        
        # tag
        self.train_num.grid(row=1,column=1)
        self.from_station.grid(row=1,column=2)
        self.to_station.grid(row=1,column=3)
        self.start_time.grid(row=1,column=4)
        self.end_time.grid(row=1,column=5)
        self.duration.grid(row=1,column=6)
        self.second.grid(row=1,column=7)
        self.first.grid(row=1,column=8)
        self.special.grid(row=1,column=9)

        self.start_label.place(x=640,y=150)
        self.strin1 = StringVar()
        self.start_input.place(x=642,y=180)
        self.start_input.focus()
        self.end_label.place(x=640,y=210)
        self.string2=StringVar()
        self.end_input.place(x=642,y=240)

        self.trip_time.place(x=640,y=270)
        self.trip_input.place(x=640,y=300)
        # Button--command
        self.check_button.grid(row=2,column=10)
        self.sel_check_button.grid(row=4,column=10)
        self.exit.grid(row=6,column=10)
        self.change_button.place(x=640,y=330)
        project = ['From_station','To_station']
        for pro in project:
        	self.fileMenu.add_command(label=pro)
        self.fileMenu.add_separator()
        self.menu.add_cascade(label='Station',menu=self.fileMenu)

        self.root['menu']=self.menu
        self.box.place(x=15,y=30)
        self.root.mainloop()

check = Check_ticket()
check.main()