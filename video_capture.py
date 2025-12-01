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
        
      
        self.capture = cv2.VideoCapture(0)
        
        if not self.capture.isOpened():
           
            self.source_type = 'none'
            self.is_opened = False
        else:
            
            self.is_opened = True
    
    def _init_video(self, path):
        
        if path is None:
           
            self.source_type = 'none'
            self.is_opened = False
            return
        
       
        self.capture = cv2.VideoCapture(path)
        
        if not self.capture.isOpened():
           
            self.source_type = 'none'
            self.is_opened = False
        else:
           
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
        
      
        if self.source_type == 'camera':
            frame = cv2.flip(frame, 1)
        
       
        frame = cv2.resize(frame, (largeur, hauteur))
        
       
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        
        frame = np.rot90(frame)
        frame = np.flipud(frame)
        
      
        frame_surface = pygame.surfarray.make_surface(frame)
        
        return frame_surface

    
    def __del__(self):
        
        self.release()


def choisir_fichier_video():
        import tkinter as tk
        from tkinter import filedialog
        
        
        root = tk.Tk()
        root.withdraw()  
        root.attributes('-topmost', True)  
        
        
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
          
            return chemin
        else:
            
            return None
    
    
       
        