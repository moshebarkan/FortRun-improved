import pygame
pygame.init()
import random
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1080,520))
screen.fill("black")

pygame.display.set_caption("המירוץ למבצר")
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
    
    # טעינת תמונת הרקע
    try:
        background = pygame.image.load("pics/Run_Screen_Background.jpg")
        background = pygame.transform.scale(background, (1080, 520))
        screen.blit(background, (0, 0))
    except:
        pass

    # הודעת Game Over
    game_over_text = font.render("!תדספה", True, "red")
    text_rect = game_over_text.get_rect(center=(540, 200))
    screen.blit(game_over_text, text_rect)
    
    # הודעת לחץ להתחלה מחדש
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
                startScreen()  # חזרה למסך הפתיחה

def baseScreen():
    screen.fill("black")
    font = pygame.font.Font("ganclm_bold-webfont.woff", 50)
    
    # טעינת תמונת הרקע
    background = pygame.image.load("pics/Run_Screen_Background.jpg")
    background = pygame.transform.scale(background, (1080,520))
    screen.blit(background, (0,0))
    
    # טעינת סאונד בנייה
    build_sound = pygame.mixer.Sound("sounds/Building_Sound.mp3")
    build_sound.play()
    
    # תמונות שלבי הבנייה
    construction_stages = [
        "pics/Building_25%.png",
        "pics/Building_50%.png",
        "pics/Building_75%.png",
        "pics/Building_100%.png",
    ]
    
    # כותרת
    title = font.render("!רצבמה תא םינוב", True, "white")
    screen.blit(title, (400, 50))
    
    # אנימציית בנייה
    for stage in construction_stages:
        # מציג את שלב הבנייה הנוכחי
        construction = pygame.image.load(stage)
        construction = pygame.transform.scale(construction, (500, 400))
        screen.blit(background, (0,0))  # מנקה את המסך עם הרקע
        screen.blit(title, (400, 50))   # מציג את הכותרת שוב
        screen.blit(construction, (290, 100))  # מציג את שלב הבנייה
        pygame.display.flip()
        pygame.time.wait(1000)  # ממתין שנייה בין כל שלב
    
    # הודעת סיום
    finish_text = font.render("!החלצהב םלשוה רצבמה", True, "white")
    screen.blit(finish_text, (350, 450))
    pygame.display.flip()
    
    # ממתין ללחיצה לסיום
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
    
    # טעינת הרקע
    try:
        background = pygame.image.load("pics/Run_Screen_Background.jpg")
        background = pygame.transform.scale(background, (1080, 520))
        screen.blit(background, (0, 0))
    except:
        pass  # אם אין רקע, נמשיך עם רקע שחור
    
    font = pygame.font.Font("ganclm_bold-webfont.woff", 50)
    
    # האפשרויות לבחירה
    character_options = [
        ("pics/Runner1.png", "1 תומד"),
        ("pics/Runner2.png", "2 תומד")
    ]
    
    buttons = []
    x = 350
    
    title = font.render("!ךלש תומדה תא רחב", True, "white")
    title_rect = title.get_rect(center=(540, 100))
    screen.blit(title, title_rect)
    
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
            print(f"Error loading image {img_path}: {e}")
    
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

def startScreen():
    startBackground = pygame.image.load("pics/Start_Screen_Background.jpg")
    startBackground = pygame.transform.scale(startBackground, (1080,520))
    screen.blit(startBackground,(0,0))

    bgMuisc = pygame.mixer.Sound("sounds/Start_Screen_Background_Muisc.mp3")
    bgMuisc.play(-1)

    font1 = pygame.font.Font("ganclm_bold-webfont.woff", 50)
    font2Border = pygame.font.Font("ganclm_bold-webfont.woff", 155)
    font2 = pygame.font.Font("ganclm_bold-webfont.woff", 150)
    font3Border = pygame.font.Font("ganclm_bold-webfont.woff", 205)
    font3 = pygame.font.Font("ganclm_bold-webfont.woff", 200)

    titleText1Border = font2Border.render("ץורימה", True, "white")
    titleText1 = font2.render("ץורימה", True, "orange")
    titleText2Border = font3Border.render("רצבמל", True, "brown")
    titleText2 = font3.render("רצבמל", True, "orange")

    startBtnText = font1.render("לחתה", True, "brown")
    startBtnTextShadow = font1.render("לחתה", True, "black")
    btnRect = pygame.Rect(400,350, 300,100)
    pygame.draw.rect(screen,"orange", btnRect,0,100)
    pygame.draw.rect(screen,"brown", (400,350, 300,100),5,100)

    screen.blit(titleText1Border, (275,0))
    screen.blit(titleText1, (285,3))
    screen.blit(titleText2Border, (200,100))
    screen.blit(titleText2, (207,103))
    screen.blit(startBtnTextShadow,(479,375))
    screen.blit(startBtnText,(477,372))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnRect.collidepoint(event.pos):
                    bgMuisc.stop()
                    choose_character_screen()
                    beforeRun()
        pygame.display.flip()

def beforeRun():
    global selected_character
    font = pygame.font.Font("ganclm_bold-webfont.woff", 50)
    runBackground1 = pygame.image.load("pics/Run_Screen_Background.jpg")
    runBackground1 = pygame.transform.scale(runBackground1, (1080,520))
    paths1 = pygame.image.load("pics/paths.png")
    paths1 = pygame.transform.scale(paths1, (595,520))
    screen.blit(runBackground1,(0,0))
    screen.blit(paths1,(260,0))
    window = pygame.image.load("pics/beforeRunPage.png")
    window = pygame.transform.scale(window,(1080,500))
    screen.blit(window, (0,0))
    
    # כפתור התחל במקום כפתורי בן/בת
    btn_start = pygame.draw.rect(screen, "orange", (440,380, 200,50),0,100)
    text_start = font.render("לחתה", True, "white")
    screen.blit(text_start, (495,380))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if btn_start.collidepoint(mouse_pos):
                    if selected_character == "pics/Runner1.png":
                        runScreen(0)  # מתחיל את המשחק כבן
                    else:
                        runScreen(1)  # מתחיל את המשחק כבת
        pygame.display.flip()

def runScreen(gen):
    global selected_character, y_1, y_2, lives, matsSpawned, matsCount  
    
    go = pygame.mixer.Sound("sounds/GO.mp3")
    go.play()
    bgMusic = pygame.mixer.Sound("sounds/Running_Background_Music.mp3")
    bgMusic.play(-1)
    lose = pygame.mixer.Sound("sounds/Lose_Sound.mp3")
    collectSound = pygame.mixer.Sound("sounds/Collect.mp3")
    hitSound = pygame.mixer.Sound("sounds/Hit_Sound.mp3")
    
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
        
        (pygame.image.load("pics/obstacles/clothes_obsticle.png"),"obs"),
        (pygame.image.load("pics/obstacles/sand_obsticle.png"),"obs"),
        (pygame.image.load("pics/obstacles/stone_obsticle.png"),"obs"),
        (pygame.image.load("pics/obstacles/clothes_obsticle.png"),"obs"),
        (pygame.image.load("pics/obstacles/sand_obsticle.png"),"obs"),
        (pygame.image.load("pics/obstacles/stone_obsticle.png"),"obs"),
    ]

    item_images = [(pygame.transform.scale(image[0], (120, 120)), image[1]) for image in item_images]
    
    items_pos = []
    add_interval = 1000
    last_add_time = 0
    last_move_time = 0  # משתנה חדש לעקוב אחרי הזמן האחרון שבו הדמות זזה

    def add_new_item():
        global matsSpawned
        item_x = random.choice([300,495,690])
        item_y = -100
        item_image = random.choice(item_images)
        items_pos.append((item_x, item_y, item_image))
        if item_image[1] == "mats":
            matsSpawned += 1

    x_player = 495
    path = "Mid"

    runBackground1 = pygame.image.load("pics/Run_Screen_Background.jpg")
    runBackground1 = pygame.transform.scale(runBackground1, (1080,520))
    runBackground2 = pygame.image.load("pics/Run_Screen_Background.jpg")
    runBackground2 = pygame.transform.scale(runBackground2, (1080,520))

    paths1 = pygame.image.load("pics/paths.png")
    paths1 = pygame.transform.scale(paths1, (595,520))
    paths2 = pygame.image.load("pics/paths.png")
    paths2 = pygame.transform.scale(paths2, (600,520))

    # טעינת הדמות שנבחרה
    player = pygame.image.load(selected_character)
    player = pygame.transform.scale(player, (130,170))

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
        screen.blit(runBackground1,(0,y_1))
        screen.blit(runBackground2,(0,y_2))
        screen.blit(paths1,(260,y_1))
        screen.blit(paths2,(257,y_2))
        needs = font.render(f"10/{matsCount} םירמוח", True, "white")
        livesCheck = font.render(f"{lives} :םייח רפסמ", True, "white")
        screen.blit(needs, (750,0))
        screen.blit(livesCheck, (750,50))
        y_1 += 2
        y_2 += 2
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

        screen.blit(player, (x_player,320))
        if time % 35 == 0:
            player = pygame.transform.flip(player, True, False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        current_time = pygame.time.get_ticks()
        
        # בדיקה אם עבר מספיק זמן מאז התזוזה האחרונה
        if current_time - last_move_time >= 150:  # 150 אלפיות שנייה = 0.15 שניות
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and path != "Left":
                if path == "Right":
                    path = "Mid"
                elif path == "Mid":
                    path = "Left"
                last_move_time = current_time  # עדכון זמן התזוזה האחרונה
            elif keys[pygame.K_RIGHT] and path != "Right":
                if path == "Left":
                    path = "Mid"
                elif path == "Mid":
                    path = "Right"
                last_move_time = current_time  # עדכון זמן התזוזה האחרונה

        clock.tick(600)
 
        if current_time - last_add_time > add_interval:
            add_new_item()
            last_add_time = current_time

        for i in range(len(items_pos)):
            items_pos[i] = (items_pos[i][0], items_pos[i][1] + 2, items_pos[i][2])
            
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

startScreen()