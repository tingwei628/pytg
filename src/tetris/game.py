import curses
from random import randint

from curses import ascii

TETRIS_GAME = 2


def _game(stdscr):

    # initial setting
    curses.curs_set(0)
    stdscr.nodelay(1)
    INITIAL_TIMEOUT = 100
    game_timeout = INITIAL_TIMEOUT
    stdscr.timeout(game_timeout)
    box_top_left_x = 5
    box_top_left_y = 5
    KEY_ESC = 27  # exit
    KEY_SPACE = 32  # pause/resume
    KEY_ENTER = 10  # reset (restart)
    START = 1
    STOP = 0
    screen_height, screen_width = stdscr.getmaxyx()
    screen_height_mid = screen_height // 2
    screen_width_mid = screen_width // 2
    box_top_left = (box_top_left_x, box_top_left_y)  # (y, x)
    box_bottom_right = (screen_height - box_top_left[0], screen_width - box_top_left[1])
    box = (box_bottom_right[0] - box_top_left[0], box_bottom_right[1] - box_top_left[1])  # box height, width
    # textpad.rectangle(stdscr, box_top_left[0], box_top_left[1], box_bottom_right[0], box_bottom_right[1])
    _rectangle(stdscr, box_top_left[0], box_top_left[1], box_bottom_right[0], box_bottom_right[1])
    # define color in rainbow order
    curses.init_color(11, *_rgb_255_to_1000((255, 0, 0)))  # RED
    curses.init_color(12, *_rgb_255_to_1000((255, 165, 0)))  # ORANGE
    curses.init_color(13, *_rgb_255_to_1000((255, 255, 0)))  # YELLOW
    curses.init_color(14, *_rgb_255_to_1000((0, 128, 0)))  # GREEN
    curses.init_color(15, *_rgb_255_to_1000((0, 0, 255)))  # BLUE
    curses.init_color(16, *_rgb_255_to_1000((75, 0, 130)))  # INDIGO
    curses.init_color(17, *_rgb_255_to_1000((238, 130, 238)))  # VIOLET

    # set block color pair
    curses.init_pair(11, 11, 11)  # RED
    curses.init_pair(12, 12, 12)  # ORANGE
    curses.init_pair(13, 13, 13)  # YELLOW
    curses.init_pair(14, 14, 14)  # GREEN
    curses.init_pair(15, 15, 15)  # BLUE
    curses.init_pair(16, 16, 16)  # INDIGO
    curses.init_pair(17, 17, 17)  # VIOLET
    # set border color pair
    curses.init_pair(20, curses.COLOR_WHITE, curses.COLOR_WHITE)
    # curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
    # stdscr.attron(curses.color_pair(13))
    game_status = START
    # status_text = "Status: {}".format("START")
    # stdscr.addstr(3, screen_width_mid - len(status_text) // 2, status_text)
    # stdscr.attroff(curses.color_pair(13))

    # stdscr.attron(curses.color_pair(11))
    # stdscr.addstr(3, 1, u"\u2588".encode("utf-8"))
    # stdscr.attroff(curses.color_pair(11))
    # stdscr.attron(curses.color_pair(12))
    # stdscr.addstr(3, 2, u"\u2588".encode("utf-8"))
    # stdscr.attroff(curses.color_pair(12))
    # stdscr.attron(curses.color_pair(13))
    # stdscr.addstr(3, 3, u"\u2588".encode("utf-8"))
    # stdscr.attroff(curses.color_pair(13))

    block = "O"
    stdscr.attron(curses.color_pair(13))
    for x in range(box_top_left[1] + 2, box_bottom_right[1] + 1):
        stdscr.addstr(box_bottom_right[0] - 2, x, block)
        stdscr.addstr(box_bottom_right[0] - 1, x, block)
    stdscr.attroff(curses.color_pair(13))

    # stdscr.attron(curses.color_pair(14))
    # stdscr.addstr(3, 4, " ")
    # stdscr.attroff(curses.color_pair(14))
    # stdscr.attron(curses.color_pair(15))
    # stdscr.addstr(3, 5, " ")
    # stdscr.attroff(curses.color_pair(15))
    # stdscr.attron(curses.color_pair(16))
    # stdscr.addstr(3, 6, " ")
    # stdscr.attroff(curses.color_pair(16))
    # stdscr.attron(curses.color_pair(17))
    # stdscr.addstr(3, 7, " ")
    # stdscr.attroff(curses.color_pair(17))

    while 1:
        key = stdscr.getch()
        if game_status == START and key == KEY_SPACE:
            stdscr.nodelay(0)
            game_status = STOP
            status_text = "Status: {}".format("STOP ")
            stdscr.addstr(3, screen_width_mid - len(status_text) // 2, status_text)
            continue

        elif game_status == STOP and key == KEY_SPACE:
            stdscr.nodelay(1)
            stdscr.timeout(game_timeout)
            game_status = START
            status_text = "Status: {}".format("START")
            stdscr.addstr(3, screen_width_mid - len(status_text) // 2, status_text)
            continue

        elif key == KEY_ESC:  # exit to sub_menu
            # avoid circular imports...
            from util.menu import menu_entry

            menu_entry(TETRIS_GAME)
            break
        elif key == KEY_ENTER:
            # screen clear
            stdscr.clear()
            # timeout
            stdscr.nodelay(1)
            snake_timeout = INITIAL_TIMEOUT
            stdscr.timeout(snake_timeout)
            # status
            game_status = START
            status_text = "Status: {}".format("START")
            stdscr.addstr(3, screen_width_mid - len(status_text) // 2, status_text)
            # # snake direction
            # snake_head_dir = curses.KEY_RIGHT
            # # box
            # textpad.rectangle(stdscr, box_top_left[0], box_top_left[1], box_bottom_right[0], box_bottom_right[1])
            # # snake body
            # snake_body = [
            #     (screen_height_mid, screen_width_mid - 1),
            #     (screen_height_mid, screen_width_mid),
            #     (screen_height_mid, screen_width_mid + 1),
            # ]
            # # score
            # score = 0
            # update_score(score, screen_width_mid, stdscr)
            # # food
            # stdscr.attron(curses.color_pair(2))
            # snake_food_pos = create_food(snake_body, box_top_left, box_bottom_right)
            # stdscr.addstr(snake_food_pos[0], snake_food_pos[1], "O")
            # stdscr.attroff(curses.color_pair(2))
            continue


def _rectangle(stdscr, uly, ulx, lry, lrx):
    """Draw a rectangle with corners at the provided upper-left
    and lower-right coordinates.
    """
    stdscr.attron(curses.color_pair(20))
    stdscr.vline(uly + 1, ulx, curses.ACS_VLINE, lry - uly - 1)
    stdscr.hline(uly, ulx + 1, curses.ACS_HLINE, lrx - ulx - 1)
    stdscr.hline(lry, ulx + 1, curses.ACS_HLINE, lrx - ulx - 1)
    stdscr.vline(uly + 1, lrx, curses.ACS_VLINE, lry - uly - 1)
    stdscr.addch(uly, ulx, curses.ACS_ULCORNER)  # top left corner
    stdscr.addch(uly, lrx, curses.ACS_URCORNER)  # top right corner
    stdscr.addch(lry, lrx, curses.ACS_LRCORNER)  # bottom right corner
    stdscr.addch(lry, ulx, curses.ACS_LLCORNER)  # bottom left corner
    stdscr.attroff(curses.color_pair(20))


# rgb 255 to 1000 curses color
def _rgb_255_to_1000(rgb_tuple: tuple) -> tuple:
    return tuple(rgb * 1000 // 255 for rgb in rgb_tuple)


def tetris_entry():
    curses.wrapper(_game)


if __name__ == "__main__":
    tetris_entry()
