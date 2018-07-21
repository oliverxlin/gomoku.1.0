import pygame.font

class Button():
    '''创建一个button'''
    
    def __init__(self,screen,msg,pos):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width = 75
        self.height = 33
        self.button_color = (139,69,19)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,25)

        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = pos
        self.prep_msg(msg)


    def prep_msg(self,msg):
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw_button(self):
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)
