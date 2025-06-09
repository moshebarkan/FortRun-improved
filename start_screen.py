def startScreen():
    """מסך פתיחה מעוצב"""
    try:
        # טעינת רקע
        startBackground = pygame.image.load("pics/Start_Screen_Background.jpg")
        startBackground = pygame.transform.scale(startBackground, (1080,520))
        screen.blit(startBackground,(0,0))

        # טעינת מוזיקת רקע
        bgMusic = pygame.mixer.Sound("sounds/Start_Screen_Background_Muisc.mp3")
        bgMusic.play(-1)

        # הגדרת פונטים
        font1 = pygame.font.Font("ganclm_bold-webfont.woff", 50)
        font2Border = pygame.font.Font("ganclm_bold-webfont.woff", 155)
        font2 = pygame.font.Font("ganclm_bold-webfont.woff", 150)
        font3Border = pygame.font.Font("ganclm_bold-webfont.woff", 205)
        font3 = pygame.font.Font("ganclm_bold-webfont.woff", 200)

        # טקסט כותרת עם גבולות
        titleText1Border = font2Border.render("ץורימה", True, "white")
        titleText1 = font2.render("ץורימה", True, "orange")
        titleText2Border = font3Border.render("רצבמל", True, "brown")
        titleText2 = font3.render("רצבמל", True, "orange")

        # כפתורים
        buttons = {
            "לחתה": (400, 350),
            "תוארוה": (400, 430)
        }

        button_rects = {}
        for text, pos in buttons.items():
            # יצירת כפתור
            btn_rect = pygame.Rect(pos[0], pos[1], 300, 60)
            pygame.draw.rect(screen, "orange", btn_rect, 0, 100)
            pygame.draw.rect(screen, "brown", btn_rect, 5, 100)
            
            # טקסט כפתור עם צל
            btnText = font1.render(text, True, "brown")
            btnTextShadow = font1.render(text, True, "black")
            
            # מיקום טקסט במרכז הכפתור
            text_rect = btnText.get_rect(center=btn_rect.center)
            shadow_rect = text_rect.copy()
            shadow_rect.x += 2
            shadow_rect.y += 3
            
            screen.blit(btnTextShadow, shadow_rect)
            screen.blit(btnText, text_rect)
            
            button_rects[text] = btn_rect

        # הצגת כותרות
        screen.blit(titleText1Border, (275,0))
        screen.blit(titleText1, (285,3))
        screen.blit(titleText2Border, (200,100))
        screen.blit(titleText2, (207,103))

        pygame.display.flip()

        # לולאת אירועים
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    
                    if button_rects["לחתה"].collidepoint(mouse_pos):
                        bgMusic.stop()
                        choose_character_screen()
                        beforeRun()
                    elif button_rects["תוארוה"].collidepoint(mouse_pos):
                        show_instructions()

            # אנימציית hover
            mouse_pos = pygame.mouse.get_pos()
            for text, rect in button_rects.items():
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, "darkorange", rect, 0, 100)
                else:
                    pygame.draw.rect(screen, "orange", rect, 0, 100)
                pygame.draw.rect(screen, "brown", rect, 5, 100)
                
                # רענון טקסט הכפתור
                btnText = font1.render(text, True, "brown")
                btnTextShadow = font1.render(text, True, "black")
                
                text_rect = btnText.get_rect(center=rect.center)
                shadow_rect = text_rect.copy()
                shadow_rect.x += 2
                shadow_rect.y += 3
                
                screen.blit(btnTextShadow, shadow_rect)
                screen.blit(btnText, text_rect)
                
                pygame.display.update(rect)
            
            clock.tick(60)

    except Exception as e:
        print(f"שגיאה במסך הפתיחה: {e}")
        screen.fill("black")
        pygame.display.flip()