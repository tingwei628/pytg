import curses
from random import randint
from curses import textpad

TETRIS_GAME = 2


def game(stdscr):

    # initial setting
    curses.curs_set(0)
    stdscr.nodelay(1)
    INITIAL_TIMEOUT = 100
    snake_timeout = INITIAL_TIMEOUT
    stdscr.timeout(snake_timeout)
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
    textpad.rectangle(stdscr, box_top_left[0], box_top_left[1], box_bottom_right[0], box_bottom_right[1])

    game_status = START
    status_text = "Status: {}".format("START")
    stdscr.addstr(3, screen_width_mid - len(status_text) // 2, status_text)

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
            stdscr.timeout(snake_timeout)
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


def tetris_entry():
    curses.wrapper(game)


if __name__ == "__main__":
    tetris_entry()
