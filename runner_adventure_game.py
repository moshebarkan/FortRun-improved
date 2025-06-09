import pygame
import random
from typing import Dict, List, Tuple

# קבועים
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 520
FPS = 60
PLAYER_MOVE_DELAY = 150
ITEM_SPAWN_INTERVAL = 1000
PLAYER_Y = 320
PATH_POSITIONS = {"Left": 300, "Mid": 495, "Right": 690}

# צבעים
COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "ORANGE": (255, 165, 0),
    "BROWN": (165, 42, 42)
}

class GameState:
    def __init__(self):
        self.y_1 = -SCREEN_HEIGHT
        self.y_2 = 0
        self.lives = 3
        self.mats_count = 0
        self.mats_spawned = 0
        self.selected_character = "pics/Runner1.png"
        self.path = "Mid"
        self.x_player = PATH_POSITIONS["Mid"]

class AssetLoader:
    @staticmethod
    def load_image(path: str, size: Tuple[int, int] = None) -> pygame.Surface:
        try:
            image = pygame.image.load(path)
            if size:
                return pygame.transform.scale(image, size)
            return image
        except Exception as e:
            print(f"שגיאה בטעינת תמונה {path}: {e}")
            # יצירת משטח ריק במקרה של שגיאה
            surface = pygame.Surface((50, 50))
            surface.fill(COLORS["RED"])
            return surface

    @staticmethod
    def load_sound(path: str) -> pygame.mixer.Sound:
        try:
            return pygame.mixer.Sound(path)
        except Exception as e:
            print(f"שגיאה בטעינת צליל {path}: {e}")
            return None

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("המירוץ למבצר")
        self.clock = pygame.time.Clock()
        self.state = GameState()
        self.load_assets()

    def load_assets(self):
        self.assets = {
            'background': AssetLoader.load_image("pics/Run_Screen_Background.jpg", (SCREEN_WIDTH, SCREEN_HEIGHT)),
            'paths': AssetLoader.load_image("pics/paths.png", (595, SCREEN_HEIGHT)),
            'player': AssetLoader.load_image(self.state.selected_character, (130, 170)),
            'sounds': {
                'go': AssetLoader.load_sound("sounds/GO.mp3"),
                'bg_music': AssetLoader.load_sound("sounds/Running_Background_Music.mp3"),
                'collect': AssetLoader.load_sound("sounds/Collect.mp3"),
                'hit': AssetLoader.load_sound("sounds/Hit_Sound.mp3"),
                'lose': AssetLoader.load_sound("sounds/Lose_Sound.mp3")
            }
        }

    def handle_collisions(self, items_pos: List[Tuple]):
        for item in items_pos[:]:
            if (item[0] == self.state.x_player and 
                item[1] < 480 and item[1] > SCREEN_HEIGHT - 250):
                items_pos.remove(item)
                self.handle_item_collection(item[2][1])

    def handle_item_collection(self, item_type: str):
        if item_type == "mats":
            if self.assets['sounds']['collect']:
                self.assets['sounds']['collect'].play()
            self.state.mats_count += 1
        elif item_type == "obs":
            if self.assets['sounds']['hit']:
                self.assets['sounds']['hit'].play()
            self.state.lives -= 1
        elif item_type == "food" and self.state.lives < 3:
            if self.assets['sounds']['collect']:
                self.assets['sounds']['collect'].play()
            self.state.lives += 1

    def handle_player_movement(self, keys):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= PLAYER_MOVE_DELAY:
            if keys[pygame.K_LEFT] and self.state.path != "Left":
                self.state.path = "Mid" if self.state.path == "Right" else "Left"
                self.last_move_time = current_time
            elif keys[pygame.K_RIGHT] and self.state.path != "Right":
                self.state.path = "Mid" if self.state.path == "Left" else "Right"
                self.last_move_time = current_time
            self.state.x_player = PATH_POSITIONS[self.state.path]

    def update_items(self, items_pos: List[Tuple], current_time: int):
        if current_time - self.last_add_time > ITEM_SPAWN_INTERVAL:
            self.add_new_item(items_pos)
            self.last_add_time = current_time

        # עדכון מיקום הפריטים
        for i in range(len(items_pos)):
            items_pos[i] = (items_pos[i][0], items_pos[i][1] + 2, items_pos[i][2])
        return [item for item in items_pos if item[1] < SCREEN_HEIGHT]

    def run_game(self):
        if self.assets['sounds']['bg_music']:
            self.assets['sounds']['bg_music'].play(-1)
        
        items_pos = []
        self.last_add_time = 0
        self.last_move_time = 0
        time = 0

        while True:
            time += 1
            current_time = pygame.time.get_ticks()

            # טיפול באירועים
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            keys = pygame.key.get_pressed()
            self.handle_player_movement(keys)
            
            # עדכון פריטים
            items_pos = self.update_items(items_pos, current_time)
            self.handle_collisions(items_pos)

            # בדיקת תנאי סיום
            if self.state.lives <= 0:
                if self.assets['sounds']['bg_music']:
                    self.assets['sounds']['bg_music'].stop()
                if self.assets['sounds']['lose']:
                    self.assets['sounds']['lose'].play()
                return 'game_over'

            if self.state.mats_spawned >= 12:
                if self.assets['sounds']['bg_music']:
                    self.assets['sounds']['bg_music'].stop()
                return 'base_screen'

            # ציור
            self.draw_game_screen(items_pos, time)
            pygame.display.flip()
            self.clock.tick(FPS)

    def draw_game_screen(self, items_pos, time):
        # ציור רקע
        self.screen.blit(self.assets['background'], (0, self.state.y_1))
        self.screen.blit(self.assets['background'], (0, self.state.y_2))
        
        # עדכון מיקום רקע
        self.state.y_1 = (self.state.y_1 + 2) % SCREEN_HEIGHT
        self.state.y_2 = (self.state.y_2 + 2) % SCREEN_HEIGHT

        # ציור פריטים
        for pos in items_pos:
            self.screen.blit(pos[2][0], (pos[0], pos[1]))

        # ציור שחקן
        if time % 35 == 0:
            self.assets['player'] = pygame.transform.flip(self.assets['player'], True, False)
        self.screen.blit(self.assets['player'], (self.state.x_player, PLAYER_Y))

        # ציור ממשק משתמש
        self.draw_ui()

    def draw_ui(self):
        font = pygame.font.Font("ganclm_bold-webfont.woff", 50)
        mats_text = font.render(f"10/{self.state.mats_count} םירמוח", True, COLORS["WHITE"])
        lives_text = font.render(f"{self.state.lives} :םייח רפסמ", True, COLORS["WHITE"])
        self.screen.blit(mats_text, (750, 0))
        self.screen.blit(lives_text, (750, 50))

if __name__ == "__main__":
    game = Game()
    game.run_game()