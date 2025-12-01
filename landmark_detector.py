import cv2
import numpy as np


class LandmarkDetector:
    
    
    def __init__(self, threshold=30, nonmax_suppression=True, detector_type='FAST'):
        
        self.threshold = threshold
        self.nonmax_suppression = nonmax_suppression
        self.detector_type = detector_type
        
       
        self.num_keypoints = 0
        self.detection_time = 0
        
        
        self._init_detector()
    
    def _init_detector(self):
       
        
        if self.detector_type == 'FAST':
            
            self.detector = cv2.FastFeatureDetector_create(
                threshold=self.threshold,
                nonmaxSuppression=self.nonmax_suppression,
                type=cv2.FAST_FEATURE_DETECTOR_TYPE_9_16  
            )
            
        
        
    def detect(self, frame):
       
        if frame is None:
            return []
        
        
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame
        
        
        import time
        start_time = time.time()
        
        
        
        keypoints = self.detector.detect(gray, None)
        
        self.detection_time = (time.time() - start_time) * 1000  # ms
        self.num_keypoints = len(keypoints)
        
        return keypoints
    
    
    
    def compute_descriptor(self, frame):
        if frame is None:
            return [], None
        
        
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame
        
        
        
        
        keypoints = self.detect(frame)
                
                
        orb = cv2.ORB_create()
        keypoints, descriptors = orb.compute(gray, keypoints)
                
        return keypoints, descriptors
    
    def draw_keypoints(self, frame, keypoints, color=(0, 255, 0), radius=3):
        
        if frame is None or len(keypoints) == 0:
            return frame
        
       
        output = frame.copy()
        
        
        for kp in keypoints:
            x = int(kp.pt[0])
            y = int(kp.pt[1])
            
           
            cv2.circle(output, (x, y), radius, color, 1)
            
          
            cv2.circle(output, (x, y), 1, color, -1)
        
        return output
    
    
        
    
    
    def set_threshold(self, threshold):
        self.threshold = max(1, min(100, threshold))
        self._init_detector()
    
    def get_stats(self):
       
        return {
            'num_keypoints': self.num_keypoints,
            'detection_time_ms': round(self.detection_time, 2),
            'threshold': self.threshold,
            'detector_type': self.detector_type
        }
    
    
    
    