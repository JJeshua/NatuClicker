import mouse
from time import sleep
import logging


class Clicker:
    def __init__(self):
        self.running = True
        self.paused = True
        self.clicks_per_second = 1 / 22

    def main(self) -> None:
        """Main program loop"""

        logging.debug("(CLICKER) Clicker main loop started")
        while self.running:
            while not self.paused:
                self.click_mouse('left')

            sleep(0.01)

    def click_mouse(self, button: str) -> None:
        """Clicks specified mouse button at non-specified location"""
        logging.debug("(CLICKER) Mouse clicked")
        mouse.click(button)
        sleep(self.clicks_per_second)

    def toggle_pause(self) -> None:
        """Pauses and unpauses main loop"""
        if self.paused:
            logging.info("(CLICKER) Clicker unpausing")
        else:
            logging.info("(CLICKER) Clicker pausing")

        self.paused = not self.paused

    def pause(self):
        """Pauses main loop"""
        logging.info("(CLICKER) Paused clicker")
        self.paused = True

    def unpause(self):
        """Pauses main loop"""
        logging.info("(CLICKER) Unpaused clicker")
        self.paused = False


if __name__ == "__main__":
    pass
