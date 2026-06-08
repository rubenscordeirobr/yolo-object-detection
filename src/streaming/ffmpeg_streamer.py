import subprocess
import numpy as np


class FFmpegStreamer:
    def __init__(
        self,
        output_url: str,
        width: int,
        height: int,
        fps: int = 20,
    ):
        self.output_url = output_url
        self.width = width
        self.height = height
        self.fps = fps

        self._process = None

    def start(self):
        command = [
            "ffmpeg",
            "-loglevel", "error",
            "-f", "rawvideo",
            "-pix_fmt", "bgr24",
            "-s", f"{self.width}x{self.height}",
            "-r", str(self.fps),
            "-i", "-",

            "-an",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-tune", "zerolatency",
            "-pix_fmt", "yuv420p",

            "-f", "rtsp",
            self.output_url,
        ]

        self._process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def write(self, frame: np.ndarray):
      
        if self._process is None or self._process.stdin is None:
            raise RuntimeError("FFmpeg streamer not started")

        if frame.shape[1] != self.width or frame.shape[0] != self.height:
            raise ValueError(
                f"Invalid frame size: expected {self.width}x{self.height}, got {frame.shape}"
            )

        try:
            self._process.stdin.write(frame.tobytes())
        except BrokenPipeError:
            raise RuntimeError("FFmpeg process died (broken pipe)")

    def stop(self):
        if self._process is None:
            return

        try:
            self._process.stdin.close()
            self._process.wait(timeout=5)
        except Exception:
            self._process.kill()
        finally:
            self._process = None