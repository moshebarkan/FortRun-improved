import pygame
import random

pygame.init()
clock = pygame.time.Clock()

# הגדרות מסך
screen = pygame.display.set_mode((1080, 520))
screen.fill("black")

pygame.display.set_caption("fortrun")
pygame.display.set_icon(pygame.image.load("pics/game_Icon.png"))

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

    game_over_text = font.render("!תדספה", True, "red")
    text_rect = game_over_text.get_rect(center=(540, 200))
    screen.blit(game_over_text, text_rect)

    restart_text = font.render("שדחמ ליחתהל ידכ ץחל", True, "white")
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
    try:
        startBackground = pygame.image.load("pics/Start_Screen_Background.jpg")
        startBackground = pygame.transform.scale(startBackground, (1080, 520))
        screen.blit(startBackground, (0, 0))
    except:
        screen.fill("black")

    try:
        bgMusic = pygame.mixer.Sound("sounds/Start_Screen_Background_Muisc.mp3")
        bgMusic.play(-1)
    except:
        print("עקר תקיזומ ןועטל ןתינ אל")

    # טעינת התמונה של הלוגו
    icon = pygame.image.load("pics/game_Icon.png")
    icon = pygame.transform.scale(icon, (750, 300))
    screen.blit(icon, (-10, 60))

    # הגדרות העמוד - הזזה ימינה
    pillar_width = 160  # צר יותר מהכפתורים
    button_start_y = 180  # התחלת אזור הכפתורים
    button_spacing = 20  # רווח בין הכפתורים
    right_margin = 100  # מרווח מהצד הימני של המסך

    # הגדרות הכפתורים
    button_heights = {
        "לחתה ": 80,
        "תוארוה": 70,
        "תורדגה": 60,
        "האיצי": 50
    }

    # חישוב גובה העמוד בהתאם לכפתורים
    total_buttons_height = sum(button_heights.values()) + (len(button_heights) - 1) * button_spacing
    pillar_height = total_buttons_height + 40  # תוספת שוליים

    # מיקום חדש לעמוד - מימין
    pillar_x = 1080 - pillar_width - right_margin
    pillar_y = button_start_y - 20

    # ציור הצל של העמוד
    shadow_surface = pygame.Surface((pillar_width, pillar_height))
    shadow_surface.fill((30, 30, 30))
    shadow_surface.set_alpha(80)
    screen.blit(shadow_surface, (pillar_x + 8, pillar_y + 8))

    # ציור העמוד העץ
    pillar_surface = pygame.Surface((pillar_width, pillar_height))
    wood_color = (139, 69, 19)
    pillar_surface.fill(wood_color)

    # הוספת טקסטורת עץ
    for i in range(0, pillar_height, 15):
        wood_line_color = (101, 67, 33)
        pygame.draw.line(pillar_surface, wood_line_color, (0, i), (pillar_width, i), 2)
        for j in range(5):
            x = random.randint(0, pillar_width)
            pygame.draw.circle(pillar_surface, wood_line_color, (x, i), 2)

    pygame.draw.rect(pillar_surface, (101, 67, 33), (0, 0, pillar_width, pillar_height), 5)
    screen.blit(pillar_surface, (pillar_x, pillar_y))

    font_buttons = pygame.font.Font("ganclm_bold-webfont.woff", 50)

    # סידור הכפתורים
    button_width_base = 300
    current_y = button_start_y
    buttons = {}

    for text, height in button_heights.items():
        width = button_width_base - (80 - height)
        # מיקום חדש לכפתורים - מימין
        x = pillar_x - (width - pillar_width) // 2
        buttons[text] = (x, current_y, width, height)
        current_y += height + button_spacing

    button_rects = {}

    # יצירת הכפתורים
    for text, (x, y, width, height) in buttons.items():
        btn_rect = pygame.Rect(x, y, width, height)

        # צל לכפתור
        shadow_rect = btn_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(screen, (60, 30, 0), shadow_rect, 0, 15)

        # רקע עץ לכפתור
        button_surface = pygame.Surface((width, height))
        wood_button_color = (205, 133, 63)
        button_surface.fill(wood_button_color)

        # טקסטורת עץ לכפתור
        for i in range(0, height, 5):
            wood_line_color = (139, 69, 19)
            pygame.draw.line(button_surface, wood_line_color, (0, i), (width, i), 1)

        screen.blit(button_surface, btn_rect)
        pygame.draw.rect(screen, (101, 67, 33), btn_rect, 3, 15)

        # הטקסט על הכפתור
        text_surface = font_buttons.render(text, True, "white")
        text_rect = text_surface.get_rect(center=btn_rect.center)
        screen.blit(text_surface, text_rect)

        button_rects[text] = btn_rect

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if button_rects["לחתה "].collidepoint(mouse_pos):
                    try:
                        bgMusic.stop()
                    except:
                        pass
                    choose_character_screen()
                    beforeRun()

                elif button_rects["תוארוה"].collidepoint(mouse_pos):
                    show_instructions()

                elif button_rects["האיצי"].collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

                elif button_rects["תורדגה"].collidepoint(mouse_pos):
                    pass

        # אפקט hover על הכפתורים
        mouse_pos = pygame.mouse.get_pos()
        for text, rect in button_rects.items():
            shadow_rect = rect.copy()
            shadow_rect.x += 4
            shadow_rect.y += 4
            pygame.draw.rect(screen, (60, 30, 0), shadow_rect, 0, 15)

            button_surface = pygame.Surface((rect.width, rect.height))
            if rect.collidepoint(mouse_pos):
                wood_color = (222, 184, 135)
            else:
                wood_color = (205, 133, 63)

            button_surface.fill(wood_color)

            for i in range(0, rect.height, 5):
                wood_line_color = (139, 69, 19)
                pygame.draw.line(button_surface, wood_line_color, (0, i), (rect.width, i), 1)

            screen.blit(button_surface, rect)
            pygame.draw.rect(screen, (101, 67, 33), rect, 3, 15)

            text_surface = font_buttons.render(text, True, "white")
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

            pygame.display.update(rect)
            pygame.display.update(shadow_rect)

        clock.tick(60)


def show_instructions():
    screen.fill("black")
    font = pygame.font.Font("ganclm_bold-webfont.woff", 30)

    try:
        background = pygame.image.load("pics/Run_Screen_Background.jpg")
        background = pygame.transform.scale(background, (1080, 520))
        screen.blit(background, (0, 0))
    except:
        pass

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
        text = font.render(line, True, "white")
        text_rect = text.get_rect(center=(540, y))
        screen.blit(text, text_rect)
        y += 50

    back_btn = pygame.draw.rect(screen, "orange", (440, 400, 200, 50), 0, 100)
    pygame.draw.rect(screen, "brown", (440, 400, 200, 50), 5, 100)
    back_text = font.render("הרזח", True, "white")
    back_rect = back_text.get_rect(center=(540, 425))
    screen.blit(back_text, back_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    startScreen()

def baseScreen():
    screen.fill("black")
    font = pygame.font.Font("ganclm_bold-webfont.woff", 50)

    try:
        background = pygame.image.load("pics/Run_Screen_Background.jpg")
        background = pygame.transform.scale(background, (1080, 520))
        screen.blit(background, (0, 0))
    except:
        pass

    try:
        build_sound = pygame.mixer.Sound("sounds/Building_Sound.mp3")
        build_sound.play()
    except:
        print("היינב לילצ ןועטל ןתינ אל")

    construction_stages = [
        "pics/Building_25%.png",
        "pics/Building_50%.png",
        "pics/Building_75%.png",
        "pics/Building_100%.png",
    ]

    title = font.render("!רצבמה תא םינוב", True, "white")
    screen.blit(title, (400, 50))

    for stage in construction_stages:
        try:
            construction = pygame.image.load(stage)
            construction = pygame.transform.scale(construction, (500, 400))
            screen.blit(background, (0, 0))
            screen.blit(title, (400, 50))
            screen.blit(construction, (290, 100))
            pygame.display.flip()
            pygame.time.wait(800)
        except:
            print(f"{stage} :הנומת ןועטל ןתינ אל")

    finish_text = font.render("!החלצהב םלשוה רצבמה", True, "white")
    screen.blit(finish_text, (350, 450))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                waiting = False

    pygame.quit()

def choose_character_screen():
    global selected_character
    screen.fill("black")

    try:
        background = pygame.image.load("pics/Run_Screen_Background.jpg")
        background = pygame.transform.scale(background, (1080, 520))
        screen.blit(background, (0, 0))
    except:
        pass

    font = pygame.font.Font("ganclm_bold-webfont.woff", 50)

    character_options = [
        ("pics/Runner1.png", "1 תומד"),
        ("pics/Runner2.png", "2 תומד")
    ]

    title = font.render("!ךלש תומדה תא רחב", True, "white")
    title_rect = title.get_rect(center=(540, 100))
    screen.blit(title, title_rect)

    buttons = []
    x = 350
    for img_path, label in character_options:
        try:
            img = pygame.image.load(img_path)
            img = pygame.transform.scale(img, (130, 170))
            screen.blit(img, (x, 150))

            btn = pygame.draw.rect(screen, "orange", (x, 150, 130, 170), 5, 15)

            text = font.render(label, True, "white")
            text_rect = text.get_rect(center=(x + 65, 370))
            screen.blit(text, text_rect)

            buttons.append((btn, img_path))
            x += 250

        except Exception as e:
            print(f"{e} :{img_path} הנומת תניעטב האיגש")

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn, path in buttons:
                    if btn.collidepoint(pos):
                        selected_character = path
                        running = False
                        return

def beforeRun():
    global selected_character
    try:
        runBackground1 = pygame.image.load("pics/Run_Screen_Background.jpg")
        runBackground1 = pygame.transform.scale(runBackground1, (1080, 520))
        paths1 = pygame.image.load("pics/paths.png")
        paths1 = pygame.transform.scale(paths1, (595, 520))
        screen.blit(runBackground1, (0, 0))
        screen.blit(paths1, (260, 0))
        window = pygame.image.load("pics/beforeRunPage.png")
        window = pygame.transform.scale(window, (1080, 500))
        screen.blit(window, (0, 0))
    except Exception as e:
        print(f"{e} :תונומת תניעטב האיגש")
        screen.fill("black")

    font = pygame.font.Font("ganclm_bold-webfont.woff", 50)
    btn_start = pygame.draw.rect(screen, "orange", (440, 380, 200, 50), 0, 100)
    text_start = font.render("לחתה", True, "white")
    screen.blit(text_start, (495, 380))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if btn_start.collidepoint(mouse_pos):
                    if selected_character == "pics/Runner1.png":
                        runScreen(0)
                    else:
                        runScreen(1)
        pygame.display.flip()

def runScreen(gen):
    global y_1, y_2, lives, matsSpawned, matsCount

    try:
        go = pygame.mixer.Sound("sounds/GO.mp3")
        go.play()
        bgMusic = pygame.mixer.Sound("sounds/Running_Background_Music.mp3")
        bgMusic.play(-1)
        lose = pygame.mixer.Sound("sounds/Lose_Sound.mp3")
        collectSound = pygame.mixer.Sound("sounds/Collect.mp3")
        hitSound = pygame.mixer.Sound("sounds/Hit_Sound.mp3")
    except Exception as e:
        print(f"{e} :םילילצ תניעטב האיגש")

    font = pygame.font.Font("ganclm_bold-webfont.woff", 50)

    item_images = [
        (pygame.image.load("pics/needs/life/food1.png"), "food"),
        (pygame.image.load("pics/needs/life/food2.png"), "food"),
        (pygame.image.load("pics/needs/life/food3.png"), "food"),
        (pygame.image.load("pics/needs/life/food4.png"), "food"),
        (pygame.image.load("pics/needs/life/food5.png"), "food"),
        (pygame.image.load("pics/needs/life/food6.png"), "food"),
        (pygame.image.load("pics/needs/life/food7.png"), "food"),
        (pygame.image.load("pics/needs/life/water.png"), "food"),
        (pygame.image.load("pics/needs/mats/bricks.png"), "mats"),
        (pygame.image.load("pics/needs/mats/metal.png"), "mats"),
        (pygame.image.load("pics/needs/mats/wood.png"), "mats"),
        (pygame.image.load("pics/needs/mats/bricks.png"), "mats"),
        (pygame.image.load("pics/needs/mats/metal.png"), "mats"),
        (pygame.image.load("pics/needs/mats/wood.png"), "mats"),
        (pygame.image.load("pics/obstacles/clothes_obsticle.png"), "obs"),
        (pygame.image.load("pics/obstacles/sand_obsticle.png"), "obs"),
        (pygame.image.load("pics/obstacles/stone_obsticle.png"), "obs"),
        (pygame.image.load("pics/obstacles/clothes_obsticle.png"), "obs"),
        (pygame.image.load("pics/obstacles/sand_obsticle.png"), "obs"),
        (pygame.image.load("pics/obstacles/stone_obsticle.png"), "obs"),
    ]

    item_images = [(pygame.transform.scale(image[0], (120, 120)), image[1]) for image in item_images]

    items_pos = []
    add_interval = 700
    last_add_time = 0

    def add_new_item():
        global matsSpawned
        item_x = random.choice([300, 495, 690])
        item_y = -100
        item_image = random.choice(item_images)
        items_pos.append((item_x, item_y, item_image))
        if item_image[1] == "mats":
            matsSpawned += 1

    x_player = 495
    path = "Mid"

    try:
        runBackground1 = pygame.image.load("pics/Run_Screen_Background.jpg")
        runBackground1 = pygame.transform.scale(runBackground1, (1080, 520))
        runBackground2 = pygame.image.load("pics/Run_Screen_Background.jpg")
        runBackground2 = pygame.transform.scale(runBackground2, (1080, 520))
        paths1 = pygame.image.load("pics/paths.png")
        paths1 = pygame.transform.scale(paths1, (595, 520))
        paths2 = pygame.image.load("pics/paths.png")
        paths2 = pygame.transform.scale(paths2, (600, 520))
        player = pygame.image.load(selected_character)
        player = pygame.transform.scale(player, (130, 170))
    except Exception as e:
        print(f"{e} :תונומת תניעטב האיגש")
        return

    time = 0

    def colideHappen(rightX):
        global lives, matsCount
        for item in items_pos[:]:
            if item[0] == rightX and item[1] < 480 and item[1] > 520 - 250:
                items_pos.remove(item)
                if item[2][1] == "mats":
                    collectSound.play()
                    matsCount += 1
                if item[2][1] == "obs":
                    hitSound.play()
                    lives -= 1
                if item[2][1] == "food" and lives < 3:
                    collectSound.play()
                    lives += 1

    while True:
        time += 1
        screen.blit(runBackground1, (0, y_1))
        screen.blit(runBackground2, (0, y_2))
        screen.blit(paths1, (260, y_1))
        screen.blit(paths2, (257, y_2))

        needs = font.render(f"10/{matsCount} םירמוח", True, "white")
        livesCheck = font.render(f"{lives} :םייח רפסמ", True, "white")
        screen.blit(needs, (750, 0))
        screen.blit(livesCheck, (750, 50))

        y_1 += 4
        y_2 += 4
        if y_1 >= 520:
            y_1 = -520
        if y_2 >= 520:
            y_2 = -520

        if path == "Mid":
            x_player = 495
        elif path == "Left":
            x_player = 300
        else:
            x_player = 690

        screen.blit(player, (x_player, 320))
        if time % 35 == 0:
            player = pygame.transform.flip(player, True, False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        current_time = pygame.time.get_ticks()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and path != "Left":
            if path == "Right":
                path = "Mid"
            elif path == "Mid":
                path = "Left"
        elif keys[pygame.K_RIGHT] and path != "Right":
            if path == "Left":
                path = "Mid"
            elif path == "Mid":
                path = "Right"

        if current_time - last_add_time > add_interval:
            add_new_item()
            last_add_time = current_time

        for i in range(len(items_pos)):
            items_pos[i] = (items_pos[i][0], items_pos[i][1] + 4, items_pos[i][2])

        items_pos = [item for item in items_pos if item[1] < 520]

        if matsSpawned < 12:
            for pos in items_pos:
                screen.blit(pos[2][0], (pos[0], pos[1]))
        else:
            bgMusic.stop()
            baseScreen()

        if lives == 0:
            bgMusic.stop()
            lose.play()
            game_over_screen()

        if x_player == 300:
            colideHappen(300)
        elif x_player == 495:
            colideHappen(495)
        else:
            colideHappen(690)

        pygame.display.flip()
        clock.tick(60)

# התחלת המשחק
startScreen()