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
KEY_DOWN: soft drop (moving speed + 20%)
SPACE: hard drop
s: pause/resume
check collisions with border/block when blocks move/rotate
check blocks land and a new block(which is drawn) in random is ready
check the complete horizontal blocks and erase (score)
check "Over" when blocks hit(or beyond) upper horizontal border
draw blocks
"""

TETRIS_GAME = 2
BLOCK_EMPTY = 0
BLOCK_FILLED = 1
# 2 is a moving block pivot
BORDER = 3


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
    KEY_SPACE = 32  # hard drop
    KEY_S = 115  # "s" pause/resume
    KEY_Z = 122  # "z" rotate couterclockwise
    KEY_ENTER = 10  # reset (restart)
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
    # curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
    # stdscr.attron(curses.color_pair(13))
    color_pair_range = (11, 16)
    block_color = choice(range(*color_pair_range))
    block_type_range = (0, 7)
    block_type = choice(range(*block_type_range))
    block_rotation_range = (0, 4)
    block_rotation = choice(range(*block_rotation_range))
    game_status = START
    block_map = mod_block.get_total_blocks()
    block_init_pos_map = mod_block.get_block_init_position(
        box_in_top_left[0], (box_in_bottom_right[1] + box_in_top_left[1]) // 2
    )
    block_dir = -1  # nothing
    # BLOCK_EMPTY = 0
    # BLOCK_FILLED = 1
    global block_stack
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

    # stdscr.addch(box_in_top_left[0], box_in_top_left[1], "O", curses.color_pair(13))
    # stdscr.addch(box_in_bottom_right[0], box_in_top_left[1], "O", curses.color_pair(13))
    # stdscr.addch(box_in_top_left[0], box_in_bottom_right[1], "O", curses.color_pair(13))
    # stdscr.addch(box_in_bottom_right[0], box_in_bottom_right[1], "O", curses.color_pair(13))

    # draw block_stack
    for _idx_y in range(0, box_in_bottom_right[0] + 1 - box_in_top_left[0]):
        for _idx_x in range(0, box_in_bottom_right[1] + 1 - box_in_top_left[1]):
            _block = block_stack[_idx_y][_idx_x]
            stdscr.addstr(_block[0], _block[1], str(_block[2]), _block[3])

    stdscr.addstr(box_in_top_left[0] + 10, box_in_top_left[1] + 2, "11111", curses.color_pair(13))

    block = block_map[block_type][block_rotation]
    block_init_pos = block_init_pos_map[block_type][block_rotation]
    block_y_pos = block_init_pos[0]  # block(5x5) top left y
    block_x_pos = block_init_pos[1]  # block(5x5) top left x

    _draw_block(
        stdscr, block, block, curses.color_pair(block_color), (block_y_pos, block_x_pos), (block_y_pos, block_x_pos)
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
            # check collide(move in block and move border)
            # move right

            _draw_block(
                stdscr,
                block,
                block,
                curses.color_pair(block_color),
                (block_y_pos, block_x_pos),
                (block_y_pos, block_x_pos + 1),
            )
            block_x_pos = block_x_pos + 1
            # merge
            # check delete line
            pass
        elif key == curses.KEY_LEFT:
            # check collide(move in block and move border)
            # move left

            _draw_block(
                stdscr,
                block,
                block,
                curses.color_pair(block_color),
                (block_y_pos, block_x_pos),
                (block_y_pos, block_x_pos - 1),
            )
            block_x_pos = block_x_pos - 1
            # merge
            # check delete line
            pass
        elif key == curses.KEY_DOWN:
            # speed down (stdscr.timeout(game_timeout))
            # collide (move in block and move border)
            # move down
            # k_left = stdscr.instr(3, screen_width_mid - len(status_text) // 2 + 1, 1)
            # k_right = stdscr.instr(3, screen_width_mid - len(status_text) // 2 + 1, 1)
            # k_bottom = stdscr.instr(3, screen_width_mid - len(status_text) // 2 + 1, 1)
            _draw_block(
                stdscr,
                block,
                block,
                curses.color_pair(block_color),
                (block_y_pos, block_x_pos),
                (block_y_pos + 1, block_x_pos),
            )
            block_y_pos = block_y_pos + 1
            # merge
            # check delete line
            pass
        elif key == KEY_SPACE:
            # collide (move in block and move border)
            # merge
            # check delete line
            pass
        elif key == curses.KEY_UP:
            block_rotation = 0 if block_rotation == 3 else block_rotation + 1
            block_next = block_map[block_type][block_rotation]
            # rotate
            block_pos_next = _rotate_block(box_in_top_left, box_in_bottom_right, block_next, (block_y_pos, block_x_pos))
            _draw_block(
                stdscr,
                block,
                block_next,
                curses.color_pair(block_color),
                (block_y_pos, block_x_pos),
                (block_pos_next[0], block_pos_next[1]),
            )
            block = block_next
            block_y_pos = block_pos_next[0]
            block_x_pos = block_pos_next[1]
            # merge
            # check delete line
            pass
        elif key == KEY_Z:
            # check collide(rotate in block)
            # rotate
            block_rotation = 3 if (block_rotation == 0) else block_rotation - 1
            block_next = block_map[block_type][block_rotation]
            block_pos_next = _rotate_block(box_in_top_left, box_in_bottom_right, block_next, (block_y_pos, block_x_pos))
            _draw_block(
                stdscr,
                block,
                block_next,
                curses.color_pair(block_color),
                (block_y_pos, block_x_pos),
                (block_pos_next[0], block_pos_next[1]),
            )
            block = block_next
            block_y_pos = block_pos_next[0]
            block_x_pos = block_pos_next[1]
            # merge
            # check delete line
            pass
        else:
            continue

        """
        # define next block
        block_color = _random_choice_next(block_color, *color_pair_range)
        block_type = _random_choice_next(block_type, *block_type_range)
        block_rotation = _random_choice_next(block_rotation, *block_rotation_range)
        block = block_map[block_type][block_rotation]
        block_init_pos = block_init_pos_map[block_type][block_rotation]
        """
        # if game over (still draw next block if necessary)
        # if not game over then draw block
        # if delete line then update score


def _draw_block(stdscr, block, block_next, block_color, block_pos: tuple, block_pos_next: tuple):
    block_len = len(block)  # as the same as length of block_next
    # clear previous block
    for _y in range(block_len):
        for _x in range(block_len):
            if block[_y][_x] > 0:
                stdscr.addstr(block_pos[0] + _y, block_pos[1] + _x, str(BLOCK_EMPTY), curses.color_pair(21))
    # add next block
    for _y in range(block_len):
        for _x in range(block_len):
            if block_next[_y][_x] > 0:
                stdscr.addstr(block_pos_next[0] + _y, block_pos_next[1] + _x, str(block_next[_y][_x]), block_color)


def _rotate_block(box_in_top_left, box_in_bottom_right, block_next, block_pos_next):
    _block_len = len(block_next)
    _block_y_pos_next = block_pos_next[0]
    _block_x_pos_next = block_pos_next[1]
    for _y in range(_block_len):
        for _x in range(_block_len):
            # check top
            if block_next[_y][_x] > 0 and _block_y_pos_next + _y == box_in_top_left[0] - 2:
                _block_y_pos_next = _block_y_pos_next + 2
            elif block_next[_y][_x] > 0 and _block_y_pos_next + _y == box_in_top_left[0] - 1:
                _block_y_pos_next = _block_y_pos_next + 1
            # check bottom
            elif block_next[_y][_x] > 0 and _block_y_pos_next + _y == box_in_bottom_right[0] + 2:
                _block_y_pos_next = _block_y_pos_next - 2
            elif block_next[_y][_x] > 0 and _block_y_pos_next + _y == box_in_bottom_right[0] + 1:
                _block_y_pos_next = _block_y_pos_next - 1
            # check left
            elif block_next[_y][_x] > 0 and _block_x_pos_next + _x == box_in_top_left[1] - 2:
                _block_x_pos_next = _block_x_pos_next + 2
            elif block_next[_y][_x] > 0 and _block_x_pos_next + _x == box_in_top_left[1] - 1:
                _block_x_pos_next = _block_x_pos_next + 1
            # check right
            elif block_next[_y][_x] > 0 and _block_x_pos_next + _x == box_in_bottom_right[1] + 2:
                _block_x_pos_next = _block_x_pos_next - 2
            elif block_next[_y][_x] > 0 and _block_x_pos_next + _x == box_in_bottom_right[1] + 1:
                _block_x_pos_next = _block_x_pos_next - 1
    return (_block_y_pos_next, _block_x_pos_next)


def _delete_line(n_lines: int):
    # delete n lines
    # move down y (n lines) which are not deleted
    pass


def _move_down(stdscr, block, block_y, block_x, block_color):
    # _draw_block(stdscr, block, block_y + 1, block_x, block_color)
    # _draw_block(stdscr, block, block_y, block_x, block_color)
    pass


def _rectangle(stdscr, uly, ulx, lry, lrx):
    """Draw a rectangle with corners at the provided upper-left
    and lower-right coordinates.
    """
    stdscr.attron(curses.color_pair(20))
    stdscr.vline(uly + 1, ulx, str(BORDER), lry - uly - 1)
    stdscr.hline(uly, ulx + 1, str(BORDER), lrx - ulx - 1)
    stdscr.hline(lry, ulx + 1, str(BORDER), lrx - ulx - 1)
    stdscr.vline(uly + 1, lrx, str(BORDER), lry - uly - 1)
    stdscr.addch(uly, ulx, curses.ACS_ULCORNER)  # top left corner
    stdscr.addch(uly, lrx, curses.ACS_URCORNER)  # top right corner
    stdscr.addch(lry, lrx, curses.ACS_LRCORNER)  # bottom right corner
    stdscr.addch(lry, ulx, curses.ACS_LLCORNER)  # bottom left corner
    # stdscr.vline(uly + 1, ulx, curses.ACS_VLINE, lry - uly - 1)
    # stdscr.hline(uly, ulx + 1, curses.ACS_HLINE, lrx - ulx - 1)
    # stdscr.hline(lry, ulx + 1, curses.ACS_HLINE, lrx - ulx - 1)
    # stdscr.vline(uly + 1, lrx, curses.ACS_VLINE, lry - uly - 1)
    # stdscr.addch(uly, ulx, curses.ACS_ULCORNER)  # top left corner
    # stdscr.addch(uly, lrx, curses.ACS_URCORNER)  # top right corner
    # stdscr.addch(lry, lrx, curses.ACS_LRCORNER)  # bottom right corner
    # stdscr.addch(lry, ulx, curses.ACS_LLCORNER)  # bottom left corner
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
