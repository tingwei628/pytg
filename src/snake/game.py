import curses
import snake.config as config
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

SNAKE_GAME = config.SNAKE_GAME
INITIAL_TIMEOUT = config.INITIAL_TIMEOUT
KEY_ESC = config.KEY_ESC  # exit
KEY_SPACE = config.KEY_SPACE  # pause/resume
KEY_ENTER = config.KEY_ENTER  # reset (restart)
START = config.START
STOP = config.STOP

# # snake body
# snake_body = []
# snake_step = 1
# # snake head direction
# snake_head_dir = -1
# score = 0
# game_status = START

# screen_width_mid = 0
# screen_height_mid = 0

# box_top_left = ()
# box_bottom_right = ()
# box = ()


def _game(stdscr):

    # initial setting
    curses.curs_set(0)
    stdscr.nodelay(1)
    snake_timeout = INITIAL_TIMEOUT
    stdscr.timeout(snake_timeout)
    box_top_left_x = 5
    box_top_left_y = 5
    screen_height, screen_width = stdscr.getmaxyx()

    # global screen_width_mid, screen_height_mid
    # global box_top_left
    # global box_bottom_right
    # global box
    # global snake_body, snake_head_dir
    # global score
    # global game_status

    config.screen_height_mid = screen_height // 2
    config.screen_width_mid = screen_width // 2
    config.box_top_left = (box_top_left_x, box_top_left_y)  # (y, x)
    config.box_bottom_right = (screen_height - config.box_top_left[0], screen_width - config.box_top_left[1])
    config.box = (
        config.box_bottom_right[0] - config.box_top_left[0],
        config.box_bottom_right[1] - config.box_top_left[1],
    )  # box height, width
    textpad.rectangle(
        stdscr, config.box_top_left[0], config.box_top_left[1], config.box_bottom_right[0], config.box_bottom_right[1]
    )

    # set snake body
    config.snake_body = [
        (config.screen_height_mid, config.screen_width_mid - 1),  # snake tail
        (config.screen_height_mid, config.screen_width_mid),
        (config.screen_height_mid, config.screen_width_mid + 1),  # snake head position
    ]
    # snake head direction
    config.snake_head_dir = curses.KEY_RIGHT

    # init color pair
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)

    for y, x in config.snake_body:
        stdscr.addstr(y, x, "|", curses.color_pair(1))

    snake_food_pos = _create_food()
    stdscr.addstr(snake_food_pos[0], snake_food_pos[1], "O", curses.color_pair(2))
    config.score = 0
    _update_score(config.score, stdscr)
    # set game status
    config.game_status = START
    _update_status("START", stdscr)

    while 1:
        key = stdscr.getch()

        if config.game_status == START and key == KEY_SPACE:
            stdscr.nodelay(0)
            config.game_status = STOP
            _update_status("STOP ", stdscr)
            continue

        elif config.game_status == STOP and key == KEY_SPACE:
            stdscr.nodelay(1)
            stdscr.timeout(snake_timeout)
            config.game_status = START
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
            config.game_status = START
            _update_status("START", stdscr)
            # snake direction
            config.snake_head_dir = curses.KEY_RIGHT
            # box
            textpad.rectangle(
                stdscr,
                config.box_top_left[0],
                config.box_top_left[1],
                config.box_bottom_right[0],
                config.box_bottom_right[1],
            )
            # snake body
            config.snake_body = [
                (config.screen_height_mid, config.screen_width_mid - 1),
                (config.screen_height_mid, config.screen_width_mid),
                (config.screen_height_mid, config.screen_width_mid + 1),
            ]
            # score
            config.score = 0
            _update_score(config.score, stdscr)
            # food
            snake_food_pos = _create_food()
            stdscr.addstr(snake_food_pos[0], snake_food_pos[1], "O", curses.color_pair(2))
            continue

        if key == -1:  # not input
            key = config.snake_head_dir

        snake_head = config.snake_body[-1]
        if key == curses.KEY_RIGHT and config.snake_head_dir != curses.KEY_LEFT:
            snake_head_next = (snake_head[0], _get_head_next_x(key))
            _append_snake(stdscr, snake_head_next)
            config.snake_head_dir = key
        elif key == curses.KEY_LEFT and config.snake_head_dir != curses.KEY_RIGHT:
            snake_head_next = (snake_head[0], _get_head_next_x(key))
            _append_snake(stdscr, snake_head_next)
            config.snake_head_dir = key
        elif key == curses.KEY_DOWN and config.snake_head_dir != curses.KEY_UP:
            snake_head_next = (_get_head_next_y(key), snake_head[1])
            _append_snake(stdscr, snake_head_next)
            config.snake_head_dir = key
        elif key == curses.KEY_UP and config.snake_head_dir != curses.KEY_DOWN:
            snake_head_next = (_get_head_next_y(key), snake_head[1])
            _append_snake(stdscr, snake_head_next)
            config.snake_head_dir = key
        else:
            continue

        snake_head = config.snake_body[-1]
        if snake_head == snake_food_pos:
            snake_food_pos = _create_food()
            stdscr.addstr(snake_food_pos[0], snake_food_pos[1], "O", curses.color_pair(2))
            config.score += 1
            _update_score(config.score, stdscr)
            # increase speed of snake
            """
            snake_timeout = snake_timeout - len(snake_body) % 90
            stdscr.timeout(snake_timeout)
            """
        elif snake_head in config.snake_body[:-1]:
            stdscr.nodelay(0)
            config.game_status = STOP
            _update_status("OVER ", stdscr)
        else:
            snake_tail = config.snake_body[0]
            stdscr.addstr(snake_tail[0], snake_tail[1], " ")
            config.snake_body.pop(0)


def _create_food():
    food = ()  # empty food (y, x)
    while food == ():
        food = (
            randint(config.box_top_left[0] + 1, config.box_bottom_right[0] - 1),
            randint(config.box_top_left[1] + 1, config.box_bottom_right[1] - 1),
        )
        if food not in config.snake_body:
            return food
        else:
            food = ()


def _get_head_next_x(key):
    snake_head = config.snake_body[-1]
    _dict = {
        curses.KEY_RIGHT: {"dir": 1, "next_start_if_hit": config.box_top_left[1], "hit_condition": config.box[1]},
        curses.KEY_LEFT: {"dir": -1, "next_start_if_hit": config.box_bottom_right[1], "hit_condition": 0},
    }
    _obj = _dict[key]
    return (
        (_obj["next_start_if_hit"] + _obj["dir"] * config.snake_step)
        if (snake_head[1] + _obj["dir"] * config.snake_step - config.box_top_left[1]) == _obj["hit_condition"]
        else snake_head[1] + _obj["dir"] * config.snake_step
    )


def _get_head_next_y(key):
    snake_head = config.snake_body[-1]
    _dict = {
        curses.KEY_DOWN: {"dir": 1, "next_start_if_hit": config.box_top_left[0], "hit_condition": config.box[0]},
        curses.KEY_UP: {"dir": -1, "next_start_if_hit": config.box_bottom_right[0], "hit_condition": 0},
    }
    _obj = _dict[key]
    return (
        (_obj["next_start_if_hit"] + _obj["dir"] * config.snake_step)
        if (snake_head[0] + _obj["dir"] * config.snake_step - config.box_top_left[0]) == _obj["hit_condition"]
        else snake_head[0] + _obj["dir"] * config.snake_step
    )


def _append_snake(stdscr, snake_head_next):
    global snake_body
    stdscr.addstr(snake_head_next[0], snake_head_next[1], "|", curses.color_pair(1))
    config.snake_body.append(snake_head_next)


def _update_score(score, stdscr):
    score_text = "Score: {}".format(score)
    stdscr.addstr(1, config.screen_width_mid - len(score_text) // 2, score_text)


def _update_status(status, stdscr):
    status_text = "Status: {}".format(status)
    stdscr.addstr(3, config.screen_width_mid - len(status_text) // 2, status_text)


def snake_entry():
    curses.wrapper(_game)


if __name__ == "__main__":
    snake_entry()
