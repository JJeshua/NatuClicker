import mouse
from time import sleep
import logging

from events import Events


class Clicker:
    def __init__(self, ee):
        self.ee = ee
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

    def get_cps(self) -> int:
        return (1 / self.clicks_per_second)

    def stop(self) -> None:
        self.running = False

    def is_paused(self) -> None:
        return self.paused

    def click_mouse(self, button: str) -> None:
        """Clicks specified mouse button at non-specified location"""
        # logging.debug("(CLICKER) Mouse clicked")
        mouse.click(button)
        sleep(self.clicks_per_second)

    def toggle_pause(self) -> None:
        """Pauses and unpauses main loop"""
        if self.paused:
            logging.info("(CLICKER) Clicker unpausing")
            self.ee.emit(Events.CLICKER_UNPAUSE.name)
        else:
            logging.info("(CLICKER) Clicker pausing")
            self.ee.emit(Events.CLICKER_PAUSE.name)

        self.paused = not self.paused

    def pause(self) -> None:
        """Pauses main loop"""
        logging.info("(CLICKER) Paused clicker")
        self.paused = True
        self.ee.emit(Events.CLICKER_PAUSE.name)

    def unpause(self) -> None:
        """Pauses main loop"""
        logging.info("(CLICKER) Unpaused clicker")
        self.paused = False
        self.ee.emit(Events.CLICKER_UNPAUSE.name)


if __name__ == "__main__":
    pass
