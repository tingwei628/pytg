from src.tetris.game import tetris_entry, _move_block
import pytest

"""
test fixture -> global variable
mock -> keyboard input
parameters -> different pos, collision
assert -> status/score
marker -> run test only tetris or snake


monkeypatch
    A convenient fixture for monkey-patching.

    The fixture provides these methods to modify objects, dictionaries or
    os.environ::

        monkeypatch.setattr(obj, name, value, raising=True)
        monkeypatch.delattr(obj, name, raising=True)
        monkeypatch.setitem(mapping, name, value)
        monkeypatch.delitem(obj, name, raising=True)
        monkeypatch.setenv(name, value, prepend=False)
        monkeypatch.delenv(name, raising=True)
        monkeypatch.syspath_prepend(path)
        monkeypatch.chdir(path)

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
"""


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
