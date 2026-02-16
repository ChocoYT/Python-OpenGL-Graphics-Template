import glfw
import time

class Clock:
    def __init__(self) -> None:
        self._last_time = glfw.get_time()
        self._delta_time = 0.0

    def tick(self, target_fps: float | None = None) -> float:
        frame_time_goal = 0.0
        if target_fps is not None:
            frame_time_goal = 1.0 / target_fps
        
        elapsed = glfw.get_time() - self._last_time
        
        if elapsed < frame_time_goal:
            time.sleep(frame_time_goal - elapsed)
        
        current_time = glfw.get_time()
        self._delta_time = current_time - self._last_time
        self._last_time = current_time

        return self._delta_time
