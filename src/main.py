from typing import List
from services.camare_service import CameraService
from utils.sys_info import check_sys_info
from streaming.camera_streamer import CameraStreamer
from streaming.ffmpeg_streamer import FFmpegStreamer
import cv2
import threading
import time
from detection.object_detector import ObjectDetector

check_sys_info()

DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 360
DEFAULT_FPS = 30
cap = cv2.VideoCapture(0)

cameras = CameraService.get_cameras()
streamers: List[CameraStreamer] = []

for camera in cameras:
    
    print(camera.camera_name)
    print(camera.ip_address)
    
    streamer = CameraStreamer(camera, display_window=True)
    streamers.append(streamer)
    streamer.start()
    
    #for debugging only stream one camera
    break;
    
#wait
for streamer in streamers:
    streamer.join()
    
    

 