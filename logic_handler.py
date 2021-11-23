import threading
from time import perf_counter, sleep
import logging
from PIL import ImageGrab
import autoit

from clicker import Clicker
from events import Events


# define a Handler which writes INFO messages or higher to the sys.stderr
# console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
# # add the handler to the root logger
# logging.getLogger('').addHandler(console)


class LogicHandler:
    def __init__(self, ee):
        self.ee = ee
        self.clicker = Clicker(ee)
        self.program_running = True
        self.paused = True
        self.button_location = (970, 990)
        self.attack_locations = [(954, 914), (954, 601), (954, 268)]
        self.index = 0

    def main(self) -> None:
        """"Main loop"""

        # Starts auto-clicker thread
        clicker_thread = threading.Thread(target=self.clicker.main)
        clicker_thread.start()

        while self.program_running:
            while not self.paused:
                """Checks to see if currently attacking"""
                # ensures clicker is paused
                self.clicker.pause()

                # move mouse to clicker location and check if attacking
                self.click(self.button_location[0], self.button_location[1])
                self.clicker.unpause()
                logging.debug("(LOGIC_HANDLER) Moving mouse to attack button")

                # checks if button is clicking
                if not self.check_attacking():
                    logging.debug("(LOGIC_HANDLER) Not attacking, trying to attack")

                    self.clicker.pause()
                    sleep(0.01)
                    self.attack()

                sleep(0.5)

            sleep(0.01)

    def stop(self) -> None:
        self.program_running = False

    def is_paused(self) -> bool:
        return self.paused

    def attack(self) -> None:
        """Clicks middle of the screen to begin attacking"""
        logging.debug("(LOGIC_HANDLER) Moving mouse to attack button, clicking")
        coords = self.attack_locations[self.index % 3]
        self.index += 1
        self.click(coords[0], coords[1])
        sleep(0.1)

    def check_attacking(self) -> bool:
        """Checks if button rgb != 0 which means player is attacking"""

        logging.debug("(LOGIC_HANDLER) Checking if player attacking")
        start_time = perf_counter()
        attacking = False

        while (perf_counter() - start_time) < 1:
            rgb = self.get_button_rgb()
            if (rgb[0] == rgb[1]) and (rgb[1] == rgb[2]):
                attacking = True
                break

        logging.debug(f"(LOGIC_HANDLER) Attacking check: {attacking}")
        return attacking

    def get_button_rgb(self) -> object:
        im = ImageGrab.grab(bbox=(
            self.button_location[0], self.button_location[0], self.button_location[0] + 1,
            self.button_location[0] + 1,))
        logging.debug(f"(LOGIC_HANDLER) Attack Button RGB: {im.getpixel((0, 0))}")
        return im.getpixel((0, 0))

    def toggle_pause(self) -> None:
        """Pauses and unpauses main loop"""
        if self.paused:
            logging.info("(LOGIC_HANDLER) Main loop unpausing")
            self.ee.emit(Events.LOGIC_LOOP_UNPAUSE.name)
        else:
            logging.info("(LOGIC_HANDLER) Main_loop pausing")
            self.ee.emit(Events.LOGIC_LOOP_PAUSE.name)

        self.paused = not self.paused

    def click(self, x: int, y: int) -> None:
        autoit.mouse_click('left', x, y, 1)


if __name__ == "__main__":
    logic_handler = LogicHandler()
    t1 = threading.Thread(target=logic_handler.main)
    t1.start()
    logging.debug("(MAIN) Main program thread started")
