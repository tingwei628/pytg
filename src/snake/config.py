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
