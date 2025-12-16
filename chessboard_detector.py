import cv2
import numpy as np


class ChessboardDetector:
    """
    Détecteur de coins d'échiquier pour la calibration de caméra
    """
    
    def __init__(self, pattern_size=(9, 6), square_size=1.0):
        """
        Initialise le détecteur d'échiquier
        
        Args:
            pattern_size: tuple (largeur, hauteur) - nombre de coins intérieurs
            square_size: taille d'un carré en unités du monde réel (ex: cm)
        """
        self.pattern_size = pattern_size
        self.square_size = square_size
        
        # Statistiques de détection
        self.num_corners = 0
        self.detection_time = 0
        self.pattern_found = False
        
        # Préparer les points 3D du motif (coordonnées monde)
        self._prepare_object_points()
    
    def _prepare_object_points(self):
        """
        Prépare les coordonnées 3D des coins de l'échiquier dans le repère monde
        L'échiquier est placé sur le plan Z=0
        """
        objp = np.zeros((self.pattern_size[0] * self.pattern_size[1], 3), np.float32)
        objp[:, :2] = np.mgrid[0:self.pattern_size[0], 
                                0:self.pattern_size[1]].T.reshape(-1, 2)
        objp *= self.square_size
        self.object_points = objp
    
    def detect(self, frame):
        """
        Détecte les coins de l'échiquier dans une image
        
        Args:
            frame: image BGR ou niveaux de gris
            
        Returns:
            corners: liste des coins détectés (format compatible avec keypoints)
                    ou liste vide si non détecté
        """
        if frame is None:
            return []
        
        # Conversion en niveaux de gris si nécessaire
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame
        
        # Mesure du temps de détection
        import time
        start_time = time.time()
        
        # Détection des coins de l'échiquier
        ret, corners = cv2.findChessboardCorners(
            gray, 
            self.pattern_size,
            cv2.CALIB_CB_ADAPTIVE_THRESH + 
            cv2.CALIB_CB_FAST_CHECK +
            cv2.CALIB_CB_NORMALIZE_IMAGE
        )
        
        self.detection_time = (time.time() - start_time) * 1000  # ms
        self.pattern_found = ret
        
        if ret:
            # Raffinement sub-pixel des coins
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            
            # Conversion en format compatible (liste de points)
            self.corners_2d = corners.reshape(-1, 2)
            self.num_corners = len(self.corners_2d)
            
            # Créer des objets similaires aux keypoints pour compatibilité
            keypoints = []
            for corner in self.corners_2d:
                # Créer un objet simple avec attribut pt
                kp = type('obj', (object,), {'pt': (corner[0], corner[1])})()
                keypoints.append(kp)
            
            return keypoints
        else:
            self.num_corners = 0
            self.corners_2d = None
            return []
    
    def get_correspondences(self):
        """
        Retourne les correspondances 2D-3D pour la calibration
        
        Returns:
            object_points: points 3D dans le repère monde
            image_points: points 2D dans l'image
        """
        if self.pattern_found and self.corners_2d is not None:
            return self.object_points, self.corners_2d
        else:
            return None, None
    
    def draw_chessboard(self, frame):
        """
        Dessine l'échiquier détecté sur l'image
        
        Args:
            frame: image BGR
            
        Returns:
            output: image avec l'échiquier dessiné
        """
        if frame is None:
            return frame
        
        output = frame.copy()
        
        if self.pattern_found and self.corners_2d is not None:
            # Dessiner les coins
            corners_int = self.corners_2d.reshape(-1, 1, 2).astype(np.float32)
            cv2.drawChessboardCorners(output, self.pattern_size, corners_int, True)
            
            # Ajouter des informations
            cv2.putText(output, f"Pattern detecte: {self.num_corners} coins", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(output, "Pattern non detecte", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        return output
    
    def draw_keypoints(self, frame, keypoints=None, color=(0, 255, 0), radius=5):
        """
        Dessine les coins détectés (compatible avec l'ancienne interface)
        
        Args:
            frame: image BGR
            keypoints: ignoré, utilise les coins détectés
            color: couleur des marqueurs
            radius: rayon des cercles
            
        Returns:
            output: image avec les coins dessinés
        """
        return self.draw_chessboard(frame)
    
    def compute_descriptor(self, frame):
        """
        Détecte l'échiquier et retourne les keypoints
        (Interface compatible avec LandmarkDetector)
        
        Returns:
            keypoints: liste des coins détectés
            descriptors: None (pas utilisé pour l'échiquier)
        """
        keypoints = self.detect(frame)
        return keypoints, None
    
    def get_stats(self):
        """
        Retourne les statistiques de détection
        
        Returns:
            dict: statistiques
        """
        return {
            'num_corners': self.num_corners,
            'detection_time_ms': round(self.detection_time, 2),
            'pattern_size': self.pattern_size,
            'pattern_found': self.pattern_found,
            'detector_type': 'Chessboard'
        }
    
    def set_pattern_size(self, width, height):
        """
        Change la taille du motif de l'échiquier
        
        Args:
            width: nombre de coins intérieurs en largeur
            height: nombre de coins intérieurs en hauteur
        """
        self.pattern_size = (width, height)
        self._prepare_object_points()
    
    def estimate_pose(self, camera_matrix, dist_coeffs=None):
        """
        Estime la pose de l'échiquier par rapport à la caméra
        
        Args:
            camera_matrix: matrice intrinsèque de la caméra (3x3)
            dist_coeffs: coefficients de distorsion (peut être None)
            
        Returns:
            rvec: vecteur de rotation
            tvec: vecteur de translation
            success: True si la pose a été estimée avec succès
        """
        if not self.pattern_found or self.corners_2d is None:
            return None, None, False
        
        if dist_coeffs is None:
            dist_coeffs = np.zeros((4, 1))
        
        # Utiliser solvePnP pour estimer la pose
        success, rvec, tvec = cv2.solvePnP(
            self.object_points,
            self.corners_2d,
            camera_matrix,
            dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )
        
        return rvec, tvec, success
    
    def get_center_position(self):
        """
        Retourne la position du centre de l'échiquier dans les coordonnées monde
        
        Returns:
            center: coordonnées [x, y, z] du centre
        """
        if not self.pattern_found:
            return None
        
        # Calculer le centre des points 3D de l'échiquier
        center_x = (self.pattern_size[0] - 1) * self.square_size / 2
        center_y = (self.pattern_size[1] - 1) * self.square_size / 2
        
        return np.array([center_x, center_y, 0.0])