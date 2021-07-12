import curses
from random import randint
from curses import textpad

"""
import menu_entry from util.menu
"""
from sys import path
from os.path import join, dirname

path.append(join(dirname(__file__), "../"))

"""
1. restart (ENTER)
   pause/resume (SPACE)
   exit (ESC)
2. A* algorithm


https://stackoverflow.com/questions/44014715/is-it-possible-to-get-the-default-background-color-using-curses-in-python

"""

SNAKE_GAME = 1
INITIAL_TIMEOUT = 100
KEY_ESC = 27  # exit
KEY_SPACE = 32  # pause/resume
KEY_ENTER = 10  # reset (restart)
START = 1
STOP = 0

# snake body
snake_body = []
snake_step = 1
# snake head direction
snake_head_dir = -1
score = 0
game_status = START

screen_width_mid = 0
screen_height_mid = 0

box_top_left = ()
box_bottom_right = ()
box = ()


def _game(stdscr):

    # initial setting
    curses.curs_set(0)
    stdscr.nodelay(1)
    snake_timeout = INITIAL_TIMEOUT
    stdscr.timeout(snake_timeout)
    box_top_left_x = 5
    box_top_left_y = 5
    screen_height, screen_width = stdscr.getmaxyx()

    global screen_width_mid, screen_height_mid
    global box_top_left
    global box_bottom_right
    global box
    global snake_body, snake_head_dir
    global score
    global game_status

    screen_height_mid = screen_height // 2
    screen_width_mid = screen_width // 2
    box_top_left = (box_top_left_x, box_top_left_y)  # (y, x)
    box_bottom_right = (screen_height - box_top_left[0], screen_width - box_top_left[1])
    box = (box_bottom_right[0] - box_top_left[0], box_bottom_right[1] - box_top_left[1])  # box height, width
    textpad.rectangle(stdscr, box_top_left[0], box_top_left[1], box_bottom_right[0], box_bottom_right[1])

    # set snake body
    snake_body = [
        (screen_height_mid, screen_width_mid - 1),  # snake tail
        (screen_height_mid, screen_width_mid),
        (screen_height_mid, screen_width_mid + 1),  # snake head position
    ]
    # snake head direction
    snake_head_dir = curses.KEY_RIGHT

    # init color pair
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)

    for y, x in snake_body:
        stdscr.addstr(y, x, "|", curses.color_pair(1))

    snake_food_pos = _create_food()
    stdscr.addstr(snake_food_pos[0], snake_food_pos[1], "O", curses.color_pair(2))
    score = 0
    _update_score(score, stdscr)
    # set game status
    game_status = START
    _update_status("START", stdscr)

    while 1:
        key = stdscr.getch()

        if game_status == START and key == KEY_SPACE:
            stdscr.nodelay(0)
            game_status = STOP
            _update_status("STOP ", stdscr)
            continue

        elif game_status == STOP and key == KEY_SPACE:
            stdscr.nodelay(1)
            stdscr.timeout(snake_timeout)
            game_status = START
            _update_status("START", stdscr)
            continue

        elif key == KEY_ESC:  # exit to sub_menu
            # avoid circular imports...
            from util.menu import menu_entry

            menu_entry(SNAKE_GAME)
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
            _update_status("START", stdscr)
            # snake direction
            snake_head_dir = curses.KEY_RIGHT
            # box
            textpad.rectangle(stdscr, box_top_left[0], box_top_left[1], box_bottom_right[0], box_bottom_right[1])
            # snake body
            snake_body = [
                (screen_height_mid, screen_width_mid - 1),
                (screen_height_mid, screen_width_mid),
                (screen_height_mid, screen_width_mid + 1),
            ]
            # score
            score = 0
            _update_score(score, stdscr)
            # food
            snake_food_pos = _create_food()
            stdscr.addstr(snake_food_pos[0], snake_food_pos[1], "O", curses.color_pair(2))
            continue

        if key == -1:  # not input
            key = snake_head_dir

        snake_head = snake_body[-1]
        if key == curses.KEY_RIGHT and snake_head_dir != curses.KEY_LEFT:
            snake_head_next = (snake_head[0], _get_head_next_x(key))
            _append_snake(stdscr, snake_head_next)
            snake_head_dir = key
        elif key == curses.KEY_LEFT and snake_head_dir != curses.KEY_RIGHT:
            snake_head_next = (snake_head[0], _get_head_next_x(key))
            _append_snake(stdscr, snake_head_next)
            snake_head_dir = key
        elif key == curses.KEY_DOWN and snake_head_dir != curses.KEY_UP:
            snake_head_next = (_get_head_next_y(key), snake_head[1])
            _append_snake(stdscr, snake_head_next)
            snake_head_dir = key
        elif key == curses.KEY_UP and snake_head_dir != curses.KEY_DOWN:
            snake_head_next = (_get_head_next_y(key), snake_head[1])
            _append_snake(stdscr, snake_head_next)
            snake_head_dir = key
        else:
            continue

        snake_head = snake_body[-1]
        if snake_head == snake_food_pos:
            snake_food_pos = _create_food()
            stdscr.addstr(snake_food_pos[0], snake_food_pos[1], "O", curses.color_pair(2))
            score += 1
            _update_score(score, stdscr)
            # increase speed of snake
            """
            snake_timeout = snake_timeout - len(snake_body) % 90
            stdscr.timeout(snake_timeout)
            """
        elif snake_head in snake_body[:-1]:
            stdscr.nodelay(0)
            game_status = STOP
            _update_status("OVER ", stdscr)
        else:
            snake_tail = snake_body[0]
            stdscr.addstr(snake_tail[0], snake_tail[1], " ")
            snake_body.pop(0)


def _create_food():
    food = ()  # empty food (y, x)
    while food == ():
        food = (
            randint(box_top_left[0] + 1, box_bottom_right[0] - 1),
            randint(box_top_left[1] + 1, box_bottom_right[1] - 1),
        )
        if food not in snake_body:
            return food
        else:
            food = ()


def _get_head_next_x(key):
    snake_head = snake_body[-1]
    _dict = {
        curses.KEY_RIGHT: {"dir": 1, "next_start_if_hit": box_top_left[1], "hit_condition": box[1]},
        curses.KEY_LEFT: {"dir": -1, "next_start_if_hit": box_bottom_right[1], "hit_condition": 0},
    }
    _obj = _dict[key]
    return (
        (_obj["next_start_if_hit"] + _obj["dir"] * snake_step)
        if (snake_head[1] + _obj["dir"] * snake_step - box_top_left[1]) == _obj["hit_condition"]
        else snake_head[1] + _obj["dir"] * snake_step
    )


def _get_head_next_y(key):
    snake_head = snake_body[-1]
    _dict = {
        curses.KEY_DOWN: {"dir": 1, "next_start_if_hit": box_top_left[0], "hit_condition": box[0]},
        curses.KEY_UP: {"dir": -1, "next_start_if_hit": box_bottom_right[0], "hit_condition": 0},
    }
    _obj = _dict[key]
    return (
        (_obj["next_start_if_hit"] + _obj["dir"] * snake_step)
        if (snake_head[0] + _obj["dir"] * snake_step - box_top_left[0]) == _obj["hit_condition"]
        else snake_head[0] + _obj["dir"] * snake_step
    )


def _append_snake(stdscr, snake_head_next):
    global snake_body
    stdscr.addstr(snake_head_next[0], snake_head_next[1], "|", curses.color_pair(1))
    snake_body.append(snake_head_next)


def _update_score(score, stdscr):
    score_text = "Score: {}".format(score)
    stdscr.addstr(1, screen_width_mid - len(score_text) // 2, score_text)


def _update_status(status, stdscr):
    status_text = "Status: {}".format(status)
    stdscr.addstr(3, screen_width_mid - len(status_text) // 2, status_text)


def snake_entry():
    curses.wrapper(_game)


if __name__ == "__main__":
    snake_entry()
