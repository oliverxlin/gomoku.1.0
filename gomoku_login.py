from tkinter import *
from tkinter.messagebox import *
import json
import requests
import re
import gomoku_alone
import gomoku_online
from tkinter import *
from PIL import Image ,ImageTk

header = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',   
        }
url = "http://47.94.219.255:8095"


print(url)

class LoginPage(object):
    def __init__(self,Root):
        self.root = Root
        self.root.geometry('%dx%d' % (400,300))
        self.username = StringVar()
        self.password = StringVar()
        self.createForm()
    

    def createForm(self):
        self.page = Frame(self.root)
        
        img = PhotoImage(file="Gomoku_logo.png")
        self.img = Label(self.root,image = img)
       
        self.img.pack(side=TOP)
        self.page.pack()
        Label(self.page,text="用户登陆",font=("宋体", 15)).grid(row=1, pady=10)
        Label(self.page, text = '账户: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=2, column=1, stick=E)
        Label(self.page, text = '密码: ').grid(row=3, stick=W, pady=10)

        Entry(self.page, textvariable=self.password, show='*').grid(row=3, column=1, stick=E)
        Button(self.page, text='登陆', command=self.loginCheck).grid(row=4, stick=W, pady=10)
        Button(self.page, text='注册并登陆', command=self.regCheck).grid(row=4,column=1, pady=10,padx=10)
        Button(self.page, text='游客登陆', command=self.visitorlogin).grid(row=4, column=2, stick=E)
        self.root.mainloop()

    def regCheck(self):
        id = self.username.get()
        pwd = self.password.get()
        datas = {"id":id,"type":"REG","pwd":pwd}
        
        datas = json.dumps(datas)
        resp = requests.post(url,headers = header,data=datas)
        print(resp.content)
        data = json.loads(resp.content.decode('utf-8').replace("'", "\""))
        

        if data["reg_data"] == "Reg Success!":
            self.page.destroy()
            #gomoku.run_game()
            MenuPage(self.root,id)
            
        elif data['reg_data'] == "Reg Failed!":
            showinfo(title='错误', message='注册错误，请重新注册！')              
        else:
            showinfo(title='错误', message='注册错误，请重新注册！')
    

    def loginCheck(self):
        id = self.username.get()
        pwd = self.password.get()
        datas = {"id":id,"type":"LOGIN"}
        
        datas = json.dumps(datas)
        resp = requests.post(url,headers = header,data=datas)
        print(resp.content)
        data = json.loads(resp.content.decode('utf-8').replace("'", "\""))
        

       
        if data["pwd"] == pwd:
            self.page.destroy()
            #gomoku.run_game()
            MenuPage(self.root,id)
            
        elif data['pwd'] == "Not Found!":
            showinfo(title='错误', message='账号不存在，请注册！')
                  
        else:
            showinfo(title='错误', message='账号或密码错误！')

    def visitorlogin(self):
        self.page.destroy()
        gomoku_alone.run_game("visitor")

class MenuPage(object):

    def __init__(self, Root=None,id=""):
        self.root = Root
        self.root.geometry('%dx%d' % (400, 350))
        self.createForm()
        self.id = id

    def createForm(self):
        self.page = Frame(self.root)
        self.page.pack()

        self.text = Text(self.page,width=40,height=10)
        self.text.grid(row=0,columnspan=3,stick=W,pady=10,padx=10)
        self.text.insert(INSERT,"      欢迎来到Gomoku游戏对战平台\n")
        Button(self.page, text='单机游戏', command=self.alone_game).grid(row=2,column=0,stick=W,padx = 10,pady=50)

        Button(self.page, text='在线游戏', command=self.online_game).grid(row=2, column=1, stick=W,padx = 10,pady=50)
        Button(self.page, text='对战记录', command=self.record).grid(row=2, column=2, stick=W,padx = 10,pady=50)

    def alone_game(self):
        gomoku_alone.run_game(self.id)
    def online_game(self):
        gomoku_online.run_game(self.id)
    def record(self):
        datas = {"type":"LOAD","id":self.id}
        datas = json.dumps(datas)
        resp = requests.post(url,headers=header,data=datas)
        data = json.loads(resp.content)
        record = "          对战记录\n" + data["record"]
        self.text.delete(1.0,END)
        self.text.insert(INSERT,record)

#RUN

if __name__ == '__main__':
    root = Tk()
    root.title('Gomoku对战平台')

    
    page1 =LoginPage(root)
    root.mainloop()
