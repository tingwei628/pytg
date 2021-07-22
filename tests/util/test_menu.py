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
from src.util.menu import menu, SNAKE_GAME, TETRIS_GAME, SUB_MENU_STAGE, SUB_MENU_LIST

# same import path of config.py in src/util/menu.py
import util.config as config

# from tests.util.conftest import cursesMock

# mock patch: snake_entry, tetris_entry, display_menu


@mock.patch("src.tetris.game.tetris_entry", return_value=None)
@mock.patch("src.snake.game.snake_entry", return_value=None)
@mock.patch("src.util.menu.display_menu", return_value=None)
@mock.patch(
    "src.util.menu.curses",
    return_value=mock.MagicMock(
        **{
            "curs_set.return_value": None,
            "init_pair.return_value": None,
            "KEY_DOWN": 258,
            "KEY_UP": 259,
            "KEY_LEFT": 260,
            "KEY_RIGHT": 261,
            "COLOR_BLACK": -1,
            "COLOR_WHITE": -1,
        }
    ),
)
# @mock.patch("src.util.menu.menu_current_index", 0)
# @mock.patch("src.util.menu.menu_stage", -1)
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
    # menu_stage,
    # menu_current_index,
    curses_mock,
    display_menu_mock,
    snake_entry_mock,
    tetris_entry_mock,
    stdscrMock,
    which_game,
    expected_dict,
):

    menu(stdscrMock, which_game, True)
    # curses_mock.assert_called()
    # display_menu_mock.assert_called()
    # assert curses_mock.curs_set.call_count == 1
    # assert curses_mock.init_pair.call_count == 1
    # assert stdscrMock.getmaxyx.call_count == 1
    # assert stdscrMock.getch.call_count == 1

    assert config.sub_menu_current_index == expected_dict["sub_menu_current_index"]
    assert config.menu_stage == expected_dict["menu_stage"]


@pytest.mark.menu
def test_menu_index_when_keyboard_moving():
    pass


# test moving
# parameterize key, menu_stage
# assert menu_current_index
# assert sub_menu_current_index


@pytest.mark.menu
def test_load_game_called():
    pass


# test load game
# parameterize key, menu_stage, sub_menu_current_index
# assert mock called
