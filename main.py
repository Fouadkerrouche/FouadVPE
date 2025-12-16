import pygame
import cv2
import numpy as np
from camera import Camera
from cube import Cube
from model_loader import ModelLoader
from video_capture import VideoCapture, choisir_fichier_video
from menu import afficher_menu
from chessboard_detector import ChessboardDetector
import os

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
    
    
    # Initialisation du détecteur d'échiquier
    # Changez pattern_size selon votre échiquier
    # Par défaut: 9x6 coins intérieurs (échiquier 10x7 cases)
    chessboard_detector = ChessboardDetector(
        pattern_size=(7, 7),  # Nombre de coins intérieurs
        square_size=0.023       # Taille d'un carré (unités arbitraires)
    )
    
    
    camera = Camera(
        largeur=LARGEUR,
        hauteur=HAUTEUR,
        focale=500
    )
    
    # Matrice intrinsèque de la caméra pour solvePnP
    camera_matrix = np.array([
        [camera.focale, 0, camera.centre_x],
        [0, camera.focale, camera.centre_y],
        [0, 0, 1]
    ], dtype=float)
    
    # Charger le modèle des pyramides
    model_path = os.path.join(
        os.path.dirname(__file__),
        "simple pyramids",
        "Great_Pyramids_v1_L1.123cecf6cbe7-5991-4a2b-9219-bc012a55622a",
        "15982_Great_Pyramids_v1.obj"
    )
    pyramid_model = ModelLoader(model_path)
    # Échelle pour adapter le modèle à la taille de l'échiquier
    pyramid_model.set_scale(0.015)
    
    show_chessboard = True
    show_model = True
    en_cours = True
    frame_count = 0
    
    while en_cours:
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            
            # Touche pour activer/désactiver l'affichage de l'échiquier
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_chessboard = not show_chessboard
                elif event.key == pygame.K_m:
                    show_model = not show_model
                elif event.key == pygame.K_ESCAPE:
                    en_cours = False
        
        
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
        
        
        # Détection de l'échiquier et affichage
        if frame_bgr is not None:
            
            # Détection des coins de l'échiquier
            keypoints, descriptors = chessboard_detector.compute_descriptor(frame_bgr)
            
            # Dessiner l'échiquier détecté si activé
            if show_chessboard:
                frame_with_chess = chessboard_detector.draw_chessboard(frame_bgr)
            else:
                frame_with_chess = frame_bgr.copy()
            
            # Obtenir les correspondances 2D-3D
            object_points, image_points = chessboard_detector.get_correspondences()
            
            # Afficher les statistiques
            stats = chessboard_detector.get_stats()
            
            # Conversion pour affichage dans pygame
            frame_rgb = cv2.cvtColor(frame_with_chess, cv2.COLOR_BGR2RGB)
            
            # Rotation et flip pour pygame
            frame_rgb = np.rot90(frame_rgb)
            frame_rgb = np.flipud(frame_rgb)
            frame_surface = pygame.surfarray.make_surface(frame_rgb)
            
            # Affichage
            ecran.blit(frame_surface, (0, 0))
            
            # Si l'échiquier est détecté, projeter le modèle 3D
            if stats['pattern_found'] and show_model:
                # Estimation de la pose de l'échiquier
                rvec, tvec, success = chessboard_detector.estimate_pose(camera_matrix)
                
                if success:
                    # Obtenir la position du centre de l'échiquier
                    center_pos = chessboard_detector.get_center_position()
                    
                    if center_pos is not None:
                        # Convertir rvec en matrice de rotation
                        rotation_matrix, _ = cv2.Rodrigues(rvec)
                        
                        # Transformer la position du centre dans le repère caméra
                        center_cam = rotation_matrix @ center_pos + tvec.flatten()
                        
                        # Positionner le modèle au centre de l'échiquier
                        pyramid_model.set_position(center_cam[0], center_cam[1], center_cam[2])
                        
                        # Appliquer la rotation de l'échiquier au modèle
                        # Convertir la rotation de Rodrigues en angles d'Euler (approximation)
                        pyramid_model.rotation_x = 0
                        pyramid_model.rotation_y = 0
                        pyramid_model.rotation_z = 0
                        
                        # Afficher le modèle
                        pyramid_model.afficher(ecran, camera, show_faces=True, show_edges=True)
        

        
        pygame.display.flip()
        horloge.tick(FPS)
        frame_count += 1
    
    
    if video_capture is not None:
        video_capture.release()
    
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()