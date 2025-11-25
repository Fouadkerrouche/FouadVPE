import pygame


def afficher_menu(ecran, largeur, hauteur):
   
    titre_font = pygame.font.Font(None, 50)
    option_font = pygame.font.Font(None, 40)
    info_font = pygame.font.Font(None, 25)
    small_font = pygame.font.Font(None, 20)
    
    en_menu = True
    choix = None
    
    
    option1_rect = pygame.Rect(0, 0, 500, 60)
    option1_rect.center = (largeur//2, 200)
    
    option2_rect = pygame.Rect(0, 0, 500, 60)
    option2_rect.center = (largeur//2, 280)
    
    option3_rect = pygame.Rect(0, 0, 500, 60)
    option3_rect.center = (largeur//2, 360)
    
    while en_menu:
       
        mouse_pos = pygame.mouse.get_pos()
        
        ecran.fill((30, 30, 50))
        
        
        titre = titre_font.render("TP VPE - Realite Augmentee", True, (0, 255, 255))
        titre_rect_display = titre.get_rect(center=(largeur//2, 80))
        ecran.blit(titre, titre_rect_display)
        
       
        couleur1 = (255, 200, 0) if option1_rect.collidepoint(mouse_pos) else (255, 255, 255)
        if option1_rect.collidepoint(mouse_pos):
            pygame.draw.rect(ecran, (60, 60, 80), option1_rect, border_radius=10)
        option1 = option_font.render("1 - Utiliser la CAMERA", True, couleur1)
        option1_text_rect = option1.get_rect(center=option1_rect.center)
        ecran.blit(option1, option1_text_rect)
        
        
        couleur2 = (255, 200, 0) if option2_rect.collidepoint(mouse_pos) else (255, 255, 255)
        if option2_rect.collidepoint(mouse_pos):
            pygame.draw.rect(ecran, (60, 60, 80), option2_rect, border_radius=10)
        option2 = option_font.render("2 - Charger une VIDEO", True, couleur2)
        option2_text_rect = option2.get_rect(center=option2_rect.center)
        ecran.blit(option2, option2_text_rect)
        
        
        couleur3 = (255, 200, 0) if option3_rect.collidepoint(mouse_pos) else (255, 255, 255)
        if option3_rect.collidepoint(mouse_pos):
            pygame.draw.rect(ecran, (60, 60, 80), option3_rect, border_radius=10)
        option3 = option_font.render("3 - Fond UNI (sans video)", True, couleur3)
        option3_text_rect = option3.get_rect(center=option3_rect.center)
        ecran.blit(option3, option3_text_rect)
        
        
        info1 = info_font.render("Cliquez sur une option ou appuyez sur 1, 2 ou 3", True, (200, 200, 200))
        info2 = small_font.render("(Option 2 ouvrira une fenetre de selection de fichier)", True, (150, 150, 150))
        info3 = info_font.render("ESC pour quitter", True, (200, 200, 200))
        
        info1_rect = info1.get_rect(center=(largeur//2, 460))
        info2_rect = info2.get_rect(center=(largeur//2, 490))
        info3_rect = info3.get_rect(center=(largeur//2, 530))
        
        ecran.blit(info1, info1_rect)
        ecran.blit(info2, info2_rect)
        ecran.blit(info3, info3_rect)
        
        pygame.display.flip()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'quit'
                elif event.key == pygame.K_1:
                    return 'camera'
                elif event.key == pygame.K_2:
                    return 'video'
                elif event.key == pygame.K_3:
                    return 'none'
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if option1_rect.collidepoint(event.pos):
                        return 'camera'
                    elif option2_rect.collidepoint(event.pos):
                        return 'video'
                    elif option3_rect.collidepoint(event.pos):
                        return 'none'
    
    return choix


def afficher_interface(ecran, largeur, hauteur, source_type, auto_rotation):
    
    font = pygame.font.Font(None, 30)
    font_small = pygame.font.Font(None, 20)
    
    
    pygame.draw.rect(ecran, (0, 0, 0, 180), (5, 5, 300, 90))
    
    texte1 = font.render("ESC : Quitter", True, (255, 255, 255))
    texte2 = font_small.render("ESPACE : Pause/Reprise", True, (255, 255, 255))
    texte3 = font_small.render("Fleches : Rotation", True, (255, 255, 255))
    texte4 = font_small.render("Q/E : Rotation Z | R : Reset", True, (255, 255, 255))
    
    ecran.blit(texte1, (10, 10))
    ecran.blit(texte2, (10, 35))
    ecran.blit(texte3, (10, 55))
    ecran.blit(texte4, (10, 75))
    
   
    if source_type == 'camera':
        source_text = font_small.render("SOURCE : CAMERA", True, (0, 255, 0))
    elif source_type == 'video':
        source_text = font_small.render("SOURCE : VIDEO", True, (0, 200, 255))
    else:
        source_text = font_small.render("SOURCE : FOND UNI", True, (255, 150, 0))
    
    pygame.draw.rect(ecran, (0, 0, 0, 180), (largeur - 210, 5, 205, 30))
    ecran.blit(source_text, (largeur - 205, 10))
    
    
    statut = "AUTO" if auto_rotation else "PAUSE"
    couleur_statut = (0, 255, 0) if auto_rotation else (255, 100, 0)
    texte_statut = font.render(statut, True, couleur_statut)
    pygame.draw.rect(ecran, (0, 0, 0, 180), (largeur - 110, 40, 105, 30))
    ecran.blit(texte_statut, (largeur - 105, 45))