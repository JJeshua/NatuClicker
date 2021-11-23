import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic
import threading
import logging
from pynput import mouse as ms
from time import perf_counter, sleep
from pymitter import EventEmitter

from events import Events
from logic_handler import LogicHandler

logging.basicConfig(
    filename=f'logs/main.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.WARNING,
    datefmt='%m-%d-%Y %H:%M:%S')

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

ee = EventEmitter()


def on_click(x, y, button, pressed) -> None:
    """Mouse event listener"""

    # print(f"({x}, {y}) | {button} | {pressed}")
    if (button == ms.Button.x2) and pressed:
        logic_handler.clicker.toggle_pause()
        logging.info("(MAIN) (USER) manually toggled clicker")

    if (button == ms.Button.x1) and pressed:
        logic_handler.toggle_pause()
        logging.info("(MAIN) (USER) manually toggled logic")


@ee.on(Events.LOGIC_LOOP_PAUSE.name)
def logic_label_update_0():
    window.logic_label_update_0()


@ee.on(Events.LOGIC_LOOP_UNPAUSE.name)
def logic_label_update_1():
    window.logic_label_update_1()


@ee.on(Events.CLICKER_PAUSE.name)
def clicker_label_update_0():
    window.clicker_label_update_0()


@ee.on(Events.CLICKER_UNPAUSE.name)
def clicker_label_update_1():
    window.clicker_label_update_1()


class Program(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("./ui_exports/1.0.0.ui", self)

        # self.setFixedSize(400, 250)
        self.events = Events

        self.cps_number_label.setText(str(logic_handler.clicker.get_cps()))

    def logic_label_update_0(self):
        self.logic_status_label.setStyleSheet(u"background-color: rgb(255, 192, 159);")

    def logic_label_update_1(self):
        self.logic_status_label.setStyleSheet(u"background-color: rgb(173, 247, 182);")

    def clicker_label_update_0(self):
        self.auto_clicker_status_label.setStyleSheet(u"background-color: rgb(255, 192, 159);")

    def clicker_label_update_1(self):
        self.auto_clicker_status_label.setStyleSheet(u"background-color: rgb(173, 247, 182);")


if __name__ == "__main__":
    """Logic Handler Portion"""
    logic_handler = LogicHandler(ee)
    t1 = threading.Thread(target=logic_handler.main)
    t1.start()
    logging.debug("(MAIN) Logic Handler thread started")

    """Starts mouse event listener"""
    listener = ms.Listener(on_click=on_click)
    listener.start()
    logging.debug("(LOGIC HANDLER) Started mouse event listener")

    """GUI Portion"""
    app = QApplication(sys.argv)

    window = Program()
    window.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Closing Window...")
        logic_handler.clicker.stop()
        logic_handler.stop()
