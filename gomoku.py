import pygame
import sys
import game_functions as gf
from button import Button
from game_stats import GameStats
import numpy as np
from settings import Setting
from ai import *
import time,json,requests
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# http
header = {
'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36', 
}
url = "http://47.94.219.255:8095"

def load_chessboard(screen):
    ''' 初始化棋盘'''

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
    '''将落子加入序列,并在屏幕画出'''

    movements.append(((pos[0], pos[1]), color))
    pygame.draw.circle(screen, color,
        (pos[0], pos[1] ), 16)
    # hit_sound.play()

def draw_movements(screen,movements):
    '''更新屏幕落子'''

    for m in movements:
        pygame.draw.circle(screen, m[1], m[0], 16)

def checkIsWin(x,y,array):
    '''判断输赢'''

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
    while (i >= 0 and j >= 0 and i<=14):
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


def ai_chess(chessboard_int,x,y):
    ''' 通过ai 判断落子坐标'''

    start = time.clock()
    ai = searcher()
    ai.board = chessboard_int
    ai_pos = ai.search(2,2)
    
    end = time.clock()
    print((x,y))
    print("ai")
    print(end-start)
    print(ai_pos[1],ai_pos[0])
    return ai_pos

def select_pos(screen,x,y,flag,__black,__white,movements,stats):
    '''落子'''

    try:    
        if __black[x][y]==0 and __white[x][y]==0:

            if flag:
                flag = not flag
                __black[x][y] = 1
                add_coin(screen,dot_list[15*x+y],BLACK,movements)
                if stats.ai_active == True:
                    chessboard = gf.chess_add(__black,__white)
                    ai_pos = ai_chess(chessboard,x,y)
                    ai_x = ai_pos[1]
                    ai_y = ai_pos[0]
                    flag = select_pos(screen,ai_x,ai_y,flag,__black,__white,movements,stats)

                if checkIsWin(x,y,__black):
                    print(1)
                    stats.win_stats = True
                    stats.game_active = False

                    datas = {"type":"SAVE","black_player_id":"321"}
                    if stats.ai_active == True:
                        datas['white_player_id'] = "AI"
                    else: 
                        datas['white_player_id'] = "321"
                    datas['win_color'] = "black"
                    datas = json.dumps(datas)
                    resp = requests.post(url,headers = header,data=datas)
            else:
                flag = not flag
                add_coin(screen,dot_list[15*x+y],WHITE,movements)
                __white[x][y] = 1
                if checkIsWin(x,y,__white):
                    print(2)
                    stats.win_stats = True
                    stats.game_active = False
                    datas = {"type":"SAVE","black_player_id":"321"}
                    if stats.ai_active == True:
                        datas['white_player_id'] = "AI"
                    else: 
                        datas['white_player_id'] = "321"
                    datas['win_color'] = "white"
                    datas = json.dumps(datas)
                    resp = requests.post(url,headers = header,data=datas)
    
    except Exception as e:
        print("Exception:", str(Exception))
        print ("e:"+ str(e))
        print ("repr(e):"+ repr(e))
        print ("message:"+ e.message)
        print ("traceback.print_exc():"+traceback.print_exc())
        print (traceback.format_exc())
        print ("########################################################") 

    return flag

def run_game(user):
    '''运行游戏'''
    
    game_settings = Setting()
    stats = GameStats()


    pygame.init()
    
    screen = pygame.display.set_mode((game_settings.screen_width,game_settings.screen_height))
    pygame.display.set_caption("Gomoku")
    pygame.mixer.music.set_volume(0.4)

    FPS = 50
    clock = pygame.time.Clock()

    play_button = Button(screen,"Start",(70,640))
    # vshuman_button = Button(screen,"Double",(160,640))
    reset_button = Button(screen,"Reset",(160,640))
    repent_button = Button(screen,"Repent",(250,640))
    quit_button = Button(screen,"Quit",(570,640))
    AI_button = Button(screen,"AI",(470,640))

    '''初始化棋子序列和黑白棋盘'''

    movements = []

    __white = np.zeros((15,15))
    __black = np.zeros((15,15))
    board = np.zeros((15,15))
    

    flag = True
    running = True
    while running:

        # clock.tick(FPS)
        time.sleep(0.75)
        load_chessboard(screen)
        gf.print_text(screen,"Welcome",20,700,50,BLACK)
        gf.print_text(screen,user+"!",20,700,75,BLACK)
        gf.print_to_screen(stats,screen,flag)
        
        
    
        draw_movements(screen,movements)
        pygame.display.flip()
        play_button.draw_button()
        reset_button.draw_button()
        repent_button.draw_button()
        quit_button.draw_button()
        AI_button.draw_button()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                m = event.pos[0]
                n = event.pos[1]
                
                if play_button.rect.collidepoint(m,n):
                    stats.game_active = True
                
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

                        flag = select_pos(screen,x,y,flag,__black,__white,movements,stats)

                    if reset_button.rect.collidepoint(m,n):
                        __white = np.zeros((15,15))
                        __black = np.zeros((15,15))
                        movements = [] 
                        flag = True
                        stats.win_stats= False
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
                    
                    if AI_button.rect.collidepoint(m,n):
                        stats.ai_active = True
                        ""
                
                if quit_button.rect.collidepoint(m,n):
                    pygame.quit()
                    sys.exit()
            
        draw_movements(screen,movements)
        pygame.display.flip()
    pygame.quit()

if __name__=="__main__":
    run_game("Gomoku Player")

