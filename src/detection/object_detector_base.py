from pathlib import Path
import cv2
from ultralytics import YOLO

BOX_COLOR = (0, 255, 0)
TEXT_COLOR = (0, 255, 0)

class ObjectDetectorBase:
    
    def __init__(self, model_path: str):
        
        model_path = self._normalize_path(model_path)
        self.model = YOLO(model_path)  # Load the YOLO model

    def detect(self, frame : cv2.typing.MatLike):
        
        results = self.model(frame)
        self._drawn_boxes(frame, results)

    def _drawn_boxes(self, frame, results):
       
        for result in results:

            for box in result.boxes:

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                label = f"{self.model.names[cls]} {conf:.2f}"

                cv2.rectangle(frame, (x1, y1), (x2, y2), BOX_COLOR, 2)
               
                cv2.putText(frame, label, (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, 
                    TEXT_COLOR, 2)
                
    def _normalize_path(self, model_file_name: str) -> str:
        """
        Normalizes the model file name to ensure it can be loaded correctly.
        If the file name starts with "yolo", it is assumed to be a model name
        """
        
        #if starts with yolo, assume it's a model name and prepend "yolo" directory
        if model_file_name.startswith("yolo"):
            return model_file_name;
         
        baseDir = Path(__file__).resolve().parents[2]
        modelsDir = baseDir / "models"
        
        if not modelsDir.exists():
            raise FileNotFoundError(f"Model file {model_file_name} not found in {modelsDir}")
        
        full_path = modelsDir / model_file_name
        
        if not full_path.exists():
            raise FileNotFoundError(f"Model file {model_file_name} not found in {modelsDir}")
        
        return str(model_file_name)
                