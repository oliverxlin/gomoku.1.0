import pygame
import sys
import numpy as np

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

font_name = pygame. font.get_default_font()

def print_text(screen, text, size, x, y, color=WHITE):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y) 
    screen.blit(text_surface, text_rect)    
    pygame.display.flip()


def print_to_screen(stats,screen,flag,color=WHITE):
    '''输出文字到屏幕'''

    if stats.game_active:
        if flag:
            print_text(screen,"Black Now",23,700,120)
            if stats.ai_active == True:
                print_text(screen,"Fight against AI",23,700,450,BLACK)
        else:
            print_text(screen,"White Now",23,700,120)
            if stats.ai_active == False:
                print_text(screen,"Fight against",23,700,450,BLACK)
                print_text(screen," Human",23,700,485,BLACK)
    else :
        if stats.win_stats and not flag:
            
            print_text(screen,"Game over",23,700,120)
            print_text(screen,"Black win!",25,700,140)
            print_text(screen,"Pressing  ",23,700,205)
            print_text(screen,"Start Button",23,700,240)

        elif stats.win_stats and flag:
            
            print_text(screen,"Game over",23,700,120)
            print_text(screen,"White win!",25,700,145)
            print_text(screen,"Pressing  ",23,700,205)
            print_text(screen,"Start Button",23,700,240)

        else:
            
            print_text(screen,"Pressing  ",23,700,120)
            print_text(screen,"Start Button",23,700,145)
   

def chess_add(__black,__white):
    '''黑白棋盘合并'''

    white_board = one_to_two(__white)
    board = __black + white_board
    board_T = board.T
    board_int = board_T.astype(int)
    return board_int


def one_to_two(matrix):
    '''矩阵中的1全部变成2'''
    bor = np.zeros((15,15))
    for i in range(15):
        for j in range(15):
            if matrix[i][j] == 1:
                bor[i][j] = 2

    return bor