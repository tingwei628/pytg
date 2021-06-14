from src.module_1.hello import hello


def test_hello():
    assert hello() == 5
