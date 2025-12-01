import numpy as np

class Camera:
    def __init__(self, largeur, hauteur, focale):
       
        self.largeur = largeur
        self.hauteur = hauteur
        self.focale = focale
        
        
        self.centre_x = largeur / 2
        self.centre_y = hauteur / 2
    
    def projeter(self, point_3d):
       
        x, y, z = point_3d
        
       
        if z <= 0:
            return None
        
       
        u = self.centre_x + self.focale * (x / z)
        v = self.centre_y + self.focale * (y / z)
        
        return (int(u), int(v))
    
    def projeter_points(self, points_3d):
       
        points_2d = []
        for point in points_3d:
            point_2d = self.projeter(point)
            points_2d.append(point_2d)
        return points_2d