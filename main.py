import pygame
import cv2
from camera import Camera
from cube import Cube
from video_capture import VideoCapture, choisir_fichier_video
from menu import afficher_menu, afficher_interface



LARGEUR = 800
HAUTEUR = 600
FPS = 60


def main():
   
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("TP VPE - Realite Augmentee")
    horloge = pygame.time.Clock()
    
    font = pygame.font.Font(None, 30)
    

    
    choix = afficher_menu(ecran, LARGEUR, HAUTEUR)
    
    if choix == 'quit':
        pygame.quit()
        return
    
   
    video_capture = None
    
    if choix == 'camera':
        video_capture = VideoCapture(source_type='camera')
    
    elif choix == 'video':
        chemin_video = choisir_fichier_video()
        video_capture = VideoCapture(source_type='video', source_path=chemin_video)
    
    else:  
        video_capture = VideoCapture(source_type='none')
    
    
    source_type = video_capture.source_type
    
    
   
   
    camera = Camera(
        largeur=LARGEUR,
        hauteur=HAUTEUR,
        focale=500
    )
    
    
    cube = Cube(taille=1.0)
    cube.positionner(0, 0, 5)
    
   
    
    rotation_x = 0.02
    rotation_y = 0.03
    auto_rotation = True
    
    
    
    en_cours = True
    frame_count = 0
    
   
    
    while en_cours:
        
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    en_cours = False
                elif event.key == pygame.K_SPACE:
                    auto_rotation = not auto_rotation
                elif event.key == pygame.K_r:
                    cube.rotation_x = 0
                    cube.rotation_y = 0
                    cube.rotation_z = 0
        
       
        touches = pygame.key.get_pressed()
        if touches[pygame.K_UP]:
            cube.rotation_x += 0.05
        if touches[pygame.K_DOWN]:
            cube.rotation_x -= 0.05
        if touches[pygame.K_LEFT]:
            cube.rotation_y -= 0.05
        if touches[pygame.K_RIGHT]:
            cube.rotation_y += 0.05
        if touches[pygame.K_q]:
            cube.rotation_z += 0.05
        if touches[pygame.K_e]:
            cube.rotation_z -= 0.05
        
        
        
        
        if auto_rotation:
            cube.rotation_x += rotation_x
            cube.rotation_y += rotation_y
        
        
        
        
        if source_type != 'none':
            frame_surface = video_capture.read_frame(LARGEUR, HAUTEUR)
            
            if frame_surface is not None:
                ecran.blit(frame_surface, (0, 0))
            else:
                
                ecran.fill((20, 20, 40))
        else:
            
            ecran.fill((20, 20, 40))
        
        
        cube.afficher(ecran, camera)
        
        
        afficher_interface(ecran, LARGEUR, HAUTEUR, source_type, auto_rotation)
        
       
        
        pygame.display.flip()
        horloge.tick(FPS)
        frame_count += 1
    
   
    if video_capture is not None:
        video_capture.release()
    
    cv2.destroyAllWindows()
    pygame.quit()
    
   


if __name__ == "__main__":
    main()