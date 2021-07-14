import pytest

# setup util fixture
@pytest.fixture(scope="module")
def util_fixture():
    return "ok"
