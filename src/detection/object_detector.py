 
from detection.object_detector_base import ObjectDetectorBase
               
class ObjectDetector(ObjectDetectorBase):

    def __init__(self):
        super().__init__(model_path="yolo11n.pt")
        
