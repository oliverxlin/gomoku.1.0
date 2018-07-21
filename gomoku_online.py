import pygame
import pygame.font
import sys
import game_functions as gf
from button import Button
from game_stats import GameStats
import numpy as np
from settings import Setting
import ai
import requests,json,time
from threading import Thread
import queue
q = queue.Queue()
# http
header = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',   
        }
url = "http://47.94.219.255:8095"

# color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
player_color = "black"
player = "black_player"

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
 
        self._return = None
 
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
 
    def join(self):
        Thread.join(self)
        return self._return

def load_chessboard(screen):
    bg_surface = pygame.image.load("bg.png").convert()
    screen.blit(bg_surface,(0,0))
    rect_lines = [
        ((40, 40), (40, 600)),
        ((40, 40), (600, 40)),
        ((40, 600),(600, 600)),
        ((600, 40),(600, 600)),
    ]
    for line in rect_lines:
        pygame.draw.line(screen, BLACK, line[0], line[1], 3)

    for i in range(13):
        pygame.draw.line(screen, BLACK,(40 * (2 + i), 40),(40 * (2 + i), 600))
        pygame.draw.line(screen, BLACK,(40, 40 * (2 + i)),(600, 40 * (2 + i)))

    center_point = [
        (120, 120),
        (120, 520),
        (520, 120),
        (520, 520),
        (320, 320)
    ]
    for cp in center_point:
        pygame.draw.circle(screen, BLACK, cp, 5)

dot_list = [(40+i*40,40+j*40) for i in range(15 ) for j in range(15)]




def add_coin(screen, pos, color,movements):
    movements.append(((pos[0], pos[1]), color))
    pygame.draw.circle(screen, color,
        (pos[0], pos[1] ), 16)

def draw_movements(screen,movements):
    for m in movements:
        pygame.draw.circle(screen, m[1], m[0], 16)

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



def select_pos(screen,x,y,color,__black,__white,movements,stats):
    try:
        if __black[x][y]==0 and __white[x][y]==0:

            if color == 'black':
                __black[x][y] = 1
                add_coin(screen,dot_list[15*x+y],BLACK,movements)
                if checkIsWin(x,y,__black):
                    stats.game_active = False
                    stats.win_stats = True
            else:
                add_coin(screen,dot_list[15*x+y],WHITE,movements)
                __white[x][y] = 1
                if checkIsWin(x,y,__white):
                    stats.game_active = False
                    stats.win_stats = True
    except:
        print("error")

def run_game(id):
    
    global player_color,player,q
    game_settings = Setting()
    stats = GameStats()
    

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((game_settings.screen_width,game_settings.screen_height))
    pygame.display.set_caption("Gomoku")
    
    

    FPS = 50
    clock = pygame.time.Clock()

    
    

    play_button = Button(screen,"Start",(70,640))
    reset_button = Button(screen,"Reset",(170,640))
    repent_button = Button(screen,"Repent",(270,640))
    quit_button = Button(screen,"Quit",(570,640))
    movements = []

    __white = np.zeros((15,15))
    __black = np.zeros((15,15))
    board = np.zeros((15,15))
    
    flag = True
    running = True
    while running:
        load_chessboard(screen)
        time.sleep(0.75)
        gf.print_text(screen,"Welcome",20,700,50,BLACK)
        gf.print_text(screen,id+"!",20,700,75,BLACK)

        play_button.draw_button()
        reset_button.draw_button()
        repent_button.draw_button()
        quit_button.draw_button()
        draw_movements(screen,movements)
        pygame.display.flip()
        
        # 状态请求,绘制对方棋子
        data = {'black_player':-1,'white_player':-1,'chess':{'x':-1,'y':-1}}
        data = rep_chess()

        print(time.ctime())

        chess = data["chess"]
        print(data['black_player'],data['white_player'],player)
        print(time.ctime())
        if chess['x'] != -1:
            x = chess['x']
            y = chess['y']
            if player_color == "white" and data['white_player'] == 1:
                select_pos(screen,x,y,"black",__black,__white,movements,stats)
            elif player_color == "black" and data['black_player'] == 1:
                select_pos(screen,x,y,"white",__black,__white,movements,stats)
            print("对方落子",x,y)
        if data['black_player'] == 1 or data['white_player'] == 1:
            gf.print_to_screen(stats,screen,data['black_player'])
        times = True
        for event in pygame.event.get():    

            if event.type == pygame.QUIT:
                sys.exit
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                   __white = np.zeros((15,15))
                   __black = np.zeros((15,15))
                   movements = [] 
                   flag = True
                   pygame.event.set_blocked([1,4,pygame.KEYUP,pygame.JOYAXISMOTION,pygame.JOYBALLMOTION,pygame.JOYBUTTONDOWN,pygame.JOYBUTTONUP,pygame.JOYHATMOTION])
                   pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN,pygame.MOUSEBUTTONUP,pygame.KEYDOWN])
                break;
            if data[player] == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    m = event.pos[0]
                    n = event.pos[1]
                    
                    
                    # 开始游戏，初始化客户端和服务端参数
                    if play_button.rect.collidepoint(m,n):
                        stats.game_active = True
                        datas = {"id":id,"type":"START"}
                        datas = json.dumps(datas)
                        resp = requests.post(url,headers = header,data=datas)
                        resp_data = json.loads(resp.content)
                        player_color = resp_data['color']
                        print("id:{},color:{}",id,player_color)
                        if player_color == "white":
                            
                            player = "white_player"

                    if stats.win_stats == True:
                        
                        __white = np.zeros((15,15))
                        __black = np.zeros((15,15))
                        movements = [] 
                        flag = True
                        stats.win_stats= False
                        pygame.event.set_blocked([1,4,pygame.KEYUP,pygame.JOYAXISMOTION,pygame.JOYBALLMOTION,pygame.JOYBUTTONDOWN,pygame.JOYBUTTONUP,pygame.JOYHATMOTION])
                        pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN,pygame.MOUSEBUTTONUP,pygame.KEYDOWN])
                    
                        break

                    if stats.game_active == True:
                        if 20 < m <= 620 and 20 < n <= 620:
                            x = round(m//40.0)
                            y = round(n//40.0)
                            if m % 40 <= 20:
                                x = x - 1
                            if n % 40 <= 20:
                                y = y - 1
                    
                            if times:
                                flag = select_pos(screen,x,y,player_color,__black,__white,movements,stats)
                                datas = {"x":x,"y":y,"type":"FALL"}
                                datas = json.dumps(datas)
                                resp = requests.post(url,headers = header,data=datas)
                                print("己方落子",resp.content,x,y)
                                time.sleep(1)
                                times = False
                        
                        if reset_button.rect.collidepoint(m,n):
                            __white = np.zeros((15,15))
                            __black = np.zeros((15,15))
                            movements = [] 
                            flag = True
                            pygame.event.set_blocked([1,4,pygame.KEYUP,pygame.JOYAXISMOTION,pygame.JOYBALLMOTION,pygame.JOYBUTTONDOWN,pygame.JOYBUTTONUP,pygame.JOYHATMOTION])
                            pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN,pygame.MOUSEBUTTONUP,pygame.KEYDOWN])
                            break
                        
                        if repent_button.rect.collidepoint(m,n):
                            
                            if len(movements) != 0:
                                    
                                    if flag:
                                        last_step = movements.pop()
                                        raw = last_step[0][0]//40-1
                                        col = last_step[0][1]//40-1
                                        __white[raw][col] = 0
                                        __black[raw][col] = 0
                                        flag = not flag
                                    
                                    elif flag == False:
                                        last_step = movements.pop()
                                        raw = last_step[0][0]//40-1
                                        col = last_step[0][1]//40-1
                                        __white[raw][col] = 0
                                        __black[raw][col] = 0
                                        flag = not flag
                            else:
                                pass
                    if quit_button.rect.collidepoint(m,n):
                        pygame.quit()
                        sys.exit()   
        play_button.draw_button()
        reset_button.draw_button()
        repent_button.draw_button()
        quit_button.draw_button()
        draw_movements(screen,movements)
        pygame.display.flip()

# run_game()
def rep_chess():
    resp = requests.get(url)
    data = json.loads(resp.content)
    return data