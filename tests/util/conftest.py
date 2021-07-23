import pytest


""" 

screen_width_mid = 22
screen_height_mid = 22
curses.KEY_DOWN = 258
curses.KEY_UP = 259
curses.KEY_RIGHT = 261
curses.KEY_LEFT = 260

"""


# setup util fixture
# @pytest.fixture(scope="module")
# @pytest.fixture()
# def cursesMock(mocker, request):
#     _cursesMock = mocker.MagicMock(
#         **{
#             "curs_set.return_value": None,
#             "init_pair.return_value": None,
#             "KEY_DOWN": 258,
#             "KEY_UP": 259,
#             "KEY_LEFT": 260,
#             "KEY_RIGHT": 261,
#             "COLOR_BLACK": -1,
#             "COLOR_WHITE": -1,
#         }
#     )
#     return _cursesMock


# @pytest.fixture(scope="module")
@pytest.fixture()
def stdscrMock(mocker, request):
    _stdscrMock = mocker.MagicMock(
        **{"getmaxyx.return_value": (22, 22), "clear.return_value": None, "getch.return_value": request.param}
    )
    return _stdscrMock
