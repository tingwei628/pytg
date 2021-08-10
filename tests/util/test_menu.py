"""
test util/menu.py
pytest -m menu -s
-s: print()
"""
import pytest
from unittest import mock


from sys import path
from os.path import join, dirname

path.append(join(dirname(__file__), "../../src"))

from util.menu import menu

# import src.util.menu as menu

# same import path of config.py in src/util/menu.py
import util.config as config

NO_GAME = config.NO_GAME
SNAKE_GAME = config.SNAKE_GAME
TETRIS_GAME = config.TETRIS_GAME
MENU_STAGE = config.MENU_STAGE
SUB_MENU_STAGE = config.SUB_MENU_STAGE
SUB_MENU_LIST = config.SUB_MENU_LIST

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


@mock.patch("util.menu.tetris_entry", return_value=None)
@mock.patch("util.menu.snake_entry", return_value=None)
@mock.patch("util.menu.display_menu", return_value=None)
@mock.patch(
    "util.menu.curses",
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

    menu(stdscrMock, which_game, True, 1)
    assert config.sub_menu_current_index == expected_dict["sub_menu_current_index"]
    assert config.menu_stage == expected_dict["menu_stage"]


@mock.patch("util.menu.tetris_entry", return_value=None)
@mock.patch("util.menu.snake_entry", return_value=None)
@mock.patch("util.menu.display_menu", return_value=None)
@mock.patch(
    "util.menu.curses",
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
    menu(stdscrMock, NO_GAME, True, 1)
    assert config.menu_stage == MENU_STAGE


@mock.patch("util.menu.tetris_entry", return_value=None)
@mock.patch("util.menu.snake_entry", return_value=None)
@mock.patch("util.menu.display_menu", return_value=None)
@mock.patch(
    "util.menu.curses",
    return_value=mock.MagicMock(**__curses_dict),
)
@pytest.mark.parametrize(
    "stdscrMock",
    [(10)],  # KEY_ENTER
    indirect=["stdscrMock"],
)
@pytest.mark.menu
def test_enter_sub_menu(
    curses_mock,
    display_menu_mock,
    snake_entry_mock,
    tetris_entry_mock,
    stdscrMock,
):
    menu(stdscrMock, NO_GAME, True, 1)
    assert config.menu_stage == SUB_MENU_STAGE


@mock.patch("util.menu.tetris_entry", return_value=None)
@mock.patch("util.menu.snake_entry", return_value=None)
@mock.patch("util.menu.display_menu", return_value=None)
@mock.patch(
    "util.menu.curses",
    return_value=mock.MagicMock(**__curses_dict),
)
@mock.patch("util.menu.config.sub_menu_current_index", SUB_MENU_LIST.index("Snake"))
@pytest.mark.parametrize(
    "stdscrMock",
    [(10)],  # KEY_ENTER
    indirect=["stdscrMock"],
)
@pytest.mark.menu
def test_load_snake_game_called(
    curses_mock,
    display_menu_mock,
    snake_entry_mock,
    tetris_entry_mock,
    stdscrMock,
):
    menu(stdscrMock, NO_GAME, True, 2)
    assert config.menu_stage == SUB_MENU_STAGE
    assert stdscrMock.clear.call_count == 1
    snake_entry_mock.assert_called_once()


@mock.patch("util.menu.tetris_entry", return_value=None)
@mock.patch("util.menu.snake_entry", return_value=None)
@mock.patch("util.menu.display_menu", return_value=None)
@mock.patch(
    "util.menu.curses",
    return_value=mock.MagicMock(**__curses_dict),
)
@mock.patch("util.menu.config.sub_menu_current_index", SUB_MENU_LIST.index("Tetris"))
@pytest.mark.parametrize(
    "stdscrMock",
    [(10)],  # KEY_ENTER
    indirect=["stdscrMock"],
)
@pytest.mark.menu
def test_load_tetris_game_called(
    curses_mock,
    display_menu_mock,
    snake_entry_mock,
    tetris_entry_mock,
    stdscrMock,
):
    menu(stdscrMock, NO_GAME, True, 2)
    assert config.menu_stage == SUB_MENU_STAGE
    assert stdscrMock.clear.call_count == 1
    tetris_entry_mock.assert_called_once()
