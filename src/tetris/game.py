import curses
from random import randint, choice, random

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
SPACE: sonic drop
s: pause/resume

support:
1.Wall kick
2.Lock delay (when soft drop/hard drop)

"""

TETRIS_GAME = 2
BLOCK_EMPTY = 0
BLOCK_FILLED = 1
# 2 is a moving block pivot

KEY_ESC = 27  # exit
KEY_SPACE = 32  # hard drop
KEY_S = 115  # "s" pause/resume
KEY_Z = 122  # "z" rotate couterclockwise
KEY_ENTER = 10  # reset (restart)

ROTATION_CLOCKWISE = 1
ROTATION_COUNTERCLOCKWISE = 2
BLOCK_TYPE_I = 1  # I block

block_stack = []
block_map = []
block_init_pos_map = []
kick_map = {}


def _game(stdscr):

    # initial setting
    curses.curs_set(0)
    stdscr.nodelay(1)
    INITIAL_TIMEOUT = 700
    game_timeout = INITIAL_TIMEOUT
    stdscr.timeout(game_timeout)
    box_top_left_x = 5
    box_top_left_y = 5
    START = 1
    STOP = 0
    BOX_SCALE = 2
    screen_height, screen_width = stdscr.getmaxyx()
    screen_height_mid = screen_height // 2
    screen_width_mid = screen_width // 2
    box_top_left = (box_top_left_x, box_top_left_y)  # (y, x)
    # box_bottom_right = ((screen_height - box_top_left[0]) // BOX_SCALE, (screen_width - box_top_left[1]) // BOX_SCALE)
    # box inside height * width = (20 ,10)
    box_bottom_right = ((31 - box_top_left[0]), (21 - box_top_left[1]))
    box = (box_bottom_right[0] - box_top_left[0], box_bottom_right[1] - box_top_left[1])  # box height, width
    # textpad.rectangle(stdscr, box_top_left[0], box_top_left[1], box_bottom_right[0], box_bottom_right[1])
    _rectangle(stdscr, box_top_left[0], box_top_left[1], box_bottom_right[0], box_bottom_right[1])

    # define box inside
    # box_in_top_left[0] <= y <= box_in_bottom_right[0]
    # box_in_top_left[1] <= x <= box_in_bottom_right[1]
    box_in_top_left = (box_top_left[0] + 1, box_top_left[1] + 1)  # y, x
    box_in_bottom_right = (box_bottom_right[0] - 1, box_bottom_right[1] - 1)  # y, x

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
    # curses.init_pair(16, 16, 16)  # INDIGO
    # curses.init_pair(17, 17, 17)  # VIOLET
    # set border color pair
    curses.init_pair(20, curses.COLOR_WHITE, curses.COLOR_WHITE)
    # set block empty color
    curses.init_pair(21, curses.COLOR_BLACK, curses.COLOR_BLACK)

    color_pair_range = (11, 16)
    block_color = choice(range(*color_pair_range))
    block_type_range = (0, 7)
    block_type = choice(range(*block_type_range))
    block_rotation_range = (0, 4)
    block_rotation = choice(range(*block_rotation_range))
    game_status = START
    is_game_over = False
    global block_map, block_init_pos_map, block_stack, kick_map
    block_map = mod_block.get_total_blocks()
    block_init_pos_map = mod_block.get_block_init_position(
        box_in_top_left[0], (box_in_bottom_right[1] + box_in_top_left[1]) // 2
    )
    kick_map = mod_block.get_kick_map()
    block_dir = curses.KEY_DOWN
    block_stack = [
        [
            (_block_y, _block_x, BLOCK_EMPTY, curses.color_pair(21))
            for _block_x in range(box_in_top_left[1], box_in_bottom_right[1] + 1)
        ]
        for _block_y in range(box_in_top_left[0], box_in_bottom_right[0] + 1)
    ]

    # status_text = "Status: {}".format("START")
    # stdscr.addstr(3, screen_width_mid - len(status_text) // 2, status_text)
    # stdscr.attroff(curses.color_pair(13))

    # draw block_stack
    for _idx_y in range(0, box_in_bottom_right[0] + 1 - box_in_top_left[0]):
        for _idx_x in range(0, box_in_bottom_right[1] + 1 - box_in_top_left[1]):
            _block = block_stack[_idx_y][_idx_x]
            stdscr.addstr(_block[0], _block[1], str(_block[2]), _block[3])

    # test block
    for _x in range(5):
        block_stack[10][_x + 2] = (block_stack[10][_x + 2][0], block_stack[10][_x + 2][1], 1, curses.color_pair(13))
        block_stack[12][_x + 2] = (block_stack[12][_x + 2][0], block_stack[10][_x + 2][1], 1, curses.color_pair(13))
        stdscr.addstr(
            block_stack[10][_x + 2][0],
            block_stack[10][_x + 2][1],
            str(block_stack[10][_x + 2][2]),
            block_stack[10][_x + 2][3],
        )
        stdscr.addstr(
            block_stack[12][_x + 2][0],
            block_stack[12][_x + 2][1],
            str(block_stack[12][_x + 2][2]),
            block_stack[12][_x + 2][3],
        )

    block_init_pos = block_init_pos_map[block_type][block_rotation]
    block_y_pos = block_init_pos[0]  # block(5x5) top left y
    block_x_pos = block_init_pos[1]  # block(5x5) top left x

    _draw_block(
        stdscr,
        (block_type, block_rotation),
        (block_type, block_rotation),
        curses.color_pair(block_color),
        (block_y_pos, block_x_pos),
        (block_y_pos, block_x_pos),
    )

    while 1:
        key = stdscr.getch()
        if game_status == START and key == KEY_S:
            stdscr.nodelay(0)
            game_status = STOP
            status_text = "Status: {}".format("STOP ")
            stdscr.addstr(3, screen_width_mid - len(status_text) // 2, status_text)
            continue

        elif game_status == STOP and key == KEY_S:
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

        if key == -1:  # not input
            key = block_dir

        # move down

        if key == curses.KEY_RIGHT:
            # move right
            block_pos_next = _move_block(
                box_in_top_left,
                box_in_bottom_right,
                (block_type, block_rotation),
                (block_y_pos, block_x_pos),
                (block_y_pos, block_x_pos + 1),
            )

            _draw_block(
                stdscr,
                (block_type, block_rotation),
                (block_type, block_rotation),
                curses.color_pair(block_color),
                (block_y_pos, block_x_pos),
                block_pos_next,
            )
            block_x_pos = block_pos_next[1]
        elif key == curses.KEY_LEFT:
            # move left
            block_pos_next = _move_block(
                box_in_top_left,
                box_in_bottom_right,
                (block_type, block_rotation),
                (block_y_pos, block_x_pos),
                (block_y_pos, block_x_pos - 1),
            )

            _draw_block(
                stdscr,
                (block_type, block_rotation),
                (block_type, block_rotation),
                curses.color_pair(block_color),
                (block_y_pos, block_x_pos),
                block_pos_next,
            )
            block_x_pos = block_pos_next[1]
        elif key == curses.KEY_DOWN:
            # move down
            block_pos_next = _move_block(
                box_in_top_left,
                box_in_bottom_right,
                (block_type, block_rotation),
                (block_y_pos, block_x_pos),
                (block_y_pos + 1, block_x_pos),
            )

            _draw_block(
                stdscr,
                (block_type, block_rotation),
                (block_type, block_rotation),
                curses.color_pair(block_color),
                (block_y_pos, block_x_pos),
                block_pos_next,
            )
            block_y_pos = block_pos_next[0]
        elif key == KEY_SPACE:
            # directly move down to block stack
            block_pos_next = _block_pos_in_block_stack(
                box_in_top_left,
                box_in_bottom_right,
                (block_type, block_rotation),
                (block_y_pos, block_x_pos),
            )
            _draw_block(
                stdscr,
                (block_type, block_rotation),
                (block_type, block_rotation),
                curses.color_pair(block_color),
                (block_y_pos, block_x_pos),
                block_pos_next,
            )
            block_y_pos = block_pos_next[0]
        elif key == curses.KEY_UP:
            block_rotation_next = 0 if block_rotation == 3 else block_rotation + 1
            # rotate collision with block stack
            block_pos_next = _rotate_block(
                (1, 1 if BLOCK_TYPE_I != block_type else 2),
                box_in_top_left,
                box_in_bottom_right,
                block_rotation,
                (block_type, block_rotation_next),
                (block_y_pos, block_x_pos),
            )
            block_rotation_next = block_pos_next[2]
            _draw_block(
                stdscr,
                (block_type, block_rotation),
                (block_type, block_rotation_next),
                curses.color_pair(block_color),
                (block_y_pos, block_x_pos),
                (block_pos_next[0], block_pos_next[1]),
            )
            block_rotation = block_rotation_next
            block_y_pos = block_pos_next[0]
            block_x_pos = block_pos_next[1]
        elif key == KEY_Z:
            block_rotation_next = 3 if (block_rotation == 0) else block_rotation - 1
            # rotate collide block stack
            block_pos_next = _rotate_block(
                (2, 1 if BLOCK_TYPE_I != block_type else 2),
                box_in_top_left,
                box_in_bottom_right,
                block_rotation,
                (block_type, block_rotation_next),
                (block_y_pos, block_x_pos),
            )
            # rotate collide block stack
            block_rotation_next = block_pos_next[2]
            _draw_block(
                stdscr,
                (block_type, block_rotation),
                (block_type, block_rotation_next),
                curses.color_pair(block_color),
                (block_y_pos, block_x_pos),
                (block_pos_next[0], block_pos_next[1]),
            )
            block_rotation = block_rotation_next
            block_y_pos = block_pos_next[0]
            block_x_pos = block_pos_next[1]
        else:
            continue

        # merge block stack
        # if delete line (and update score)

        # define next block
        # block_color = _random_choice_next(block_color, *color_pair_range)
        # block_type = _random_choice_next(block_type, *block_type_range)
        # block_rotation = _random_choice_next(block_rotation, *block_rotation_range)
        # block_init_pos = block_init_pos_map[block_type][block_rotation]
        # block_y_pos = block_init_pos[0]
        # block_x_pos = block_init_pos[1]
        # if game over (new block over top border)
        if False:
            is_game_over = True

        if is_game_over:
            # update game status
            # stop game
            # draw part of block
            _draw_block_if_game_over(
                stdscr, (block_type, block_rotation), curses.color_pair(block_color), block_init_pos
            )
        else:
            pass
            # if not game over (draw new block)
            # _draw_block(
            #     stdscr,
            #     (block_type, block_rotation),
            #     (block_type, block_rotation),
            #     curses.color_pair(block_color),
            #     block_init_pos,
            #     block_init_pos,
            # )


def _draw_block(
    stdscr, block_setup: tuple, block_setup_next: tuple, block_color, block_pos: tuple, block_pos_next: tuple
):
    _block_type = block_setup[0]
    _block_rotation = block_setup[1]
    _block_rotation_next = block_setup_next[1]
    _block = block_map[_block_type][_block_rotation]
    _block_next = block_map[_block_type][_block_rotation_next]
    _block_len = len(_block)  # as the same as length of block_next

    # clear previous block
    for _y in range(_block_len):
        for _x in range(_block_len):
            if _block[_y][_x] > 0:
                stdscr.addstr(block_pos[0] + _y, block_pos[1] + _x, str(BLOCK_EMPTY), curses.color_pair(21))
    # add next block
    for _y in range(_block_len):
        for _x in range(_block_len):
            if _block_next[_y][_x] > 0:
                stdscr.addstr(block_pos_next[0] + _y, block_pos_next[1] + _x, str(_block_next[_y][_x]), block_color)


def _draw_block_if_game_over(stdscr, box_in_top_left: tuple, block_setup: tuple, block_color, block_pos: tuple):

    _block_type = block_setup[0]
    _block_rotation = block_setup[1]
    _block = block_map[_block_type][_block_rotation]
    _block_len = len(_block)
    for _y in range(_block_len):
        for _x in range(_block_len):
            if (
                _block[_y][_x] > 0
                and block_map[block_pos[0] + _y][block_pos[1] + _x][2] == BLOCK_EMPTY
                and (block_pos[0] + _y > box_in_top_left[0])
            ):
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
    _step_limit = box_in_bottom_right[0] - box_in_top_left[0]

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
    _block_y_pos_next = _block_y_pos_next - 1 if _block_y_pos_next == block_pos[0] else _block_y_pos_next
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
    _variant_pos = kick_map[(rotation_key[0], rotation_key[1])][_block_rotation_next]
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


def _is_block_next_same(block_rotation, block_rotation_next, block_pos: tuple, block_pos_next: tuple):
    return block_rotation == block_rotation_next and block_pos == block_pos_next


def _is_block_pos_overlap(
    box_in_top_left: tuple,
    box_in_bottom_right: tuple,
    block_setup: tuple,
    block_pos_next: tuple,
):

    _block_type = block_setup[0]
    _block_rotation_next = block_setup[1]
    _block_next = block_map[_block_type][_block_rotation_next]
    _block_len = len(_block_next)
    _block_y_pos_next = block_pos_next[0]
    _block_x_pos_next = block_pos_next[1]

    # check if it overlaps border/block stack
    for _y in range(_block_len):
        for _x in range(_block_len):
            if _block_next[_y][_x] > 0 and (
                box_in_top_left[0] > (_block_y_pos_next + _y)
                or box_in_top_left[1] > (_block_x_pos_next + _x)
                or box_in_bottom_right[0] < (_block_y_pos_next + _y)
                or box_in_bottom_right[1] < (_block_x_pos_next + _x)
                or block_stack[_block_y_pos_next + _y - box_in_top_left[0]][
                    _block_x_pos_next + _x - box_in_top_left[1]
                ][2]
                > 0
            ):
                return True

    return False


def _merge_block_stack():
    pass


def _delete_line(n_lines: int):
    # delete n lines
    # move down y (n lines) which are not deleted
    pass


def _move_line_down(stdscr, block, block_y, block_x, block_color):
    # _draw_block(stdscr, block, block_y + 1, block_x, block_color)
    # _draw_block(stdscr, block, block_y, block_x, block_color)
    pass


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


# rgb 255 to 1000 curses color
def _rgb_255_to_1000(rgb_tuple: tuple) -> tuple:
    return tuple(rgb * 1000 // 255 for rgb in rgb_tuple)


def _random_choice_next(curr: int, start: int, end: int) -> int:
    # end is not included
    return choice([x for x in range(start, end) if x != curr])


def tetris_entry():
    curses.wrapper(_game)


if __name__ == "__main__":
    tetris_entry()
