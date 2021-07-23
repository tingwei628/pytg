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

COLOR_PAIR_RANGE = (11, 16)
BLOCK_TYPE_RANGE = (0, 7)
BLOCK_ROTATION_RANGE = (0, 4)

SCORE_POS = (2, 5)
STATUS_POS = (3, 5)

START = 1
STOP = 0

block_stack = []
block_map = []
block_init_pos_map = []
kick_map = {}
block_lock = False  # is this block locked to be merged
block_y_pos = 0
block_x_pos = 0
block_color = -1
block_type = -1
block_rotation = -1
score = 0
