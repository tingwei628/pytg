from src.tetris.game import tetris_entry, _move_block

# from pytest_mock import mocker, MockFixture
import pytest
from unittest import mock

"""
test fixture -> global variable
mock -> keyboard input
parameters -> different pos, collision
assert -> status/score
marker -> run test only tetris or snake

pytest -v -m tetris
"""

"""
monkeypatch(fixture)

1. mock function in builtins
2. mock function in package

MagicMock
mocker.spy
"""


"""
global variable
parameterize fixture
parameterize params  to fixture by using "indirect"


mock
assert called_once
assert called


side_effect()
reset_mock()


"""


def m1_base():
    return 3


def m1():
    return m1_base()


def m2_base():
    return 5


def m2():
    return m2_base()


# order of decorator
@mock.patch("tests.tetris.test_game.m2_base")
@mock.patch("tests.tetris.test_game.m1_base")
# @mock.patch("tests.tetris.test_game.m2_base", return_value=500)
# @mock.patch("tests.tetris.test_game.m1_base", return_value=300)
@pytest.mark.tetris
def test_mock3(mock_m1_base, mock_m2_base):
    mock_m1_base.return_value = 300
    mock_m2_base.return_value = 500
    assert m1() == 300
    assert m2() == 500


@mock.patch("tests.tetris.test_game.m1_base")
@pytest.mark.parametrize("x_fixture, expected", [("a", "aaa")], indirect=["x_fixture"])
@pytest.mark.tetris
def test_mock2(mock_m1_base, x_fixture, expected):
    # mock_m1_base = mocker.patch("tests.tetris.test_game.m1_base")
    mock_m1_base.return_value = 2
    assert m1() == 2
    assert x_fixture == expected
    mock_m1_base.assert_called_once()


@pytest.mark.tetris
def test_mock1(mocker):
    # m2 = mocker.MagicMock(return_value=2, anything_you_want=100)
    # **{}: it packs all key-values to single dict to pass them to function
    m2 = mocker.MagicMock(**{"return_value": 2, "anything_you_want": 100, "prop.return_value": 1})

    assert m2() == 2
    assert m2.anything_you_want == 100
    assert m2.prop() == 1
    m2.assert_called_once()
    m2.assert_called_once_with()  # m2(args)
    # mocker.spy()


@pytest.mark.tetris
@pytest.mark.parametrize("x_fixture, expected", [("a", "aaa")], indirect=["x_fixture"])
def test_indirect(x_fixture, expected):
    assert x_fixture == expected
    # assert y == "b"


@pytest.mark.tetris
def test_f2(tetris_fixture):
    assert tetris_fixture == "ok"


# @pytest.fixture(scope="module", params=["start", "stop"])
# def action(request):
#     return request.param


# @pytest.mark.tetris
# def test_action(action):
#     # assert "pause" == action
#     assert action in ["start", "stop"]


"""
parameters
"""

# @pytest.mark.tetris
# def mysum(numbers):
#     sum = 0
#     for n in numbers:
#         sum += n
#     return sum
# @pytest.mark.parametrize("numbers,output", [([], 0), ([10, 20, 30], 60), ([0.1, 1.2, 2.3, 3.4, 4.5], 11.5)])
# def test_mysum(numbers, output):
#     assert mysum(numbers) == output


@pytest.mark.tetris
@pytest.mark.parametrize("a,b", [(1, 1), (2, 2)], ids=["this is 1", "this is 2"])  # ids -> test ids
def test_1(a, b):
    assert a == b


@pytest.mark.tetris
def test__game():
    # mock keyboard input
    pass


@pytest.mark.tetris
def test__block_pos_in_block_stack():
    pass


@pytest.mark.tetris
def test__move_block():
    pass


@pytest.mark.tetris
def test__rotate_block():
    pass


"""
test fixture
"""

# test fixture
@pytest.mark.tetris
def test__set_block_stack():
    pass


@pytest.mark.tetris
def test__is_game_over():
    pass


# test different position
@pytest.mark.tetris
def test__is_block_pos_overlap():
    pass


@pytest.mark.tetris
def test__merge_block_stack():
    # merge
    # deleted
    # move
    pass


@pytest.mark.tetris
def test__set_status():
    pass


@pytest.mark.tetris
def test__set_score():
    pass
