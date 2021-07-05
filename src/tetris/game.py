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




1.Wall kick
2.Floor kick ???
3.Lock delay (when soft drop/hard drop)

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
BLOCK_I_INDEX = 1  # I block

block_stack = []
block_map = []


def _game(stdscr):

    # initial setting
    curses.curs_set(0)
    stdscr.nodelay(1)
    INITIAL_TIMEOUT = 100
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
    # curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
    # stdscr.attron(curses.color_pair(13))
    color_pair_range = (11, 16)
    block_color = choice(range(*color_pair_range))
    block_type_range = (0, 7)
    block_type = choice(range(*block_type_range))
    block_rotation_range = (0, 4)
    block_rotation = choice(range(*block_rotation_range))
    game_status = START
    global block_map, block_stack
    block_map = mod_block.get_total_blocks()
    block_init_pos_map = mod_block.get_block_init_position(
        box_in_top_left[0], (box_in_bottom_right[1] + box_in_top_left[1]) // 2
    )
    block_dir = -1  # nothing
    # BLOCK_EMPTY = 0
    # BLOCK_FILLED = 1
    # global block_stack
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
        elif key == curses.KEY_DOWN:
            # speed down (stdscr.timeout(game_timeout))
            # collide (move in block and move border)
            # move down
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
        elif key == KEY_SPACE:
            # collide (move in block and move border)
            # merge
            # check delete line
            pass
        elif key == curses.KEY_UP:
            block_rotation_next = 0 if block_rotation == 3 else block_rotation + 1
            block_next = block_map[block_type][block_rotation]
            # rotate
            block_pos_next = _rotate_block(
                (1, 1 if BLOCK_I_INDEX != block_rotation_next else 2),
                box_in_top_left,
                box_in_bottom_right,
                block_rotation_next,
                block_next,
                [block_y_pos, block_x_pos],
            )
            # rotate collision with block stack
            block_next = block_next if block_pos_next[2] else block
            _draw_block(
                stdscr,
                block,
                block_next,
                curses.color_pair(block_color),
                (block_y_pos, block_x_pos),
                (block_pos_next[0], block_pos_next[1]),
            )
            block = block_next
            block_rotation = block_rotation_next if block_pos_next[2] else block_rotation
            block_y_pos = block_pos_next[0]
            block_x_pos = block_pos_next[1]
            # merge
            # check delete line
        elif key == KEY_Z:
            # check collide(rotate in block)
            # rotate
            block_rotation = 3 if (block_rotation == 0) else block_rotation - 1
            block_next = block_map[block_type][block_rotation]
            block_pos_next = _rotate_block(
                (2, 1 if BLOCK_I_INDEX != block_rotation_next else 2),
                box_in_top_left,
                box_in_bottom_right,
                block_rotation_next,
                block_next,
                [block_y_pos, block_x_pos],
            )
            # rotate collide block stack
            block_next = block_next if block_pos_next[2] else block
            _draw_block(
                stdscr,
                block,
                block_next,
                curses.color_pair(block_color),
                (block_y_pos, block_x_pos),
                (block_pos_next[0], block_pos_next[1]),
            )
            block = block_next
            block_rotation = block_rotation_next if block_pos_next[2] else block_rotation
            block_y_pos = block_pos_next[0]
            block_x_pos = block_pos_next[1]
            # merge
            # check delete line
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


def _rotate_block(
    rotation_key: tuple, box_in_top_left, box_in_bottom_right, block_rotation_next, block_next, block_pos_next: tuple
) -> tuple:
    _block_len = len(block_next)
    _block_y_pos_next = block_pos_next[0]
    _block_x_pos_next = block_pos_next[1]
    global block_stack
    _rotation_test = [
        True,  # Test 1
        True,  # Test 2
        True,  # Test 3
        True,  # Test 4
        True,  # Test 5
    ]

    # rotate successfully -> one of _test_rotate_ is True
    # _block_y_pos_rotate = _block_y_pos_next
    # _block_x_pos_rotate = _block_x_pos_next
    # for _y in range(_block_len):
    #     for _x in range(_block_len):
    #         # top border (kick and move down)
    #         if block_next[_y][_x] > 0 and _block_y_pos_next + _y == box_in_top_left[0] - 2:
    #             _block_y_pos_rotate = _block_y_pos_rotate + 2
    #         elif block_next[_y][_x] > 0 and _block_y_pos_next + _y == box_in_top_left[0] - 1:
    #             _block_y_pos_rotate = _block_y_pos_rotate + 1
    #         # bottom border (kick and move up )
    #         elif block_next[_y][_x] > 0 and _block_y_pos_next + _y == box_in_bottom_right[0] + 2:
    #             _block_y_pos_rotate = _block_y_pos_rotate - 2
    #         elif block_next[_y][_x] > 0 and _block_y_pos_next + _y == box_in_bottom_right[0] + 1:
    #             _block_y_pos_rotate = _block_y_pos_rotate - 1
    #         # left border (kick and move right)
    #         elif block_next[_y][_x] > 0 and _block_x_pos_next + _x == box_in_top_left[1] - 2:
    #             _block_x_pos_rotate = _block_x_pos_rotate + 2
    #         elif block_next[_y][_x] > 0 and _block_x_pos_next + _x == box_in_top_left[1] - 1:
    #             _block_x_pos_rotate = _block_x_pos_rotate + 1
    #         # right border (kick and move left)
    #         elif block_next[_y][_x] > 0 and _block_x_pos_next + _x == box_in_bottom_right[1] + 2:
    #             _block_x_pos_rotate = _block_x_pos_rotate - 2
    #         elif block_next[_y][_x] > 0 and _block_x_pos_next + _x == box_in_bottom_right[1] + 1:
    #             _block_x_pos_rotate = _block_x_pos_rotate - 1

    # J, L, S, T, Z Tetromino Wall Kick Data
    # (x, y)
    # x>0 move right
    # y>0 move up
    # x<0 move left
    # y<0 move down
    #       Test 1	Test 2	Test 3	Test 4	Test 5
    # L->0	( 0, 0)	(-1, 0)	(-1,-1)	( 0,+2)	(-1,+2)
    # 0->R	( 0, 0)	(-1, 0)	(-1,+1)	( 0,-2)	(-1,-2)
    # R->2	( 0, 0)	(+1, 0)	(+1,-1)	( 0,+2)	(+1,+2)
    # 2->L	( 0, 0)	(+1, 0)	(+1,+1)	( 0,-2)	(+1,-2)

    # R->0	( 0, 0)	(+1, 0)	(+1,-1)	( 0,+2)	(+1,+2)
    # 2->R	( 0, 0)	(-1, 0)	(-1,+1)	( 0,-2)	(-1,-2)
    # L->2	( 0, 0)	(-1, 0)	(-1,-1)	( 0,+2)	(-1,+2)
    # 0->L	( 0, 0)	(+1, 0)	(+1,+1)	( 0,-2)	(+1,-2)

    # I Tetromino Wall Kick Data
    # (x, y)
    # x>0 move right
    # y>0 move up
    # x<0 move left
    # y<0 move down
    #       Test 1	Test 2	Test 3	Test 4	Test 5
    # L->0	( 0, 0)	(+1, 0)	(-2, 0)	(+1,-2)	(-2,+1)
    # 0->R	( 0, 0)	(-2, 0)	(+1, 0)	(-2,-1)	(+1,+2)
    # R->2	( 0, 0)	(-1, 0)	(+2, 0)	(-1,+2)	(+2,-1)
    # 2->L	( 0, 0)	(+2, 0)	(-1, 0)	(+2,+1)	(-1,-2)

    # R->0	( 0, 0)	(+2, 0)	(-1, 0)	(+2,+1)	(-1,-2)
    # 2->R	( 0, 0)	(+1, 0)	(-2, 0)	(+1,-2)	(-2,+1)
    # L->2	( 0, 0)	(-2, 0)	(+1, 0)	(-2,-1)	(+1,+2)
    # 0->L	( 0, 0)	(-1, 0)	(+2, 0)	(-1,+2)	(+2,-1)

    # wall check
    # box_in_top_left[0] > _block_y_pos_next or
    # box_in_top_left[1] > _block_x_pos_next or
    # box_in_bottom_right[0] < _block_y_pos_next or
    # box_in_bottom_right[1] < _block_x_pos_next

    kick_map = {
        # (up/z, not I/I)
        # up =1, z =2
        # not i  =1, I = 2
        # each element is (x, y)
        (1, 1): [
            [(0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2)],  # block_rotation_next = 0
            [(0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)],  # block_rotation_next = 1
            [(0, 0), (+1, 0), (+1, -1), (0, +2), (+1, +2)],  # block_rotation_next = 2
            [(0, 0), (+1, 0), (+1, +1), (0, -2), (+1, -2)],  # block_rotation_next = 3
        ],
        (2, 1): [
            [(0, 0), (+1, 0), (+1, -1), (0, +2), (+1, +2)],
            [(0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)],
            [(0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2)],
            [(0, 0), (+1, 0), (+1, +1), (0, -2), (+1, -2)],
        ],
        (1, 2): [
            [(0, 0), (+1, 0), (-2, 0), (+1, -2), (-2, +1)],
            [(0, 0), (-2, 0), (+1, 0), (-2, -1), (+1, +2)],
            [(0, 0), (-1, 0), (+2, 0), (-1, +2), (+2, -1)],
            [(0, 0), (+2, 0), (-1, 0), (+2, +1), (-1, -2)],
        ],
        (2, 2): [
            [(0, 0), (+2, 0), (-1, 0), (+2, +1), (-1, -2)],
            [(0, 0), (+1, 0), (-2, 0), (+1, -2), (-2, +1)],
            [(0, 0), (-2, 0), (+1, 0), (-2, -1), (+1, +2)],
            [(0, 0), (-1, 0), (+2, 0), (-1, +2), (+2, -1)],
        ],
    }
    # (x, y)
    _variant_pos = kick_map[(rotation_key[0], rotation_key[1])][block_rotation_next]
    for _y in range(_block_len):
        for _x in range(_block_len):
            if block_next[_y][_x] > 0 and (
                box_in_top_left[0] > (_block_y_pos_next + _y - _variant_pos[0][1])
                or box_in_top_left[1] > (_block_x_pos_next + _x + _variant_pos[0][0])
                or box_in_bottom_right[0] < (_block_y_pos_next + _y - _variant_pos[0][1])
                or box_in_bottom_right[1] < (_block_x_pos_next + _x + _variant_pos[0][0])
                or block_stack[_block_y_pos_next + _y - _variant_pos[0][1] - box_in_top_left[0]][
                    _block_x_pos_next + _x + _variant_pos[0][0] - box_in_top_left[1]
                ][2]
                > 0
            ):
                if _rotation_test[0]:
                    _rotation_test[0] = False
                    break
        if not _rotation_test[0]:
            break

    if _rotation_test[0]:
        return (
            _block_y_pos_next - _variant_pos[0][1],
            _block_x_pos_next + _variant_pos[0][0],
            True,
        )

    for _y in range(_block_len):
        for _x in range(_block_len):
            if block_next[_y][_x] > 0 and (
                box_in_top_left[0] > (_block_y_pos_next + _y - _variant_pos[1][1])
                or box_in_top_left[1] > (_block_x_pos_next + _x + _variant_pos[1][0])
                or box_in_bottom_right[0] < (_block_y_pos_next + _y - _variant_pos[1][1])
                or box_in_bottom_right[1] < (_block_x_pos_next + _x + _variant_pos[1][0])
                or block_stack[_block_y_pos_next + _y - _variant_pos[1][1] - box_in_top_left[0]][
                    _block_x_pos_next + _x + _variant_pos[1][0] - box_in_top_left[1]
                ][2]
                > 0
            ):
                if _rotation_test[1]:
                    _rotation_test[1] = False
                    break
        if not _rotation_test[1]:
            break

    if _rotation_test[1]:
        return (
            _block_y_pos_next - _variant_pos[1][1],
            _block_x_pos_next + _variant_pos[1][0],
            True,
        )

    for _y in range(_block_len):
        for _x in range(_block_len):
            if block_next[_y][_x] > 0 and (
                box_in_top_left[0] > (_block_y_pos_next + _y - _variant_pos[2][1])
                or box_in_top_left[1] > (_block_x_pos_next + _x + _variant_pos[2][0])
                or box_in_bottom_right[0] < (_block_y_pos_next + _y - _variant_pos[2][1])
                or box_in_bottom_right[1] < (_block_x_pos_next + _x + _variant_pos[2][0])
                or block_stack[_block_y_pos_next + _y - _variant_pos[2][1] - box_in_top_left[0]][
                    _block_x_pos_next + _x + _variant_pos[2][0] - box_in_top_left[1]
                ][2]
                > 0
            ):
                if _rotation_test[2]:
                    _rotation_test[2] = False
                    break
        if not _rotation_test[2]:
            break

    if _rotation_test[2]:
        return (
            _block_y_pos_next - _variant_pos[2][1],
            _block_x_pos_next + _variant_pos[2][0],
            True,
        )

    for _y in range(_block_len):
        for _x in range(_block_len):
            if block_next[_y][_x] > 0 and (
                box_in_top_left[0] > (_block_y_pos_next + _y - _variant_pos[3][1])
                or box_in_top_left[1] > (_block_x_pos_next + _x + _variant_pos[3][0])
                or box_in_bottom_right[0] < (_block_y_pos_next + _y - _variant_pos[3][1])
                or box_in_bottom_right[1] < (_block_x_pos_next + _x + _variant_pos[3][0])
                or block_stack[_block_y_pos_next + _y - _variant_pos[3][1] - box_in_top_left[0]][
                    _block_x_pos_next + _x + _variant_pos[3][0] - box_in_top_left[1]
                ][2]
                > 0
            ):
                if _rotation_test[3]:
                    _rotation_test[3] = False
                    break
        if not _rotation_test[3]:
            break

    if _rotation_test[3]:
        return (
            _block_y_pos_next - _variant_pos[3][1],
            _block_x_pos_next + _variant_pos[3][0],
            True,
        )

    for _y in range(_block_len):
        for _x in range(_block_len):
            if block_next[_y][_x] > 0 and (
                box_in_top_left[0] > (_block_y_pos_next + _y - _variant_pos[4][1])
                or box_in_top_left[1] > (_block_x_pos_next + _x + _variant_pos[4][0])
                or box_in_bottom_right[0] < (_block_y_pos_next + _y - _variant_pos[4][1])
                or box_in_bottom_right[1] < (_block_x_pos_next + _x + _variant_pos[4][0])
                or block_stack[_block_y_pos_next + _y - _variant_pos[4][1] - box_in_top_left[0]][
                    _block_x_pos_next + _x + _variant_pos[4][0] - box_in_top_left[1]
                ][2]
                > 0
            ):
                if _rotation_test[4]:
                    _rotation_test[4] = False
                    break
        if not _rotation_test[4]:
            break

    if _rotation_test[4]:
        return (
            _block_y_pos_next - _variant_pos[4][1],
            _block_x_pos_next + _variant_pos[4][0],
            True,
        )

    return (_block_y_pos_next, _block_x_pos_next, False)
    # _rotation_index = _rotation_test.index(True) if True in _rotation_test else -1
    # if _rotation_index == -1:  # failed
    #     return (_block_y_pos_next, _block_x_pos_next, False)
    # return (
    #     _block_y_pos_next - _variant_pos[_rotation_index][1],
    #     _block_x_pos_next + _variant_pos[_rotation_index][0],
    #     True,
    # )


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
