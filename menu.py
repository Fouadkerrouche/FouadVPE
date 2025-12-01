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
        
        
        titre = titre_font.render("TP VPE - Realite Augmente", True, (0, 255, 255))
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
                if event.button == 1:   
                    if option1_rect.collidepoint(event.pos):
                        return 'camera'
                    elif option2_rect.collidepoint(event.pos):
                        return 'video'
                    elif option3_rect.collidepoint(event.pos):
                        return 'none'
    
    return choix



    
    
