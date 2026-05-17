import mss
import ctypes
import time
import random
from numpy import array, uint8, frombuffer

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

class ColorTriggerbot:
    def __init__(self, target_color, tolerance=30, delay_range=(0.01, 0.03)):
        self.target = array(target_color, dtype=uint8)
        self.tolerance = tolerance
        self.delay_min, self.delay_max = delay_range
        self.sct = mss.mss()
        
    def get_crosshair_pixel(self, monitor_width, monitor_height):
        center_x = monitor_width // 2
        center_y = monitor_height // 2
        
        region = {
            'left': center_x,
            'top': center_y,
            'width': 1,
            'height': 1
        }
        
        screenshot = self.sct.grab(region)
        bgra = frombuffer(screenshot.bgra, dtype=uint8)
        pixel = array([bgra[2], bgra[1], bgra[0]], dtype=uint8)
        return pixel
    
    def color_matches(self, pixel):
        diff = abs(pixel.astype(int) - self.target.astype(int))
        return all(diff <= self.tolerance)
    
    def fire(self):
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.01)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
    def run(self):
        monitor = self.sct.monitors[1]
        width = monitor['width']
        height = monitor['height']
        
        print(f"[Triggerbot Active] Monitoring {width}x{height}")
        
        try:
            while True:
                pixel = self.get_crosshair_pixel(width, height)
                
                if self.color_matches(pixel):
                    self.fire()
                    time.sleep(random.uniform(self.delay_min, self.delay_max))
                
                time.sleep(0.001)
                
        except KeyboardInterrupt:
            print("\n[Triggerbot Stopped]")

PURPLE_ENEMY = (200, 100, 220)

if __name__ == "__main__":
    bot = ColorTriggerbot(
        target_color=PURPLE_ENEMY,
        tolerance=45,
        delay_range=(0.015, 0.035)
    )
    bot.run()
