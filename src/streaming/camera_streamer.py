import threading
import cv2
import time

from utils.helpers import format_url_path
from domain.camera import CameraConfig
from streaming.ffmpeg_streamer import FFmpegStreamer
from utils.helpers import build_rtsp_url
from detection.object_detector import ObjectDetector
from detection.anpr_detector import AnprDetector    
from utils.fps_controller import FPSController

DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 360
DEFAULT_FPS = 10

class CameraStreamer:

    def __init__(self, camera : CameraConfig, display_window: bool = False):

        self.camera = camera
        self.display_window = display_window
        self.fps_controller = FPSController(target_fps=DEFAULT_FPS)

        formatted_camera_name = format_url_path(camera.camera_name)

        self.streamer = FFmpegStreamer(
            output_url=f"rtsp://localhost:8554/{formatted_camera_name}",
            width=DEFAULT_WIDTH,
            height=DEFAULT_HEIGHT,
            fps=DEFAULT_FPS
        )
        
        self.thread = threading.Thread(
            target=self._stream,
            daemon=True,
            name=f"stream-{self.camera.camera_name}"
        )
        self.detector= ObjectDetector()

    def start(self):
        self.thread.start()
        
    def _stream(self):

        self.streamer.start()
        url_stream = build_rtsp_url(self.camera.ip_address, self.camera.port, self.camera.username, self.camera.password)

        cap = cv2.VideoCapture(url_stream)
        # cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            raise Exception(f"Cannot open camera {self.camera.camera_name}")

        while True:

            self.fps_controller.start_frame()
            ret, frame = cap.read()

            if not ret:
                print(f"Failed frame: {self.camera.camera_name}")
                break

            frame = cv2.resize(frame, (DEFAULT_WIDTH, DEFAULT_HEIGHT))
            self.detector.detect(frame)
            self.streamer.write(frame)

            if self.display_window:
                cv2.imshow(self.camera.camera_name, frame)
                cv2.waitKey(1)
                
            self.fps_controller.wait()
             
        cap.release()
        self.streamer.stop()
        cv2.destroyAllWindows()
        
    def join(self):
        self.thread.join()