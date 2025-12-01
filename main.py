import pygame
import cv2
import numpy as np
from camera import Camera
from cube import Cube
from video_capture import VideoCapture, choisir_fichier_video
from menu import afficher_menu
from landmark_detector import LandmarkDetector

LARGEUR = 800
HAUTEUR = 600
FPS = 60


def main():
    
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("TP VPE - Realite Augmente")
    horloge = pygame.time.Clock()
    
    font = pygame.font.Font(None, 30)
    small_font = pygame.font.Font(None, 20)
    
    
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
    
    
    landmark_detector = LandmarkDetector(
        threshold=30,
        nonmax_suppression=True,
        detector_type='FAST'  
    )
    
    
    
    
    
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
    
    
    show_landmarks = True
    en_cours = True
    frame_count = 0
    
    while en_cours:
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
        
        
        
        if auto_rotation:
            cube.rotation_x += rotation_x
            cube.rotation_y += rotation_y
        
        
        frame_bgr = None  
        
        if source_type != 'none':
            
            frame_surface = video_capture.read_frame(LARGEUR, HAUTEUR)
            
            if frame_surface is not None:
                
                ecran.blit(frame_surface, (0, 0))
                        
                frame_array = pygame.surfarray.array3d(frame_surface)
                
                
                frame_array = np.transpose(frame_array, (1, 0, 2))
                
                
                frame_bgr = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)
            else:
                ecran.fill((20, 20, 40))
        else:
            ecran.fill((20, 20, 40))
        
        
        keypoints = []
        descriptors = None
        
        if frame_bgr is not None and show_landmarks:
            
            keypoints, descriptors = landmark_detector.compute_descriptor(frame_bgr)
       
            
            frame_with_kp = landmark_detector.draw_keypoints(
                frame_bgr, 
                keypoints,
                color=(255, 0, 255),
                radius=3
                )
            
            
            frame_rgb = cv2.cvtColor(frame_with_kp, cv2.COLOR_BGR2RGB)
            
            
            frame_rgb = np.rot90(frame_rgb)
            frame_rgb = np.flipud(frame_rgb)
            frame_surface = pygame.surfarray.make_surface(frame_rgb)
            
            
            ecran.blit(frame_surface, (0, 0))
        
        
        cube.afficher(ecran, camera)



        pygame.display.flip()
        horloge.tick(FPS)
        frame_count += 1
    
    
    if video_capture is not None:
        video_capture.release()
    
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()