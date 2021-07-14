from src.snake.game import snake_entry
import pytest


@pytest.mark.snake
def test_f1(snake_fixture):
    assert snake_fixture == "ok"


# test fixture global variable
@pytest.mark.snake
def test__game():
    # snake()
    # mock keyboard input
    # spy
    pass


@pytest.mark.snake
def test__update_status():
    pass


@pytest.mark.snake
def test__update_score():
    pass


@pytest.mark.snake
def test__create_food():
    pass


@pytest.mark.snake
def test__get_head_next_y():
    pass


@pytest.mark.snake
def test__get_head_next_x():
    pass


@pytest.mark.snake
def test__append_snake():
    pass
