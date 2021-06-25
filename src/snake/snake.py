import curses
from random import randint
from curses import textpad

"""
1. Game restart/pause/exit
2. A* algorithm


https://stackoverflow.com/questions/44014715/is-it-possible-to-get-the-default-background-color-using-curses-in-python

"""


def game(stdscr):

    # initial setting
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    box_top_left_x = 5
    box_top_left_y = 5
    screen_height, screen_width = stdscr.getmaxyx()
    screen_height_mid = screen_height // 2
    screen_width_mid = screen_width // 2
    box_top_left = (box_top_left_x, box_top_left_y)  # (y, x)
    box_bottom_right = (screen_height - box_top_left[0], screen_width - box_top_left[1])
    # box = [box_start, box_end]
    textpad.rectangle(stdscr, box_top_left[0], box_top_left[1], box_bottom_right[0], box_bottom_right[1])

    # snake body
    snake_body = [
        (screen_height_mid, screen_width_mid - 1),  # snake tail
        (screen_height_mid, screen_width_mid),
        (screen_height_mid, screen_width_mid + 1),  # snake head position
    ]
    snake_step = 1
    # snake head direction
    snake_head_dir = curses.KEY_RIGHT

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
    stdscr.attron(curses.color_pair(1))

    for y, x in snake_body:
        stdscr.addstr(y, x, "|")
    stdscr.attroff(curses.color_pair(1))

    update_score(len(snake_body), screen_width, stdscr)

    while 1:
        key = stdscr.getch()

        if key == -1:  # not input
            key = snake_head_dir

        snake_head = snake_body[-1]
        # snake_head_next = ()
        if key == curses.KEY_RIGHT and snake_head_dir != curses.KEY_LEFT:
            x = (
                (box_top_left[1] + snake_step)
                if (snake_head[1] + snake_step - box_top_left[1]) % box_bottom_right[1] == 0
                else snake_head[1] + snake_step
            )
            snake_head_next = (
                snake_head[0],
                x,
            )
            append_snake(stdscr, snake_body, snake_head_next)
            snake_head_dir = key
            # update_score(key, screen_width, stdscr)
        elif key == curses.KEY_LEFT and snake_head_dir != curses.KEY_RIGHT:
            snake_head_next = (snake_head[0], snake_head[1] - snake_step)
            append_snake(stdscr, snake_body, snake_head_next)
            snake_head_dir = key
            # update_score(key, screen_width, stdscr)
        elif key == curses.KEY_DOWN and snake_head_dir != curses.KEY_UP:
            snake_head_next = (snake_head[0] + snake_step, snake_head[1])
            append_snake(stdscr, snake_body, snake_head_next)
            snake_head_dir = key
            # update_score(key, screen_width, stdscr)
        elif key == curses.KEY_UP and snake_head_dir != curses.KEY_DOWN:
            snake_head_next = (snake_head[0] - snake_step, snake_head[1])
            append_snake(stdscr, snake_body, snake_head_next)
            snake_head_dir = key
            # update_score(key, screen_width, stdscr)
        else:
            continue
        # stdscr.addstr(snake_head_next[0], snake_head_next[1], "|")
        # snake_body.append(snake_head_next)

        snake_tail = snake_body[0]
        stdscr.addstr(snake_tail[0], snake_tail[1], " ")
        snake_body.pop(0)


def append_snake(stdscr, snake_body, snake_head_next):
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(snake_head_next[0], snake_head_next[1], "|")
    snake_body.append(snake_head_next)
    stdscr.attroff(curses.color_pair(1))


def update_score(score, screen_width, stdscr):
    score_text = "Score: {}".format(score)
    stdscr.addstr(1, screen_width // 2 - len(score_text) // 2, score_text)


def snake():
    curses.wrapper(game)


if __name__ == "__main__":
    snake()
