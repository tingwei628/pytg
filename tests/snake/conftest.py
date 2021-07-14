import pytest

# setup snake fixture
@pytest.fixture(scope="module")
def snake_fixture():
    return "ok"
