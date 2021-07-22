"""
test util/menu.py

Test fixure:  stdscr
mock keyboard input
stub game_entry()
"""
import pytest
from unittest import mock

# from src.tetris.game import tetris_entry
# from src.snake.game import snake_entry
from src.util.menu import menu, NO_GAME, SNAKE_GAME, TETRIS_GAME, MENU_STAGE, SUB_MENU_STAGE, SUB_MENU_LIST

# same import path of config.py in src/util/menu.py
import util.config as config

__curses_dict = {
    "curs_set.return_value": None,
    "init_pair.return_value": None,
    "KEY_DOWN": 258,
    "KEY_UP": 259,
    "KEY_LEFT": 260,
    "KEY_RIGHT": 261,
    "COLOR_BLACK": -1,
    "COLOR_WHITE": -1,
}

# pytest setup in function level
def setup_function():
    config.menu_current_index = 0
    config.sub_menu_current_index = 0
    config.menu_stage = -1


@mock.patch("src.tetris.game.tetris_entry", return_value=None)
@mock.patch("src.snake.game.snake_entry", return_value=None)
@mock.patch("src.util.menu.display_menu", return_value=None)
@mock.patch(
    "src.util.menu.curses",
    return_value=mock.MagicMock(**__curses_dict),
)
@pytest.mark.parametrize(
    "stdscrMock, which_game, expected_dict",
    [
        (
            -1,
            TETRIS_GAME,
            {"menu_stage": SUB_MENU_STAGE, "sub_menu_current_index": SUB_MENU_LIST.index("Tetris")},
        ),
        (
            -1,
            SNAKE_GAME,
            {"menu_stage": SUB_MENU_STAGE, "sub_menu_current_index": SUB_MENU_LIST.index("Snake")},
        ),
    ],
    indirect=["stdscrMock"],
)
@pytest.mark.menu
def test_initial_game_stage(
    curses_mock,
    display_menu_mock,
    snake_entry_mock,
    tetris_entry_mock,
    stdscrMock,
    which_game,
    expected_dict,
):

    menu(stdscrMock, which_game, True)
    assert config.sub_menu_current_index == expected_dict["sub_menu_current_index"]
    assert config.menu_stage == expected_dict["menu_stage"]


@mock.patch("src.tetris.game.tetris_entry", return_value=None)
@mock.patch("src.snake.game.snake_entry", return_value=None)
@mock.patch("src.util.menu.display_menu", return_value=None)
@mock.patch(
    "src.util.menu.curses",
    return_value=mock.MagicMock(**__curses_dict),
)
@pytest.mark.parametrize(
    "stdscrMock, expected_dict",
    [
        (
            258,  # KEY_UP
            {"index": 1},
        ),
        (
            259,  # KEY_DOWN
            {"index": 0},
        ),
    ],
    indirect=["stdscrMock"],
)
@pytest.mark.menu
def test_menu_arrowkey_moving(
    curses_mock,
    display_menu_mock,
    snake_entry_mock,
    tetris_entry_mock,
    stdscrMock,
    expected_dict,
):
    menu(stdscrMock, NO_GAME, True)
    assert config.menu_stage == MENU_STAGE


@mock.patch("src.tetris.game.tetris_entry", return_value=None)
@mock.patch("src.snake.game.snake_entry", return_value=None)
@mock.patch("src.util.menu.display_menu", return_value=None)
@mock.patch(
    "src.util.menu.curses",
    return_value=mock.MagicMock(**__curses_dict),
)
@pytest.mark.parametrize(
    "stdscrMock, expected_dict",
    [
        (
            10,  # KEY_ENTER
            {"index": 0},
        )
    ],
    indirect=["stdscrMock"],
)
@pytest.mark.menu
def test_enter_sub_menu(
    curses_mock,
    display_menu_mock,
    snake_entry_mock,
    tetris_entry_mock,
    stdscrMock,
    expected_dict,
):
    menu(stdscrMock, NO_GAME, True)
    assert config.menu_stage == SUB_MENU_STAGE
    assert config.sub_menu_current_index == 0


@pytest.mark.menu
def test_load_game_called():
    # curses_mock.assert_called()
    # display_menu_mock.assert_called()
    # assert curses_mock.curs_set.call_count == 1
    # assert curses_mock.init_pair.call_count == 1
    # assert stdscrMock.getmaxyx.call_count == 1
    # assert stdscrMock.getch.call_count == 1
    pass


# test load game
# parameterize key, menu_stage, sub_menu_current_index
# assert mock called
