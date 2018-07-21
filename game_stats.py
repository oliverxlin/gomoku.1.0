class GameStats():
    def __init__(self):
        
        # self.reset_stats()
        self.game_active = False
        self.ai_active = False
        self.online_active = False
        self.high_score = 0
        self.win_stats = False
        self.gameover_stats = self.game_active and self.win_stats


    def reset_stats(self):
        
        self.score = 0
        self.level = 1