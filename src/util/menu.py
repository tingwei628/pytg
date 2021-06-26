from snake.game import snake_entry
import curses

NO_GAME = 0
SNAKE_GAME = 1
TERTRIS_GAME = 2


def menu(stdscr, which_game):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    KEY_ENTER = 10
    KEY_ESC = 27
    MENU_STAGE = 0
    SUB_MENU_STAGE = 1
    screen_height, screen_width = stdscr.getmaxyx()
    screen_height_mid = screen_height // 2
    screen_width_mid = screen_width // 2
    menu_current_index = 0
    sub_menu_current_index = 0
    menu_stage = MENU_STAGE

    menu = ["Select Games", "Exit"]
    sub_menu = ["Snake", "Tetris", "Exit"]
    menu_select_games_idx = 0
    menu_exit_idx = 1
    if which_game == SNAKE_GAME:
        sub_menu_current_index = sub_menu.index("Snake")
        menu_stage = SUB_MENU_STAGE
        display_menu(stdscr, sub_menu_current_index, sub_menu, screen_height_mid, screen_width_mid)
    elif which_game == TERTRIS_GAME:
        sub_menu_current_index = sub_menu.index("Tetris")
        menu_stage = SUB_MENU_STAGE
        display_menu(stdscr, sub_menu_current_index, sub_menu, screen_height_mid, screen_width_mid)
    else:
        display_menu(stdscr, menu_current_index, menu, screen_height_mid, screen_width_mid)
    while 1:
        key = stdscr.getch()
        if key == curses.KEY_UP and menu_stage == MENU_STAGE:
            menu_current_index = menu_current_index - 1 if menu_current_index > 0 else len(menu) - 1
        elif key == curses.KEY_DOWN and menu_stage == MENU_STAGE:
            menu_current_index = menu_current_index + 1 if menu_current_index < len(menu) - 1 else 0
        elif key == KEY_ENTER and menu_current_index == menu_select_games_idx and menu_stage == MENU_STAGE:
            menu_stage = SUB_MENU_STAGE
        elif key == curses.KEY_UP and menu_stage == SUB_MENU_STAGE:
            sub_menu_current_index = sub_menu_current_index - 1 if sub_menu_current_index > 0 else len(sub_menu) - 1
        elif key == curses.KEY_DOWN and menu_stage == SUB_MENU_STAGE:
            sub_menu_current_index = sub_menu_current_index + 1 if sub_menu_current_index < len(sub_menu) - 1 else 0
        elif (
            key == KEY_ENTER and sub_menu_current_index == len(sub_menu) - 1 and menu_stage == SUB_MENU_STAGE
        ) or key == KEY_ESC:
            # reset sub menu index
            sub_menu_current_index = 0
            menu_stage = MENU_STAGE
        elif key == KEY_ENTER and menu_stage == SUB_MENU_STAGE and sub_menu_current_index == sub_menu.index("Snake"):
            stdscr.clear()
            snake_entry()
            break
        elif key == KEY_ENTER and menu_current_index == menu_exit_idx and menu_stage == MENU_STAGE:
            break

        if menu_stage == MENU_STAGE:
            display_menu(stdscr, menu_current_index, menu, screen_height_mid, screen_width_mid)
        elif menu_stage == SUB_MENU_STAGE:
            display_menu(stdscr, sub_menu_current_index, sub_menu, screen_height_mid, screen_width_mid)


def display_menu(stdscr, select_idx, menu, screen_height_mid, screen_width_mid):
    menu_len = len(menu)
    stdscr.clear()
    for idx, menu_item in enumerate(menu):
        x = screen_width_mid - len(menu_item)
        y = screen_height_mid - menu_len + idx
        if select_idx == idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, menu_item)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, menu_item)


def menu_entry(which_game=NO_GAME):
    curses.wrapper(menu, which_game)


if __name__ == "__main__":
    menu_entry()
