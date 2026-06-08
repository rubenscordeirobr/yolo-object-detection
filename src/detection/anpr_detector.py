from detection.object_detector_base import ObjectDetectorBase

class AnprDetector(ObjectDetectorBase):
    
    def __init__(self):
        super().__init__(model_path="anpr_best.pt")