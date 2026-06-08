from utils.sys_info import check_sys_info

check_sys_info()

 

#how import the class ANPR from number-plate-recognition.py file and use it in main.py
from src.number_plate_recognition import ANPR

anpr = ANPR(model_path="anpr_best.pt")
anpr.infer_video(source=0, display=True)

def detect_plates(fileName: str):
      # Use trained YOLO license plate model
    anpr.infer_video(source=f"videos/{fileName}", output_path=f"output/{fileName.replace('.mp4', '-anpr.mp4')}", display=True)

if __name__ == "__main__":

    detect_plates("anpr-demo-video.mp4")
    detect_plates("anpr-demo-video.mp4")
    detect_plates("carLicence1.mp4")
    detect_plates("carLicence2.mp4")
    detect_plates("carLicence3.mp4")
    detect_plates("carLicence4.mp4")
