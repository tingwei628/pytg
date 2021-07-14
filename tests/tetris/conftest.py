import pytest

# setup tetris fixture
@pytest.fixture(scope="module")
def tetris_fixture():
    return "ok"


@pytest.fixture()
def x(request):
    return request.param * 3


# @pytest.fixture()
# def y(request):
#     return request.param * 2
