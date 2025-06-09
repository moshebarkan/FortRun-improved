import pygame
import random

pygame.init()
clock = pygame.time.Clock()

# הגדרות מסך
screen = pygame.display.set_mode((1080, 520))
screen.fill("black")

pygame.display.set_caption("המרוץ למבצר")  # תוקן
try:
    pygame.display.set_icon(pygame.image.load("pics/game_Icon.png"))
except:
    print("לא ניתן לטעון אייקון")

# משתנים גלובליים
y_1 = -520
y_2 = 0
lives = 3
matsCount = 0
matsSpawned = 0
selected_character = "pics/Runner1.png"  # ברירת מחדל


def game_over_screen():
    screen.fill("black")
    font = pygame.font.Font("ganclm_bold-webfont.woff", 50)

    try:
        background = pygame.image.load("pics/Run_Screen_Background.jpg")
        background = pygame.transform.scale(background, (1080, 520))
        screen.blit(background, (0, 0))
    except:
        pass

    game_over_text = font.render("הפסדת!", True, "red")  # תוקן
    text_rect = game_over_text.get_rect(center=(540, 200))
    screen.blit(game_over_text, text_rect)

    restart_text = font.render("לחץ כדי להתחיל מחדש", True, "white")  # תוקן
    restart_rect = restart_text.get_rect(center=(540, 300))
    screen.blit(restart_text, restart_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                waiting = False
                startScreen()


def startScreen():
    """מסך פתיחה משופר"""
    # טעינת רקע
    try:
        startBackground = pygame.image.load("pics/Start_Screen_Background.jpg")
        startBackground = pygame.transform.scale(startBackground, (1080, 520))
        screen.blit(startBackground, (0, 0))
    except:
        screen.fill("black")

    # טעינת מוזיקת רקע
    try:
        bgMusic = pygame.mixer.Sound("sounds/Start_Screen_Background_Muisc.mp3")
        bgMusic.play(-1)
    except:
        print("לא ניתן לטעון מוזיקת רקע")

    # הגדרת פונטים
    font_title = pygame.font.Font("ganclm_bold-webfont.woff", 100)
    font_buttons = pygame.font.Font("ganclm_bold-webfont.woff", 50)

    # כותרת המשחק עם אפקט צל
    title_text = "המרוץ למבצר"  # תוקן
    title_surface = font_title.render(title_text, True, "orange")
    title_rect = title_surface.get_rect(center=(540, 100))

    title_shadow = font_title.render(title_text, True, "brown")
    shadow_rect = title_rect.copy()
    shadow_rect.x += 4
    shadow_rect.y += 4

    screen.blit(title_shadow, shadow_rect)
    screen