import curses
from random import choice
import tetris.config as config

"""
import util/block when executing game.py
"""
from sys import path
from os.path import join, dirname

path.append(join(dirname(__file__), "../"))

from util import block as mod_block


"""
KEY_RIGHT: move right
KEY_LEFT: move left
KEY_UP: rotate (clockwise)
z: rotate (counterclockwise)
SPACE: drop rapidly
s: pause/resume

support:
1.Wall kick
"""

TETRIS_GAME = config.TETRIS_GAME
BLOCK_EMPTY = config.BLOCK_EMPTY
BLOCK_FILLED = config.BLOCK_FILLED

# 2 is a moving block pivot

KEY_ESC = config.KEY_ESC  # exit
KEY_SPACE = config.KEY_SPACE  # hard drop
KEY_S = config.KEY_S  # "s" pause/resume
KEY_Z = config.KEY_Z  # "z" rotate couterclockwise
KEY_ENTER = config.KEY_ENTER  # reset (restart)

ROTATION_CLOCKWISE = config.ROTATION_CLOCKWISE
ROTATION_COUNTERCLOCKWISE = config.ROTATION_COUNTERCLOCKWISE
BLOCK_TYPE_I = config.BLOCK_TYPE_I  # I block

COLOR_PAIR_RANGE = config.COLOR_PAIR_RANGE
BLOCK_TYPE_RANGE = config.BLOCK_TYPE_RANGE
BLOCK_ROTATION_RANGE = config.BLOCK_ROTATION_RANGE

SCORE_POS = config.SCORE_POS
STATUS_POS = config.STATUS_POS

START = config.START
STOP = config.STOP

# block_stack = []
# block_map = []
# block_init_pos_map = []
# kick_map = {}
# block_lock = False  # is this block locked to be merged
# block_y_pos = 0
# block_x_pos = 0
# block_color = -1
# block_type = -1
# block_rotation = -1
# score = 0


def _game(stdscr):

    # initial setting
    curses.curs_set(0)
    stdscr.nodelay(1)
    INITIAL_TIMEOUT = 700
    game_timeout = INITIAL_TIMEOUT
    stdscr.timeout(game_timeout)
    box_top_left_x = 5
    box_top_left_y = 5
    game_status = START
    is_game_over = False
    # global block_map, block_init_pos_map, block_stack, kick_map
    # global block_lock
    # global block_color, block_type, block_rotation
    # global block_y_pos, block_x_pos
    # global score
    # screen_height, screen_width = stdscr.getmaxyx()
    # screen_height_mid = screen_height // 2
    # screen_width_mid = screen_width // 2
    box_top_left = (box_top_left_x, box_top_left_y)  # (y, x)
    # box inside height * width = (20 ,10)
    box_bottom_right = ((31 - box_top_left[0]), (21 - box_top_left[1]))
    _rectangle(stdscr, box_top_left[0], box_top_left[1], box_bottom_right[0], box_bottom_right[1])

    # define box inside
    # box_in_top_left[0] <= y <= box_in_bottom_right[0]
    # box_in_top_left[1] <= x <= box_in_bottom_right[1]
    box_in_top_left = (box_top_left[0] + 1, box_top_left[1] + 1)  # y, x
    box_in_bottom_right = (box_bottom_right[0] - 1, box_bottom_right[1] - 1)  # y, x

    mod_block.set_curses_color()
    # set border color pair
    curses.init_pair(20, curses.COLOR_WHITE, curses.COLOR_WHITE)
    # set block empty color
    curses.init_pair(21, curses.COLOR_BLACK, curses.COLOR_BLACK)

    config.block_map = mod_block.get_total_blocks()
    config.block_init_pos_map = mod_block.get_block_init_position(
        box_in_top_left[0], (box_in_bottom_right[1] + box_in_top_left[1]) // 2
    )
    config.kick_map = mod_block.get_kick_map()

    # set block stack
    _set_block_stack(box_in_top_left, box_in_bottom_right)

    _draw_block_stack(stdscr, box_in_top_left, box_in_bottom_right)

    # score
    _set_score(stdscr, 0)

    # set status
    _set_status(stdscr, "START")

    # set block
    _set_block()

    _draw_block(
        stdscr,
        (config.block_type, config.block_rotation),
        (config.block_type, config.block_rotation),
        curses.color_pair(config.block_color),
        (config.block_y_pos, config.block_x_pos),
        (config.block_y_pos, config.block_x_pos),
    )

    while 1:
        key = stdscr.getch()
        if game_status == START and key == KEY_S:
            stdscr.nodelay(0)
            game_status = STOP
            _set_status(stdscr, "STOP")
            continue

        elif game_status == STOP and key == KEY_S:
            stdscr.nodelay(1)
            stdscr.timeout(game_timeout)
            game_status = START
            _set_status(stdscr, "START")
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
            stdscr.timeout(INITIAL_TIMEOUT)
            # status
            game_status = START
            _set_status(stdscr, "START")

            # reset block_stack
            _set_block_stack(box_in_top_left, box_in_bottom_right)

            # reset block
            _set_block()
            config.block_lock = False

            # draw border
            _rectangle(stdscr, box_top_left[0], box_top_left[1], box_bottom_right[0], box_bottom_right[1])
            # draw block_stack
            _draw_block_stack(stdscr, box_in_top_left, box_in_bottom_right)
            # draw new block
            _draw_block(
                stdscr,
                (config.block_type, config.block_rotation),
                (config.block_type, config.block_rotation),
                curses.color_pair(config.block_color),
                (config.block_y_pos, config.block_x_pos),
                (config.block_y_pos, config.block_x_pos),
            )
            # reset score
            _set_score(stdscr, 0)
            continue

        if game_status == STOP:
            continue

        if key == -1:  # not input
            key = curses.KEY_DOWN  # default block direction

        if key == curses.KEY_RIGHT:
            # move right
            block_pos_next = _move_block(
                box_in_top_left,
                box_in_bottom_right,
                (config.block_type, config.block_rotation),
                (config.block_y_pos, config.block_x_pos),
                (config.block_y_pos, config.block_x_pos + 1),
            )
            _draw_block(
                stdscr,
                (config.block_type, config.block_rotation),
                (config.block_type, config.block_rotation),
                curses.color_pair(config.block_color),
                (config.block_y_pos, config.block_x_pos),
                block_pos_next,
            )
            config.block_x_pos = block_pos_next[1]
        elif key == curses.KEY_LEFT:
            # move left
            block_pos_next = _move_block(
                box_in_top_left,
                box_in_bottom_right,
                (config.block_type, config.block_rotation),
                (config.block_y_pos, config.block_x_pos),
                (config.block_y_pos, config.block_x_pos - 1),
            )
            _draw_block(
                stdscr,
                (config.block_type, config.block_rotation),
                (config.block_type, config.block_rotation),
                curses.color_pair(config.block_color),
                (config.block_y_pos, config.block_x_pos),
                block_pos_next,
            )
            config.block_x_pos = block_pos_next[1]
        elif key == curses.KEY_DOWN:
            # move down
            block_pos_next = _move_block(
                box_in_top_left,
                box_in_bottom_right,
                (config.block_type, config.block_rotation),
                (config.block_y_pos, config.block_x_pos),
                (config.block_y_pos + 1, config.block_x_pos),
            )

            _draw_block(
                stdscr,
                (config.block_type, config.block_rotation),
                (config.block_type, config.block_rotation),
                curses.color_pair(config.block_color),
                (config.block_y_pos, config.block_x_pos),
                block_pos_next,
            )

            if config.block_y_pos == block_pos_next[0] and not config.block_lock:
                config.block_lock = True
            config.block_y_pos = block_pos_next[0]
        elif key == KEY_SPACE:
            # directly move down to block stack
            block_pos_next = _block_pos_in_block_stack(
                box_in_top_left,
                box_in_bottom_right,
                (config.block_type, config.block_rotation),
                (config.block_y_pos, config.block_x_pos),
            )
            _draw_block(
                stdscr,
                (config.block_type, config.block_rotation),
                (config.block_type, config.block_rotation),
                curses.color_pair(config.block_color),
                (config.block_y_pos, config.block_x_pos),
                block_pos_next,
            )
            config.block_y_pos = block_pos_next[0]

            # avoid another new block to fall fast
            if not config.block_lock:
                config.block_lock = True
        elif key == curses.KEY_UP:
            block_rotation_next = 0 if config.block_rotation == 3 else config.block_rotation + 1
            # rotate collision with block stack
            block_pos_next = _rotate_block(
                (1, 1 if BLOCK_TYPE_I != config.block_type else 2),
                box_in_top_left,
                box_in_bottom_right,
                config.block_rotation,
                (config.block_type, block_rotation_next),
                (config.block_y_pos, config.block_x_pos),
            )
            block_rotation_next = block_pos_next[2]
            _draw_block(
                stdscr,
                (config.block_type, config.block_rotation),
                (config.block_type, block_rotation_next),
                curses.color_pair(config.block_color),
                (config.block_y_pos, config.block_x_pos),
                (block_pos_next[0], block_pos_next[1]),
            )
            config.block_rotation = block_rotation_next
            config.block_y_pos = block_pos_next[0]
            config.block_x_pos = block_pos_next[1]
        elif key == KEY_Z:
            block_rotation_next = 3 if (config.block_rotation == 0) else config.block_rotation - 1
            # rotate collide block stack
            block_pos_next = _rotate_block(
                (2, 1 if BLOCK_TYPE_I != config.block_type else 2),
                box_in_top_left,
                box_in_bottom_right,
                config.block_rotation,
                (config.block_type, block_rotation_next),
                (config.block_y_pos, config.block_x_pos),
            )
            block_rotation_next = block_pos_next[2]
            _draw_block(
                stdscr,
                (config.block_type, config.block_rotation),
                (config.block_type, block_rotation_next),
                curses.color_pair(config.block_color),
                (config.block_y_pos, config.block_x_pos),
                (block_pos_next[0], block_pos_next[1]),
            )
            config.block_rotation = block_rotation_next
            config.block_y_pos = block_pos_next[0]
            config.block_x_pos = block_pos_next[1]
        else:
            continue

        # if DROP DONE
        if config.block_lock:
            # merge block stack
            after_erged_score = _merge_block_stack(
                stdscr,
                box_in_top_left,
                box_in_bottom_right,
                (config.block_type, config.block_rotation),
                (config.block_y_pos, config.block_x_pos),
                curses.color_pair(config.block_color),
            )

            # update score
            config.score += after_erged_score
            _set_score(stdscr, config.score)

            # define next block
            block_init_pos = _set_block()

            # check if game over
            is_game_over = _is_game_over(
                box_in_top_left, (config.block_type, config.block_rotation), (config.block_y_pos, config.block_x_pos)
            )

            if is_game_over:
                # update game status
                # stop game
                stdscr.nodelay(0)
                game_status = STOP
                _set_status(stdscr, "OVER")

                # draw part of block
                _draw_block_if_game_over(
                    stdscr,
                    (config.block_type, config.block_rotation),
                    curses.color_pair(config.block_color),
                    block_init_pos,
                )

            else:
                # draw next new block
                _draw_block(
                    stdscr,
                    (config.block_type, config.block_rotation),
                    (config.block_type, config.block_rotation),
                    curses.color_pair(config.block_color),
                    block_init_pos,
                    block_init_pos,
                )
                config.block_lock = False


def _set_status(stdscr, status: str):
    status_text = "Status: {} ".format(status)
    stdscr.addstr(*STATUS_POS, status_text)


def _set_score(stdscr, score: int):
    score_text = "Score: {}".format(score)
    stdscr.addstr(*SCORE_POS, score_text)


def _set_block_stack(box_in_top_left: tuple, box_in_bottom_right: tuple):
    # global block_stack
    config.block_stack = [
        [
            (_block_y, _block_x, BLOCK_EMPTY, curses.color_pair(21))
            for _block_x in range(box_in_top_left[1], box_in_bottom_right[1] + 1)
        ]
        for _block_y in range(box_in_top_left[0], box_in_bottom_right[0] + 1)
    ]


def _set_block() -> tuple:
    # global block_init_pos_map, block_y_pos, block_x_pos
    # global block_color, block_type, block_type, block_rotation
    config.block_color = choice(range(*COLOR_PAIR_RANGE))
    config.block_type = choice(range(*BLOCK_TYPE_RANGE))
    config.block_rotation = choice(range(*BLOCK_ROTATION_RANGE))
    block_init_pos = config.block_init_pos_map[config.block_type][config.block_rotation]
    config.block_y_pos = block_init_pos[0]  # block(5x5) top left y
    config.block_x_pos = block_init_pos[1]  # block(5x5) top left x
    return block_init_pos


def _draw_block_stack(stdscr, box_in_top_left: tuple, box_in_bottom_right: tuple):
    for _idx_y in range(0, box_in_bottom_right[0] + 1 - box_in_top_left[0]):
        for _idx_x in range(0, box_in_bottom_right[1] + 1 - box_in_top_left[1]):
            _block = config.block_stack[_idx_y][_idx_x]
            stdscr.addstr(_block[0], _block[1], str(_block[2]), _block[3])


def _draw_block(
    stdscr, block_setup: tuple, block_setup_next: tuple, block_color, block_pos: tuple, block_pos_next: tuple
):
    _block_type = block_setup[0]
    _block_rotation = block_setup[1]
    _block_rotation_next = block_setup_next[1]
    _block = config.block_map[_block_type][_block_rotation]
    _block_next = config.block_map[_block_type][_block_rotation_next]
    _block_len = len(_block)  # as the same as length of block_next

    # clear previous block
    for _y in range(_block_len):
        for _x in range(_block_len):
            if _block[_y][_x] > BLOCK_EMPTY:
                stdscr.addstr(block_pos[0] + _y, block_pos[1] + _x, str(BLOCK_EMPTY), curses.color_pair(21))
    # add next block
    for _y in range(_block_len):
        for _x in range(_block_len):
            if _block_next[_y][_x] > BLOCK_EMPTY:
                stdscr.addstr(block_pos_next[0] + _y, block_pos_next[1] + _x, str(_block_next[_y][_x]), block_color)


def _draw_block_if_game_over(stdscr, block_setup: tuple, block_color, block_pos: tuple):

    _block_type = block_setup[0]
    _block_rotation = block_setup[1]
    _block = config.block_map[_block_type][_block_rotation]
    _block_len = len(_block)

    for _y in range(_block_len):
        for _x in range(_block_len):
            if _block[_y][_x] > BLOCK_EMPTY:
                stdscr.addstr(block_pos[0] + _y, block_pos[1] + _x, str(_block[_y][_x]), block_color)


def _block_pos_in_block_stack(
    box_in_top_left: tuple,
    box_in_bottom_right: tuple,
    block_setup: tuple,
    block_pos: tuple,
) -> tuple:
    _block_type = block_setup[0]
    _block_rotation = block_setup[1]
    _block_x_pos_next = block_pos[1]
    _block_y_pos_next = block_pos[0]
    _step_limit = box_in_bottom_right[0] - box_in_top_left[0] + 1

    for _step_y in range(0, _step_limit):
        _block_y_pos_next = block_pos[0] + _step_y
        _moving_test = _is_block_pos_overlap(
            box_in_top_left,
            box_in_bottom_right,
            (_block_type, _block_rotation),
            (_block_y_pos_next, _block_x_pos_next),
        )
        if _moving_test:
            break

    _block_y_pos_next = block_pos[0] if _block_y_pos_next == block_pos[0] else _block_y_pos_next - 1
    return (_block_y_pos_next, _block_x_pos_next)


def _move_block(
    box_in_top_left: tuple,
    box_in_bottom_right: tuple,
    block_setup: tuple,
    block_pos: tuple,
    block_pos_next: tuple,
):
    _block_type = block_setup[0]
    _block_rotation = block_setup[1]
    _block_y_pos_next = block_pos_next[0]
    _block_x_pos_next = block_pos_next[1]

    _moving_test = _is_block_pos_overlap(
        box_in_top_left,
        box_in_bottom_right,
        (_block_type, _block_rotation),
        (_block_y_pos_next, _block_x_pos_next),
    )
    if not _moving_test:
        return block_pos_next

    return block_pos


def _rotate_block(
    rotation_key: tuple,
    box_in_top_left: tuple,
    box_in_bottom_right: tuple,
    block_rotation: int,
    block_setup: tuple,
    block_pos_next: tuple,
) -> tuple:
    _block_type = block_setup[0]
    _block_rotation_next = block_setup[1]
    _block_y_pos_next = block_pos_next[0]
    _block_x_pos_next = block_pos_next[1]
    _variant_pos = config.kick_map[(rotation_key[0], rotation_key[1])][_block_rotation_next]
    WALL_KICK_TEST_NUM = 5

    for test in range(WALL_KICK_TEST_NUM):
        _rotatation_test = _is_block_pos_overlap(
            box_in_top_left,
            box_in_bottom_right,
            (_block_type, _block_rotation_next),
            (_block_y_pos_next - _variant_pos[test][1], _block_x_pos_next + _variant_pos[test][0]),
        )
        if not _rotatation_test:
            return (
                _block_y_pos_next - _variant_pos[test][1],
                _block_x_pos_next + _variant_pos[test][0],
                _block_rotation_next,
            )
    return (_block_y_pos_next, _block_x_pos_next, block_rotation)


def _is_game_over(box_in_top_left: tuple, block_setup: tuple, block_pos: tuple) -> bool:
    _block_type = block_setup[0]
    _block_rotation = block_setup[1]
    _block = config.block_map[_block_type][_block_rotation]
    _block_len = len(_block)
    _block_y_pos = block_pos[0]
    _block_x_pos = block_pos[1]
    for _y in range(_block_len):
        for _x in range(_block_len):
            if _block[_y][_x] > BLOCK_EMPTY and (
                config.block_stack[_block_y_pos + _y - box_in_top_left[0]][_block_x_pos + _x - box_in_top_left[1]][2]
                > BLOCK_EMPTY
            ):
                return True

    return False


def _is_block_pos_overlap(
    box_in_top_left: tuple,
    box_in_bottom_right: tuple,
    block_setup: tuple,
    block_pos_next: tuple,
):
    _block_type = block_setup[0]
    _block_rotation_next = block_setup[1]
    _block_next = config.block_map[_block_type][_block_rotation_next]
    _block_len = len(_block_next)
    _block_y_pos_next = block_pos_next[0]
    _block_x_pos_next = block_pos_next[1]

    # check if it overlaps border/block stack
    for _y in range(_block_len):
        for _x in range(_block_len):
            if _block_next[_y][_x] > BLOCK_EMPTY and (
                box_in_top_left[0] > (_block_y_pos_next + _y)
                or box_in_top_left[1] > (_block_x_pos_next + _x)
                or box_in_bottom_right[0] < (_block_y_pos_next + _y)
                or box_in_bottom_right[1] < (_block_x_pos_next + _x)
                or config.block_stack[_block_y_pos_next + _y - box_in_top_left[0]][
                    _block_x_pos_next + _x - box_in_top_left[1]
                ][2]
                > BLOCK_EMPTY
            ):
                return True

    return False


def _merge_block_stack(
    stdscr, box_in_top_left: tuple, box_in_bottom_right: tuple, block_setup: tuple, block_pos: tuple, block_color
):
    _block_type = block_setup[0]
    _block_rotation = block_setup[1]
    _block = config.block_map[_block_type][_block_rotation]
    _block_len = len(_block)
    _block_y_pos = block_pos[0]
    _block_x_pos = block_pos[1]
    _score_line = 0
    # merge block into block stack
    for _y in range(_block_len):
        for _x in range(_block_len):
            _temp_y = _block_y_pos + _y - box_in_top_left[0]
            _temp_x = _block_x_pos + _x - box_in_top_left[1]

            if _block[_y][_x] > BLOCK_EMPTY and (config.block_stack[_temp_y][_temp_x][2] == BLOCK_EMPTY):

                """
                tuple does not support item assignment
                it needs another new tuple to udpate
                """
                config.block_stack[_temp_y][_temp_x] = (
                    _temp_y + box_in_top_left[0],
                    _temp_x + box_in_top_left[1],
                    BLOCK_FILLED,
                    block_color,
                )

    # if any the possible lines to be deleted
    # delete and move down - deleted blocks to new position
    # repeat (until it has no possible lines)
    _block_stack_x_end = box_in_bottom_right[1] + 1 - box_in_top_left[1]
    _line_x_num = 0
    _dy = box_in_bottom_right[0]
    while _dy > box_in_top_left[0]:
        for _dx in range(0, _block_stack_x_end):
            if config.block_stack[_dy - box_in_top_left[0]][_dx][2] > BLOCK_EMPTY:
                _line_x_num += 1

        if _line_x_num == _block_stack_x_end:
            _score_line += 1
            for _y in range(_dy, box_in_top_left[0], -1):
                for _x in range(0, _block_stack_x_end):
                    _moved_temp = config.block_stack[_y - box_in_top_left[0] - 1][_x]
                    # move down
                    config.block_stack[_y - box_in_top_left[0]][_x] = (
                        _y,
                        _moved_temp[1],
                        _moved_temp[2],
                        _moved_temp[3],
                    )
                    # clear original
                    config.block_stack[_y - box_in_top_left[0] - 1][_x] = (
                        _moved_temp[0],
                        _moved_temp[1],
                        BLOCK_EMPTY,
                        curses.color_pair(21),
                    )
        else:
            _dy -= 1
        _line_x_num = 0

    # draw block stack after deleting and moving down
    for _idx_y in range(0, box_in_bottom_right[0] + 1 - box_in_top_left[0]):
        for _idx_x in range(0, box_in_bottom_right[1] + 1 - box_in_top_left[1]):
            _block = config.block_stack[_idx_y][_idx_x]
            stdscr.addstr(_block[0], _block[1], str(_block[2]), _block[3])

    return _score_line


def _rectangle(stdscr, uly, ulx, lry, lrx):
    """
    Draw a rectangle with corners at the provided upper-left
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


def tetris_entry():
    curses.wrapper(_game)


if __name__ == "__main__":
    tetris_entry()
