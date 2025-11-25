
import cv2
import numpy as np
import pygame


class VideoCapture:
    def __init__(self, source_type='none', source_path=None):
        
        self.source_type = source_type
        self.source_path = source_path
        self.capture = None
        self.is_opened = False
        
        if source_type == 'camera':
            self._init_camera()
        elif source_type == 'video':
            self._init_video(source_path)
    def _init_camera(self):
        
        print("\n[INFO] Ouverture de la camera...")
        self.capture = cv2.VideoCapture(0)
        
        if not self.capture.isOpened():
            print("[ERREUR] Impossible d'ouvrir la camera !")
            print("[INFO] Passage en mode FOND UNI")
            self.source_type = 'none'
            self.is_opened = False
        else:
            print("[OK] Camera ouverte avec succes !")
            self.is_opened = True
    
    def _init_video(self, path):
        
        if path is None:
            print("[ERREUR] Aucun chemin de video fourni !")
            self.source_type = 'none'
            self.is_opened = False
            return
        
        print(f"\n[INFO] Chargement de la video : {path}")
        self.capture = cv2.VideoCapture(path)
        
        if not self.capture.isOpened():
            print(f"[ERREUR] Impossible d'ouvrir le fichier : {path}")
            print("[INFO] Passage en mode FOND UNI")
            self.source_type = 'none'
            self.is_opened = False
        else:
            print("[OK] Video chargee avec succes !")
            self.is_opened = True
    
    def read_frame(self, largeur, hauteur):
        
        if not self.is_opened or self.capture is None:
            return None
        
        ret, frame = self.capture.read()
        
        if not ret:
            
            if self.source_type == 'video':
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.capture.read()
                if not ret:
                    return None
            else:
                return None
        
        
        frame = cv2.resize(frame, (largeur, hauteur))
        
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        
        frame = np.rot90(frame)
        frame = np.flipud(frame)
        
        
        frame_surface = pygame.surfarray.make_surface(frame)
        
        return frame_surface
    
    def get_info(self):
       
        if not self.is_opened or self.capture is None:
            return {
                'type': self.source_type,
                'opened': False
            }
        
        info = {
            'type': self.source_type,
            'opened': True,
            'width': int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        }
        
        if self.source_type == 'video':
            info['fps'] = self.capture.get(cv2.CAP_PROP_FPS)
            info['frame_count'] = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
            info['duration'] = info['frame_count'] / info['fps'] if info['fps'] > 0 else 0
        
        return info
    
    def release(self):
        
        if self.capture is not None:
            self.capture.release()
            self.is_opened = False
            print("\n[INFO] Capture video liberee")
    
    def __del__(self):
        
        self.release()


def choisir_fichier_video():
    """
    Ouvre une fenêtre de dialogue pour sélectionner un fichier vidéo
    
    Returns:
        str: Chemin du fichier vidéo, ou None si annulé
    """
    try:
        
        import tkinter as tk
        from tkinter import filedialog
        
        
        root = tk.Tk()
        root.withdraw()  
        root.attributes('-topmost', True)  
        
        print("\n" + "="*50)
        print("SELECTION D'UNE VIDEO")
        print("="*50)
        print("\n[INFO] Une fenetre de selection va s'ouvrir...")
        print("[INFO] Choisissez votre fichier video")
        print("-"*50)
        
        
        filetypes = [
            ('Fichiers vidéo', '*.mp4 *.avi *.mov *.mkv *.webm *.flv *.wmv'),
            ('MP4', '*.mp4'),
            ('AVI', '*.avi'),
            ('MOV', '*.mov'),
            ('MKV', '*.mkv'),
            ('Tous les fichiers', '*.*')
        ]
        
        
        chemin = filedialog.askopenfilename(
            title="Sélectionnez une vidéo",
            filetypes=filetypes,
            initialdir=".",  
        )
        
        
        root.destroy()
        
        if chemin:
            print(f"\n[OK] Video selectionnee : {chemin}")
            return chemin
        else:
            print("\n[INFO] Aucun fichier selectionne")
            print("[INFO] Utilisation de 'video.mp4' par defaut")
            return "video.mp4"
    
    except ImportError:
       
        print("\n[ATTENTION] Tkinter non disponible")
        print("[INFO] Utilisation du mode texte")
        print("\n" + "="*50)
        print("CHARGEMENT D'UNE VIDEO")
        print("="*50)
        print("\nEntrez le chemin de la video (ex: video.mp4)")
        print("Ou laissez vide pour utiliser 'video.mp4' par defaut")
        print("-"*50)
        
        chemin = input("Chemin : ").strip()
        
        if chemin == "":
            chemin = "video.mp4"
        
        return chemin
    
    except Exception as e:
        print(f"\n[ERREUR] Probleme avec la fenetre de selection : {e}")
        print("[INFO] Utilisation de 'video.mp4' par defaut")
        return "video.mp4"