#coding=utf-8

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json,urllib
import numpy as np
from gomoku_sql import *


black_player = 1
white_player = 0
chesses = [(-1,-1)]

port = 8095
white = np.zeros((15,15))
black = np.zeros((15,15))


player = []
def checkIsWin(x,y,array):
    count1,count2,count3,count4 = 0,0,0,0
    i = x-1
    while(i>=0):
        if array[i][y] == 1:
            count1+=1
            i -= 1
        else:
            break
    i = x+1
    while i<15:
        if array[i][y] == 1:
            count1+=1
            i += 1
        else:
            break
    j =y-1
    while (j >= 0):
        if array[x][j] == 1:
            count2 += 1
            j -= 1
        else:
            break
    j = y + 1
    while j < 15:
        if array[x][j] == 1:
            count2 += 1
            j += 1
        else:
            break
    i,j = x-1,y-1
    while(i>=0 and j>=0):
        if array[i][j] == 1:
            count3 += 1
            i -= 1
            j -= 1
        else :
            break
    i, j = x + 1, y + 1
    while (i <= 14 and j <= 14):
        if array[i][j] == 1:
            count3 += 1
            i += 1
            j += 1
        else:
            break
    i, j = x + 1, y - 1
    while (i >= 0 and j >= 0):
        if array[i][j] == 1:
            count4 += 1
            i += 1
            j -= 1
        else:
            break
    i, j = x - 1, y + 1
    while (i <= 14 and j <= 14):
        if array[i][j] == 1:
            count4 += 1
            i -= 1
            j += 1
        else:
            break
    if count1>=4 or count2>=4 or count3 >= 4 or count4 >= 4:
        return True
    else:
        return False


def init_chessboard():
    global white_player,black_player,chesses,white,black

    chesses = []
    chesses.append((-1,-1))
    black_player = 1
    white_player = 0
    white = np.zeros((15,15))
    black = np.zeros((15,15))


class ServerHttp(BaseHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        print("初始化")
        BaseHTTPRequestHandler.__init__(self,*args,**kwargs)
         

    def do_GET(self):
        data = {"black_player":black_player,"white_player":white_player }
        global chesses
        data["chess"] = {"x":chesses[-1][0],"y":chesses[-1][1]}
        
        data = json.dumps(data)
        self.protocal_version = "HTTP/1.1" 
        self.send_response(200)
        self.send_header("Welcome", "Contect")
        self.send_header("Content-type","application/json")
        self.end_headers()
        
        self.wfile.write(data)


    def do_POST(self):
        global white_player,black_player,chesses,white,black,player
        
        datas = self.rfile.read(int((self.headers['content-length'])))
        data = json.loads(datas)
        
        # 登陆信息
        if data["type"] == "LOGIN":
            player = []
            init_chessboard()
            sql = db_process(db="gomoku",host="127.0.0.1",user="root",passwd="199814",default_table="player_info")
            sql.connect()
            pwd = sql.get_pwd_with_id(data["id"])
            rep_data = {"pwd":pwd}
            

        # 注册信息
        elif data["type"] == "REG":
            sql = db_process(db="gomoku",host="127.0.0.1",user="root",passwd="199814",default_table="player_info")
            sql.connect()
            reg_data = sql.write_data_with_id(id=data["id"],pwd=data["pwd"])
            rep_data = {"reg_data":reg_data}
            

        # 落子
        elif data["type"] == "FALL":
            chesses.append((data['x'],data['y']))
            if black_player == 1:
                black[data['x']][data['y']] = 1
                if checkIsWin(data['x'],data['y'],black):
                    print("\nblack win!")
                    f_black = open("{}_record".format(player[0]['id']),"a+")
                    f_white = open("{}_record".format(player[1]['id']),"a+")
                    f_black.write("{}({}) vs {}({}) : success!\n".format(player[0]['id'],player[0]['color'],player[1]['id'],player[1]['color']))
                    f_white.write("{}({}) vs {}({}) : fail!\n".format(player[1]['id'],player[1]['color'],player[0]['id'],player[0]['color']))
                    f_black.close()
                    f_white.close()

            else:
                white[data['x']][data['y']] = 1
                if checkIsWin(data['x'],data['y'],white):
                    print("\nwhite win!")
                    f_black = open("{}_record".format(player[0]['id']),"a+")
                    f_white = open("{}_record".format(player[1]['id']),"a+")
                    f_black.write("{}({}) vs {}({}) : fail!\n".format(player[0]['id'],player[0]['color'],player[1]['id'],player[1]['color']))
                    f_white.write("{}({}) vs {}({}) : success!\n".format(player[1]['id'],player[1]['color'],player[0]['id'],player[0]['color']))
                    f_black.close()
                    f_white.close()

            white_player,black_player = black_player,white_player
            rep_data = {"rep_data":"fall success!"}
            

        # 开始游戏 
        elif data['type'] == "START":
            
            if len(player) == 0:
                player.append({"id":data['id'],"color":"black"})
                rep_data = {"color":"black"}
            else:
                player.append({"id":data['id'],"color":"white"})
                rep_data = {"color":"white"}
            black_player = 1
            white_player = 0
            


        # 加载对局记录   
        elif data['type'] == "LOAD":
            id = data['id']
            try:
                f_record = open("{}_record".format(id),"r")
                rep_data = {"record":f_record.read()}
            except:
                rep_data = {"record":"NO RECORD!"}

        # 存储单机对局记录
        elif data['type'] == "SAVE":
            black_id = data['black_player_id']
            white_id = data['white_player_id']
            
            if data['win_color'] == "black":
                f_black = open("{}_record".format(black_id),"a+")
                f_black.write("{}({}) vs {}({}) : success!\n".format(black_id,"black",white_id,"white"))
                f_black.close()
                
                if black_id != white_id:
                    f_white = open("{}_record".format(white_id),"a+")
                    f_white.write("{}({}) vs {}({}) : fail!\n".format(white_id,"white",black_id,"black"))
                    f_white.close()

            if data['win_color'] == "white":
                f_black = open("{}_record".format(black_id),"a+")
                f_black.write("{}({}) vs {}({}) : fail!\n".format(black_id,"black",white_id,"white"))
                f_black.close()
                
                if black_id != white_id:
                    f_white = open("{}_record".format(white_id),"a+")
                    f_white.write("{}({}) vs {}({}) : success!\n".format(white_id,"white",black_id,"black"))
                    f_white.close()

            rep_data = {"rep_data":"success!"}
            

        rep_data = json.dumps(rep_data)
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()
        self.wfile.write(rep_data)

def start_server():
    http_server = HTTPServer(('',port), ServerHttp)
    http_server.serve_forever() #设置一直监听并接收请求`

if __name__ == '__main__':
    start_server()
