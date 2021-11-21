from pynput import mouse as ms
import threading
from time import perf_counter, sleep
import logging
from PIL import ImageGrab
import autoit

from clicker import Clicker

logging.basicConfig(
    filename=f'logs/main.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%m-%d-%Y %H:%M:%S')


# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# add the handler to the root logger
logging.getLogger('').addHandler(console)


class Program:
    def __init__(self):
        self.clicker = Clicker()

        self.program_running = True
        self.paused = True

        self.button_location = (970, 990)
        self.attack_location = (936, 270)
        self.attack_location_2 = (955, 521)
        self.attack_locations = [(936, 270), (955, 521)]
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
                logging.debug("(MAIN) Moving mouse to attack button")

                # checks if button is clicking
                if not self.check_attacking():
                    logging.debug("(MAIN) Not attacking, trying to attack")

                    self.clicker.pause()
                    sleep(0.01)
                    self.attack()

                sleep(0.5)

            sleep(0.01)

    def attack(self) -> None:
        """Clicks middle of the screen to begin attacking"""
        logging.debug("(MAIN) Moving mouse to attack button, clicking")
        coords = self.attack_locations[self.index % 2]
        self.index += 1
        self.click(coords[0], coords[1])
        sleep(0.1)

    def check_attacking(self):
        """Checks if button rgb != 0 which means player is attacking"""

        logging.debug("(MAIN) Checking if player attacking")
        start_time = perf_counter()
        attacking = False

        while (perf_counter() - start_time) < 1:
            rgb = self.get_button_rgb()
            if (rgb[0] == rgb[1]) and (rgb[1] == rgb[2]):
                attacking = True
                break

        logging.debug(f"(MAIN) Attacking check: {attacking}")
        return attacking

    def get_button_rgb(self) -> object:
        im = ImageGrab.grab(bbox=(
            self.button_location[0], self.button_location[0], self.button_location[0] + 1,
            self.button_location[0] + 1,))
        logging.debug(f"(MAIN) Attack Button RGB: {im.getpixel((0, 0))}")
        return im.getpixel((0, 0))

    def toggle_pause(self):
        """Pauses and unpauses main loop"""
        if self.paused:
            logging.info("(MAIN) Main loop unpausing")
        else:
            logging.info("(MAIN) Main_loop pausing")

        self.paused = not self.paused

    def click(self, x, y):
        autoit.mouse_click('left', x, y, 1)


def on_click(x, y, button, pressed) -> None:
    """Mouse event listener"""

    # print(f"({x}, {y}) | {button} | {pressed}")
    if (button == ms.Button.x2) and pressed:
        logging.info("(MAIN) (USER) manually toggled clicker")
        program.clicker.toggle_pause()

    if (button == ms.Button.x1) and pressed:
        logging.info("(MAIN) (USER) manually toggled main loop")
        program.toggle_pause()


if __name__ == "__main__":
    program = Program()
    t1 = threading.Thread(target=program.main)
    t1.start()
    logging.debug("(MAIN) Main program thread started")

    logging.debug("(MAIN) Starting mouse event listener")
    with ms.Listener(on_click=on_click) as listener:
        listener.join()
