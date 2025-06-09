import pygame
import random
import sys
from pygame.locals import *

# הגדרת מצבי משחק
class GameState:
    MAIN_MENU = "main_menu"
    INSTRUCTIONS = "instructions"
    CHARACTER_SELECT = "character_select"
    BEFORE_RUN = "before_run"
    RUNNING = "running"
    GAME_OVER = "game_over"
    BUILDING = "building"

# מחלקת כפתור
class Button:
    def __init__(self, rect, text, font, colors):
        self.rect = rect
        self.text = text
        self.font = font
        self.colors = colors
        self.is_clicked = False
        self.click_time = 0
    
    def draw(self, screen):
        color = self.colors['hover'] if self.is_hovered() else self.colors['normal']
        pygame.draw.rect(screen, color, self.rect, 0, 20)
        pygame.draw.rect(screen, self.colors['border'], self.rect, 3, 20)
        
        text_surface = self.font.render(self.text, True, "white")
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def handle_click(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.click_time > 200:
            self.is_clicked = True
            self.click_time = current_time
            return True
        return False

# אתחול המשחק
pygame.init()
clock = pygame.time.Clock()

# הגדרות מסך
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 520
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
current_state = GameState.MAIN_MENU

# צבעים
COLORS = {
    'normal': "orange",
    'hover': "darkorange",
    'border': "brown",
    'text': "white"
}

def load_assets():
    assets = {
        'images': {},
        'sounds': {},
        'fonts': {}
    }
    
    # טעינת תמונות
    image_paths = {
        'background': "pics/Run_Screen_Background.jpg",
        'icon': "pics/game_Icon.png",
        'paths': "pics/paths.png",
        'runner1': "pics/Runner1.png",
        'runner2': "pics/Runner2.png",
        'before_run': "pics/beforeRunPage.png",
        'building_25': "pics/Building_25%.png",
        'building_50': "pics/Building_50%.png",
        'building_75': "pics/Building_75%.png",
        'building_100': "pics/Building_100%.png"
    }
    
    for key, path in image_paths.items():
        try:
            if 'background' in key:
                size = (SCREEN_WIDTH, SCREEN_HEIGHT)
            elif 'paths' in key:
                size = (595, 520)
            elif 'building' in key:
                size = (500, 400)
            else:
                size = (130, 170)
            assets['images'][key] = pygame.transform.scale(pygame.image.load(path), size)
        except Exception as e:
            print(f"{path} :הנומת ןועטל ןתינ אל - {e}")
            
    # טעינת צלילים
    sound_paths = {
        'background_music': "sounds/Start_Screen_Background_Muisc.mp3",
        'go': "sounds/GO.mp3",
        'collect': "sounds/Collect.mp3",
        'hit': "sounds/Hit_Sound.mp3",
        'lose': "sounds/Lose_Sound.mp3",
        'build': "sounds/Building_Sound.mp3"
    }
    
    for key, path in sound_paths.items():
        try:
            assets['sounds'][key] = pygame.mixer.Sound(path)
        except Exception as e:
            print(f"{path} :לילצ ןועטל ןתינ אל - {e}")
            
    # טעינת פונטים
    assets['fonts'] = {
        'large': pygame.font.Font("ganclm_bold-webfont.woff", 100),
        'medium': pygame.font.Font("ganclm_bold-webfont.woff", 50),
        'small': pygame.font.Font("ganclm_bold-webfont.woff", 30)
    }
    
    return assets

# משתנים גלובליים
y_1 = -520
y_2 = 0
lives = 3
matsCount = 0
matsSpawned = 0
selected_character = "pics/Runner1.png"
assets = load_assets()

pygame.display.set_caption("רצבמל ץורימה")
try:
    pygame.display.set_icon(assets['images']['icon'])
except:
    print("ןוקייא ןועטל ןתינ אל")

def create_menu_buttons():
    buttons = {}
    menu_items = {
        "לחתה": (440, 250),
        "תוארוה": (440, 330),
        "האיצי": (440, 410)
    }
    
    for text, pos in menu_items.items():
        rect = pygame.Rect(pos[0], pos[1], 200, 60)
        buttons[text] = Button(rect, text, assets['fonts']['medium'], COLORS)
    
    return buttons

def game_over_screen():
    global current_state
    screen.blit(assets['images']['background'], (0, 0))
    
    game_over_text = assets['fonts']['medium'].render("!תדספה", True, "red")
    screen.blit(game_over_text, game_over_text.get_rect(center=(540, 200)))
    
    buttons = {
        "שדחמ קחש": Button(pygame.Rect(340, 300, 200, 50), "שדחמ קחש", assets['fonts']['small'], COLORS),
        "טירפתל רוזח": Button(pygame.Rect(540, 300, 200, 50), "טירפתל רוזח", assets['fonts']['small'], COLORS)
    }
    
    for button in buttons.values():
        button.draw(screen)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                for text, button in buttons.items():
                    if button.handle_click():
                        if text == "שדחמ קחש":
                            current_state = GameState.CHARACTER_SELECT
                            choose_character_screen()
                        else:
                            current_state = GameState.MAIN_MENU
                            startScreen()
                        waiting = False

def show_instructions():
    screen.blit(assets['images']['background'], (0, 0))
    
    instructions = [
        "!רצבמל ץורימל םיאבה םיכורב",
        "םילולסמה ןיב עונל ידכ הלאמשו הנימי םיצחב ושמתשה",
        "רצבמה תיינבל היינב ירמוח ופסא",
        "םילושכממ וענמיה",
        "םייח תרזחהל ןוזמ ופסא",
        "רצבמה תא םילשהל ידכ היינב ירמוח 10 ורבצ"
    ]

    y = 100
    for line in instructions:
        text = assets['fonts']['small'].render(line, True, "white")
        screen.blit(text, text.get_rect(center=(540, y)))
        y += 50

    back_button = Button(pygame.Rect(440, 400, 200, 50), "הרזח", assets['fonts']['medium'], COLORS)
    back_button.draw(screen)
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if back_button.handle_click():
                    startScreen()
                    return

def choose_character_screen():
    global selected_character, current_state
    
    screen.blit(assets['images']['background'], (0, 0))
    
    title = assets['fonts']['medium'].render("!ךלש תומדה תא רחב", True, "white")
    screen.blit(title, title.get_rect(center=(540, 100)))
    
    character_buttons = []
    x = 350
    for i, path in enumerate(["pics/Runner1.png", "pics/Runner2.png"]):
        rect = pygame.Rect(x, 150, 130, 170)
        if path == selected_character:
            pygame.draw.rect(screen, "yellow", rect, 3, 15)
        else:
            pygame.draw.rect(screen, "orange", rect, 3, 15)
        
        screen.blit(assets['images'][f'runner{i+1}'], (x, 150))
        character_buttons.append((rect, path))
        x += 250
    
    continue_button = Button(
        pygame.Rect(440, 380, 200, 50),
        "ךשמה",
        assets['fonts']['medium'],
        COLORS
    )
    continue_button.draw(screen)
    
    pygame.display.flip()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for rect, path in character_buttons:
                    if rect.collidepoint(pos):
                        selected_character = path
                        for i, (r, p) in enumerate(character_buttons):
                            if p == selected_character:
                                pygame.draw.rect(screen, "yellow", r, 3, 15)
                            else:
                                pygame.draw.rect(screen, "orange", r, 3, 15)
                        pygame.display.update()
                
                if continue_button.rect.collidepoint(pos):
                    current_state = GameState.BEFORE_RUN
                    beforeRun()
                    running = False

def startScreen():
    global current_state
    
    screen.blit(assets['images']['background'], (0, 0))
    
    try:
        assets['sounds']['background_music'].play(-1)
    except:
        pass

    buttons = create_menu_buttons()
    
    title_text = "רצבמל ץורימה"
    title_shadow = assets['fonts']['large'].render(title_text, True, COLORS['border'])
    title_surface = assets['fonts']['large'].render(title_text, True, COLORS['normal'])
    
    shadow_rect = title_surface.get_rect(center=(544, 104))
    title_rect = title_surface.get_rect(center=(540, 100))
    
    screen.blit(title_shadow, shadow_rect)
    screen.blit(title_surface, title_rect)
    
    pygame.display.flip()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == MOUSEBUTTONDOWN:
                for text, button in buttons.items():
                    if button.handle_click():
                        if text == "קחשמ לחתה":
                            try:
                                assets['sounds']['background_music'].stop()
                            except:
                                pass
                            current_state = GameState.CHARACTER_SELECT
                            choose_character_screen()
                            running = False
                        elif text == "תוארוה":
                            current_state = GameState.INSTRUCTIONS
                            show_instructions()
                            running = False
                        elif text == "האיצי":
                            pygame.quit()
                            sys.exit()
        
        for button in buttons.values():
            button.draw(screen)
        
        pygame.display.update()
        clock.tick(60)


def beforeRun():
    global selected_character, current_state

    screen.blit(assets['images']['background'], (0, 0))
    screen.blit(assets['images']['paths'], (260, 0))
    screen.blit(assets['images']['before_run'], (0, 0))

    start_button = Button(
        pygame.Rect(440, 380, 200, 50),
        "לחתה",
        assets['fonts']['medium'],
        COLORS
    )
    start_button.draw(screen)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if start_button.handle_click():
                    current_state = GameState.RUNNING
                    runScreen(1 if selected_character == "pics/Runner2.png" else 0)
        pygame.display.flip()


def baseScreen():
    global current_state
    screen.blit(assets['images']['background'], (0, 0))

    try:
        assets['sounds']['build'].play()
    except:
        pass

    title = assets['fonts']['medium'].render("!רצבמה תא םינוב", True, "white")
    screen.blit(title, (400, 50))

    building_stages = ['building_25', 'building_50', 'building_75', 'building_100']

    for stage in building_stages:
        screen.blit(assets['images']['background'], (0, 0))
        screen.blit(title, (400, 50))
        screen.blit(assets['images'][stage], (290, 100))
        pygame.display.flip()
        pygame.time.wait(800)

    finish_text = assets['fonts']['medium'].render("!החלצהב םלשוה רצבמה", True, "white")
    screen.blit(finish_text, (350, 450))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
                waiting = False
                pygame.quit()
                sys.exit()


def runScreen(gen):
    global y_1, y_2, lives, matsSpawned, matsCount, current_state

    try:
        assets['sounds']['go'].play()
        assets['sounds']['background_music'].play(-1)
    except:
        pass

    item_images = load_game_items()
    items_pos = []
    add_interval = 700
    last_add_time = 0
    x_player = 495
    path = "Mid"
    time = 0

    def add_new_item():
        global matsSpawned
        item_x = random.choice([300, 495, 690])
        item_y = -100
        item_image = random.choice(item_images)
        items_pos.append((item_x, item_y, item_image))
        if item_image[1] == "mats":
            matsSpawned += 1

    def colideHappen(rightX):
        global lives, matsCount
        for item in items_pos[:]:
            if item[0] == rightX and item[1] < 480 and item[1] > 520 - 250:
                items_pos.remove(item)
                if item[2][1] == "mats":
                    assets['sounds']['collect'].play()
                    matsCount += 1
                if item[2][1] == "obs":
                    assets['sounds']['hit'].play()
                    lives -= 1
                if item[2][1] == "food" and lives < 3:
                    assets['sounds']['collect'].play()
                    lives += 1

    while True:
        time += 1
        screen.blit(assets['images']['background'], (0, y_1))
        screen.blit(assets['images']['background'], (0, y_2))
        screen.blit(assets['images']['paths'], (260, y_1))
        screen.blit(assets['images']['paths'], (257, y_2))

        # הצגת מידע על המסך
        needs = assets['fonts']['medium'].render(f"10/{matsCount} םירמוח", True, "white")
        livesCheck = assets['fonts']['medium'].render(f"{lives} :םייח רפסמ", True, "white")
        screen.blit(needs, (750, 0))
        screen.blit(livesCheck, (750, 50))

        # עדכון מיקום רקע
        y_1 += 4
        y_2 += 4
        if y_1 >= 520:
            y_1 = -520
        if y_2 >= 520:
            y_2 = -520

        # עדכון מיקום שחקן
        if path == "Mid":
            x_player = 495
        elif path == "Left":
            x_player = 300
        else:
            x_player = 690

        screen.blit(assets['images'][f'runner{gen + 1}'], (x_player, 320))
        if time % 35 == 0:
            assets['images'][f'runner{gen + 1}'] = pygame.transform.flip(assets['images'][f'runner{gen + 1}'], True,
                                                                         False)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # בדיקת מקשים
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and path != "Left":
            if path == "Right":
                path = "Mid"
            elif path == "Mid":
                path = "Left"
        elif keys[K_RIGHT] and path != "Right":
            if path == "Left":
                path = "Mid"
            elif path == "Mid":
                path = "Right"

        # הוספת פריטים חדשים
        current_time = pygame.time.get_ticks()
        if current_time - last_add_time > add_interval:
            add_new_item()
            last_add_time = current_time

        # עדכון מיקום פריטים
        for i in range(len(items_pos)):
            items_pos[i] = (items_pos[i][0], items_pos[i][1] + 4, items_pos[i][2])
        items_pos = [item for item in items_pos if item[1] < 520]

        # בדיקת סיום משחק
        if matsSpawned < 12:
            for pos in items_pos:
                screen.blit(pos[2][0], (pos[0], pos[1]))
        else:
            try:
                assets['sounds']['background_music'].stop()
            except:
                pass
            current_state = GameState.BUILDING
            baseScreen()

        if lives == 0:
            try:
                assets['sounds']['background_music'].stop()
                assets['sounds']['lose'].play()
            except:
                pass
            current_state = GameState.GAME_OVER
            game_over_screen()
            return

        # בדיקת התנגשויות
        if x_player == 300:
            colideHappen(300)
        elif x_player == 495:
            colideHappen(495)
        else:
            colideHappen(690)

        pygame.display.flip()
        clock.tick(60)


def load_game_items():
    item_types = {
        'food': [f"pics/needs/life/food{i}.png" for i in range(1, 8)] + ["pics/needs/life/water.png"],
        'mats': ["pics/needs/mats/bricks.png", "pics/needs/mats/metal.png", "pics/needs/mats/wood.png"] * 2,
        'obs': ["pics/obstacles/clothes_obsticle.png", "pics/obstacles/sand_obsticle.png",
                "pics/obstacles/stone_obsticle.png"] * 2
    }

    items = []
    for item_type, paths in item_types.items():
        for path in paths:
            try:
                img = pygame.transform.scale(pygame.image.load(path), (120, 120))
                items.append((img, item_type))
            except:
                print(f"{path} :הנומת ןועטל ןתינ אל")

    return items


# התחלת המשחק
startScreen()



