from utils.sys_info import check_sys_info
from streaming.ffmpeg_streamer import FFmpegStreamer
import cv2
import threading
from detection.object_detector import ObjectDetector
 
streamer = FFmpegStreamer(
            output_url=f"rtsp://localhost:8554/webcam",
            width=640,
            height=360,
            fps=30
        )

detector = ObjectDetector()

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise ValueError(f"Cannot open video source: WebCam")

def _thread_stream():
    streamer.start()
  
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        frame = cv2.resize(frame, (640, 360))
        
        detector.detect(frame)
        
        streamer.write(frame)
        cv2.imshow("WebCam", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
thread = threading.Thread(target=_thread_stream, daemon=True)
thread.start()
thread.join()

cap.release()
streamer.stop()
cv2.destroyAllWindows()

 