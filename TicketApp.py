#!-*-coding:utf-8 -*-
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import requests
import time
import json
import threading
class Widget():
    def __init__(self):

        self.flag = True
        self.t=None
        self.mutex=threading.Lock()
        self.root = Tk()
        self.root.title('12306火车票查询系统')
        self.root.resizable(False,False)
        #self.root.geometry("600x300+200+200")
        self.frame_bottom=Frame(width=800,height=100)
        self.frame_top = Frame(width=800,height=50)

        # 上部Frame,由左到右，依次添加控件
        # 显示当前日期,
        #Label : row=0, column = 0/1
        #所在位置为第一行的1、2两列
        self.date_title = Label(self.frame_top,text='当前日期',width=8)
        self.date_label = Label(self.frame_top,text = '',width=10)
        self.date_title.grid(row=0,column=0)
        self.date_label.grid(row=0,column=1)

        # 显示出行日期
        #位置:第二行的1、2两列
        self.time_string = StringVar()
        #self.time_string.set('2018-01-01')
        self.time_label = Label(self.frame_top,text='出行日期',width=8,pady=5)
        self.time_entry = Entry(self.frame_top,textvariable=self.time_string,width=10)
        self.time_label.grid(row=1,column=0)
        self.time_entry.grid(row=1,column=1)

        # 调用set_date方法，显示当前日期，及初始化出行日期
        self.set_date()
        
        # 添加始发站(标签及输入框)
        #位置:第1行的3、4两列
        self.start_string = StringVar()
        self.start_string.set('合肥')
        self.start_label = Label(self.frame_top,text='出发站',width=8,padx=2,pady=5)
        self.start_entry = Entry(self.frame_top,textvariable = self.start_string,width=10)
        self.start_label.grid(row=0,column=2)
        self.start_entry.grid(row=0,column=3)
        
        # 添加终点站(标签及输入框)
        #位置:第2行的3、4列
        self.end_string = StringVar()
        self.end_string.set('武汉')
        self.end_label = Label(self.frame_top,text='终点站',width=8,padx=2,pady=5)
        self.end_entry = Entry(self.frame_top,textvariable=self.end_string,width=10)
        self.end_label.grid(row=1,column=2)
        self.end_entry.grid(row=1,column=3)

        # 命令按钮
        #位置:第3行的5、6列
        self.check_button = Button(self.frame_top,text='查询',width=10,command=self.check_ticket)
        self.check_button_ = Button(self.frame_top,text='自动查询',width=10,command=self.auto_check_ticket)
        self.change_button = Button(self.frame_top,text='交换始发站',width=10,command = self.change_station)
        self.exit_button = Button(self.frame_top,text='退出',width=10,command=self.root.quit)
        self.clear_button = Button(self.frame_top,text='清空列表',width=10,command=self.clear_conent)
        self.check_button.grid(row=0,column=4,padx=10,pady=10)
        self.check_button_.grid(row=1,column=4,padx=10,pady=10)
        self.change_button.grid(row=0,column=5,padx=10,pady=10)
        self.exit_button.grid(row=1,column=5,padx=10,pady=10)
        self.clear_button.grid(row=0,column=6,padx=10,pady=10)

        self.num_label = Label(self.frame_top,text='查询到车次:',width=10)
        self.num_label.grid(row=1,column=6,padx=0,pady=5)
        self.display  = Label(self.frame_top,text='',width=8)
        self.display.grid(row=1,column=7,padx=0,pady=5)


        #登录窗口
        self.login_bt = Button(self.frame_top,text='登录',width=6)
        self.name = Label(self.frame_top,text='用户名:',width=8)
        self.pwd = Label(self.frame_top,text='密码:',width=8)
        self.name_entry = Entry(self.frame_top,width=12)
        self.pwd_entry = Entry(self.frame_top,width=12)
        self.login_bt.grid(row=0,column=7)
        self.name.grid(row=0,column=8)
        self.name_entry.grid(row=0,column=9)
        self.pwd.grid(row=1,column=8)
        self.pwd_entry.grid(row=1,column=9)
        # 下部Frame部件
        cols = ('a','b','c','d','e','f','g','h','i','j','k','m','n','p','q')
        
        self.treeview = ttk.Treeview(self.frame_bottom,show='headings',height=18,columns=cols,selectmode='browse')
        self.scroll = ttk.Scrollbar(self.frame_bottom,orient='vertical',command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scroll.set)
        self.treeview.column('a',width=65,anchor='center')
        self.treeview.column('b',width=65,anchor='center')
        self.treeview.column('c',width=65,anchor='center')
        self.treeview.column('d',width=70,anchor='center')
        self.treeview.column('e',width=70,anchor='center')
        self.treeview.column('f',width=60,anchor='center')
        self.treeview.column('g',width=50,anchor='center')
        self.treeview.column('h',width=50,anchor='center')
        self.treeview.column('i',width=50,anchor='center')    
        self.treeview.column('j',width=50,anchor='center')    
        self.treeview.column('k',width=50,anchor='center')    
        self.treeview.column('m',width=50,anchor='center')
        self.treeview.column('n',width=50,anchor='center')
        self.treeview.column('p',width=50,anchor='center')
        self.treeview.column('q',width=70,anchor='center')
        self.treeview.heading('a' ,text='车次')
        self.treeview.heading('b' ,text='出发站')
        self.treeview.heading('c' ,text='终点站')
        self.treeview.heading('d' ,text='出发时间')
        self.treeview.heading('e' ,text='到达时间')
        self.treeview.heading('f' ,text='时长')
        self.treeview.heading('g' ,text='软卧')
        self.treeview.heading('h' ,text='无座')
        self.treeview.heading('i' ,text='硬卧')
        self.treeview.heading('j' ,text='硬座')
        self.treeview.heading('k' ,text='二等座')
        self.treeview.heading('m' ,text='一等座')
        self.treeview.heading('n' ,text='商务座')
        self.treeview.heading('p' ,text='动卧')
        self.treeview.heading('q' ,text='日期')
        self.treeview.grid(row=0,column=0,sticky=NSEW)
        self.scroll.grid(row=0,column=1,sticky=NSEW)
        #self.scroll.pack(side=RIGHT,fill=Y)








    def get_train_times(self):
         num = len(self.treeview.get_children())
         self.display['text']=str(num)+' 班列车'
       
    def set_date(self):
        date =time.strftime('%Y-%m-%d',time.localtime(time.time()))
        self.date_label['text']=date
        self.time_string.set(date)

    def change_station(self):
        temp1 = self.start_entry.get()
        temp2 = self.end_entry.get()
        self.start_string.set(temp2)
        self.end_string.set(temp1)
    
        # 获取出行日期
    def get_date(self):
        return self.time_entry.get()

        #获取用户输入的站点
    def get_station_name(self):
        st1,st2 =  self.start_entry.get(),self.end_entry.get()
        return st1,st2


        #设置站点代码
    def station_dict(self):
        station_dict = {
                    "武汉":'WHN',
                    "汉口":'HKN',
                    "武昌":'WCN',
                    "蚌埠":'BMH',
                    "合肥":'HFH',
                    "北京":'BJP',
                    "上海":'SHH',
                    "广州":'GZQ',
                    "重庆":'CQW',
                    "重庆北":'CUW'
                    }
        return station_dict

        # 获取站点代码
    def get_station_code(self):
        s_dict = self.station_dict()
        sname, ename = self.get_station_name()            
        s_code = s_dict[sname]
        e_code = s_dict[ename]
        return s_code,e_code  #返回始发站的代码

        #根据用户输入站点和日期修正url
    def fix_url(self):
        date = self.get_date()
        s_code ,e_code = self.get_station_code()
        url =url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date='+date+'&leftTicketDTO.from_station='+s_code+'&leftTicketDTO.to_station='+e_code+'&purpose_codes=ADULT'
        get_header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"}
        return url,get_header

    def get_info(self):
        url, header = self.fix_url()
        addr = []
        info = []
        try:
            response = requests.get(url,headers=header,timeout=20)
            response = json.loads(response.text)
        except Exception as e:
            print('timeout')
            print(e)
        else:
            addr = response['data']['map']
            info = response['data']['result']
        return addr,info

    def train_info(self):
        addr ,info = self.get_info()
        #print(info)
        #train_num = []
        for item in info:
            temp = []
            item = item.split("|")
            if len(item)==37:
                temp.append(item[3]) #车次 
                temp.append(addr[item[6]]) #起始站 
                temp.append(addr[item[7]]) #终点站
                temp.append(item[8]) #itemtart time
                temp.append(item[9]) # end time
                temp.append(item[10]) # 时间段
                temp.append(item[23]) #软卧
                temp.append(item[26]) #无坐
                temp.append(item[28]) #硬卧
                temp.append(item[29]) #硬座
                temp.append(item[30]) #二等座
                temp.append(item[31]) #一等座
                temp.append(item[32]) #商务座
                temp.append(item[33]) #动卧
                temp.append(item[13]) #出行日期
                #train_num.append(temp)
                self.treeview.insert('','end',values=temp)
        #print(train_num)

    def clear_conent(self):

        for _ in map(self.treeview.delete,self.treeview.get_children("")):
            pass

    def check_ticket(self):
        a,b = self.get_station_name()
        if a=='' or b=='':
            tkinter.messagebox.showinfo('提示','不能为空!!!')
            return
        self.train_info()
        self.get_train_times()

    def auto_check_ticket(self):
        for i in range(10):
            self.t=threading.Thread(target=self.check_thread)
            #print('current thread is %d' % i)
            self.t.start()
            
        

    def check_thread(self):
        self.mutex.acquire(10)
        a,b = self.get_station_name()
        if a=='' or b=='':
            a='武汉'
            b='合肥'
            
        self.train_info()
        self.get_train_times()
        time.sleep(10)
        self.mutex.release()        
        
           
                
    def main(self):
        #self.frame_left.grid(row=0, column=0, columnspan=2, padx=4, pady=5)
        #self.frame_right.grid(row=0,column=10,columnspan=2,padx=4,pady=5)
        self.frame_top.pack(side=TOP)
        self.frame_bottom.pack(side=BOTTOM) 
        self.root.mainloop()
        


app =Widget()
app.main()