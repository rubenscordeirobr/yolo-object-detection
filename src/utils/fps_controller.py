import time

class FPSController:
    """
    Controls loop timing to maintain a target FPS.
    """

    def __init__(self, target_fps: float = 30):
        
        if target_fps <= 0:
            raise ValueError("target_fps must be greater than 0")

        self.target_fps = target_fps
        self.frame_duration = 1.0 / target_fps

        self._last_time = None
        self._frame_count = 0
        self._start_time = time.perf_counter()

    def set_target_fps(self, new_fps: float):
        """
        Updates the target FPS and recalculates frame duration.
        """
        if new_fps <= 0:
            raise ValueError("new_fps must be greater than 0")
       
        self.target_fps = new_fps
        self.frame_duration = 1.0 / new_fps

    def get_target_fps(self) -> float:
        """
        Returns the current target FPS.
        """
        return self.target_fps

    def start_frame(self):
        """
        Call at the beginning of each frame.
        """
        self._last_time = time.perf_counter()

    def wait(self) -> float:
        """
        Sleeps to maintain target FPS.

        Returns:
            actual sleep time (0 if behind schedule)
        """
        if self._last_time is None:
            self.start_frame()
            return 0.0

        elapsed = time.perf_counter() - self._last_time
        sleep_time = self.frame_duration - elapsed

        if sleep_time > 0:
            time.sleep(sleep_time)
            slept = sleep_time
        else:
            slept = 0.0

        self._frame_count += 1
        return slept

    def get_fps(self) -> float:
        """
        Returns actual achieved FPS since start.
        """
        elapsed = time.perf_counter() - self._start_time
        if elapsed <= 0:
            return 0.0
        return self._frame_count / elapsed
    
  

    def reset(self):
        """
        Resets internal counters.
        """
        self._frame_count = 0
        self._start_time = time.perf_counter()
        self._last_time = None