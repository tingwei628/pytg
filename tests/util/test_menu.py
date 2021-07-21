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
from src.util.menu import menu


# mock patch: snake_entry, tetris_entry, display_menu

# test different menu pos
@pytest.mark.menu
def test_menu():
    pass


@mock.patch("src.tetris.game.tetris_entry", return_value=300)
@mock.patch("src.snake.game.snake_entry", return_value=500)
@mock.patch("src.util.menu.display_menu", return_value=300)
@pytest.mark.parametrize("stdscrMock, expected_dict", [("a", "aaa")], indirect=["stdscrMock"])
@pytest.mark.menu
def test_initial_game_stage(display_menu_mock, snake_entry_mock, tetris_entry_mock, stdscrMock, expected_dict):
    menu()
    assert display_menu_mock() == 300
    assert snake_entry_mock() == 500
    assert tetris_entry_mock() == 300


# test initial game
# parameterize which_game, key
# assert sub_menu_current_index
# assert menu_stage


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
