import pygame
import numpy as np

class ModelLoader:
    """
    Classe pour charger et afficher des modèles 3D au format OBJ
    """
    
    def __init__(self, obj_path):
        """
        Initialise le chargeur de modèle
        
        Args:
            obj_path: chemin vers le fichier .obj
        """
        self.vertices = []
        self.faces = []
        self.load_obj(obj_path)
        
        # Position et rotation du modèle
        self.position = np.array([0.0, 0.0, 0.0])
        self.rotation_x = 0.0
        self.rotation_y = 0.0
        self.rotation_z = 0.0
        self.scale = 1.0
        
        # Couleur par défaut
        self.edge_color = (255, 215, 0)  # Gold
        self.face_color = (200, 180, 50)  # Darker gold
    
    def load_obj(self, obj_path):
        """
        Charge un fichier OBJ et extrait les sommets et les faces
        
        Args:
            obj_path: chemin vers le fichier .obj
        """
        self.vertices = []
        self.faces = []
        
        try:
            with open(obj_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = line.split()
                    if not parts:
                        continue
                    
                    # Lecture des sommets
                    if parts[0] == 'v':
                        # Format: v x y z
                        x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                        self.vertices.append([x, y, z])
                    
                    # Lecture des faces
                    elif parts[0] == 'f':
                        # Format: f v1 v2 v3 ou f v1/vt1/vn1 v2/vt2/vn2 v3/vt3/vn3
                        face = []
                        for vertex_data in parts[1:]:
                            # Extraire l'index du sommet (peut être v, v/vt, v/vt/vn, ou v//vn)
                            vertex_index = vertex_data.split('/')[0]
                            # OBJ utilise des indices commençant à 1
                            face.append(int(vertex_index) - 1)
                        self.faces.append(face)
            
            self.vertices = np.array(self.vertices, dtype=float)
            print(f"Modèle chargé: {len(self.vertices)} sommets, {len(self.faces)} faces")
            
        except Exception as e:
            print(f"Erreur lors du chargement du modèle: {e}")
            # Créer un modèle par défaut (pyramide simple)
            self.create_default_pyramid()
    
    def create_default_pyramid(self):
        """
        Crée une pyramide par défaut si le chargement échoue
        """
        self.vertices = np.array([
            [0.0, 0.0, 10.0],    # Sommet
            [-5.0, -5.0, 0.0],   # Base
            [5.0, -5.0, 0.0],
            [5.0, 5.0, 0.0],
            [-5.0, 5.0, 0.0]
        ], dtype=float)
        
        self.faces = [
            [0, 1, 2],  # Faces latérales
            [0, 2, 3],
            [0, 3, 4],
            [0, 4, 1],
            [1, 2, 3, 4]  # Base
        ]
    
    def set_position(self, x, y, z):
        """Définit la position du modèle"""
        self.position = np.array([x, y, z])
    
    def set_scale(self, scale):
        """Définit l'échelle du modèle"""
        self.scale = scale
    
    def matrice_rotation_x(self, angle):
        """Matrice de rotation autour de l'axe X"""
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([
            [1, 0,  0],
            [0, c, -s],
            [0, s,  c]
        ])
    
    def matrice_rotation_y(self, angle):
        """Matrice de rotation autour de l'axe Y"""
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([
            [ c, 0, s],
            [ 0, 1, 0],
            [-s, 0, c]
        ])
    
    def matrice_rotation_z(self, angle):
        """Matrice de rotation autour de l'axe Z"""
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([
            [c, -s, 0],
            [s,  c, 0],
            [0,  0, 1]
        ])
    
    def get_transformed_vertices(self):
        """
        Obtient les sommets transformés (rotation + échelle + translation)
        
        Returns:
            sommets transformés
        """
        # Matrices de rotation
        Rx = self.matrice_rotation_x(self.rotation_x)
        Ry = self.matrice_rotation_y(self.rotation_y)
        Rz = self.matrice_rotation_z(self.rotation_z)
        
        # Rotation combinée
        R = Rz @ Ry @ Rx
        
        # Application de l'échelle et de la rotation
        vertices = (R @ (self.vertices * self.scale).T).T
        
        # Application de la translation
        vertices += self.position
        
        return vertices
    
    def afficher(self, ecran, camera, show_faces=True, show_edges=True):
        """
        Affiche le modèle 3D sur l'écran
        
        Args:
            ecran: surface pygame
            camera: objet Camera pour la projection
            show_faces: afficher les faces remplies
            show_edges: afficher les arêtes
        """
        # Obtenir les sommets transformés
        vertices_3d = self.get_transformed_vertices()
        
        # Projeter les sommets en 2D
        vertices_2d = camera.projeter_points(vertices_3d)
        
        # Afficher les faces
        if show_faces:
            for face in self.faces:
                # Vérifier que tous les sommets de la face sont projetés
                points_2d = []
                valid = True
                for idx in face:
                    if idx < len(vertices_2d) and vertices_2d[idx] is not None:
                        point = vertices_2d[idx]
                        if self._est_dans_limites(point, ecran):
                            points_2d.append(point)
                        else:
                            valid = False
                            break
                    else:
                        valid = False
                        break
                
                # Dessiner la face si tous les points sont valides
                if valid and len(points_2d) >= 3:
                    try:
                        pygame.draw.polygon(ecran, self.face_color, points_2d)
                    except:
                        pass
        
        # Afficher les arêtes
        if show_edges:
            for face in self.faces:
                # Dessiner les arêtes de chaque face
                for i in range(len(face)):
                    idx1 = face[i]
                    idx2 = face[(i + 1) % len(face)]
                    
                    if idx1 < len(vertices_2d) and idx2 < len(vertices_2d):
                        point1 = vertices_2d[idx1]
                        point2 = vertices_2d[idx2]
                        
                        if (point1 is not None and point2 is not None and
                            self._est_dans_limites(point1, ecran) and
                            self._est_dans_limites(point2, ecran)):
                            try:
                                pygame.draw.line(ecran, self.edge_color, point1, point2, 2)
                            except:
                                pass
    
    def _est_dans_limites(self, point, ecran):
        """Vérifie si un point est dans les limites de l'écran"""
        x, y = point
        largeur, hauteur = ecran.get_size()
        margin = 100  # Marge pour éviter les erreurs
        return -margin <= x < largeur + margin and -margin <= y < hauteur + margin
