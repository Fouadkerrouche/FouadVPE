import pygame
import numpy as np

class Cube:
   
    
    def __init__(self, taille=10.0):
      
        self.taille = taille
        s = taille / 2
        
       
        self.sommets_originaux = np.array([
            [-s, -s, -s],  
            [ s, -s, -s],  
            [ s,  s, -s],  
            [-s,  s, -s],  
            [-s, -s,  s],  
            [ s, -s,  s],  
            [ s,  s,  s],  
            [-s,  s,  s],  
        ], dtype=float)
        
        
        self.aretes = [
            
            (0, 1), (1, 2), (2, 3), (3, 0),
            
            (4, 5), (5, 6), (6, 7), (7, 4),
            
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        
       
        self.position = np.array([0.0, 0.0, 0.0])
        
       
        self.rotation_x = 0.0
        self.rotation_y = 0.0
        self.rotation_z = 0.0
        
        
        self.couleur = (0, 255, 255)  
    
    def positionner(self, x, y, z):
       
        self.position = np.array([x, y, z])
    
    def matrice_rotation_x(self, angle):
        
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([
            [1, 0,  0],
            [0, c, -s],
            [0, s,  c]
        ])
    
    def matrice_rotation_y(self, angle):
        
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([
            [ c, 0, s],
            [ 0, 1, 0],
            [-s, 0, c]
        ])
    
    def matrice_rotation_z(self, angle):
        
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([
            [c, -s, 0],
            [s,  c, 0],
            [0,  0, 1]
        ])
    
    def obtenir_sommets_transformes(self):
       
       
        Rx = self.matrice_rotation_x(self.rotation_x)
        Ry = self.matrice_rotation_y(self.rotation_y)
        Rz = self.matrice_rotation_z(self.rotation_z)
        
       
        R = Rz @ Ry @ Rx
        
        
        sommets = (R @ self.sommets_originaux.T).T
        
        
        sommets += self.position
        
        return sommets
    
    def afficher(self, ecran, camera):
       
        
        sommets_3d = self.obtenir_sommets_transformes()
        
       
        sommets_2d = camera.projeter_points(sommets_3d)
        
       
        for arete in self.aretes:
            idx1, idx2 = arete
            
            point1 = sommets_2d[idx1]
            point2 = sommets_2d[idx2]
            
           
            if point1 is not None and point2 is not None:
                
                if self._est_dans_ecran(point1, ecran) and \
                   self._est_dans_ecran(point2, ecran):
                   
                    pygame.draw.line(ecran, self.couleur, point1, point2, 2)
        
        
        for point in sommets_2d:
            if point is not None and self._est_dans_ecran(point, ecran):
                pygame.draw.circle(ecran, (255, 255, 0), point, 4)
    
    def _est_dans_ecran(self, point, ecran):
       
        x, y = point
        largeur, hauteur = ecran.get_size()
        return 0 <= x < largeur and 0 <= y < hauteur