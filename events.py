from enum import Enum


class Events(Enum):
    CLICKER_PAUSE = "clicker_pause"
    CLICKER_UNPAUSE = "clicker_unpause"
    LOGIC_LOOP_PAUSE = "logic_loop_pause"
    LOGIC_LOOP_UNPAUSE = "logic_loop_unpause"


if __name__ == "__main__":
    print(Events.CLICKER_PAUSE.name)
