import pytest
from custom_package.example_subpackage import example_module


def test_hello():
    assert example_module.hello("Bob") == "Hello Bob"


@pytest.mark.parametrize("name", ["Jane", "JOHN", "betty"])
def test_hello_multiple(name):
    assert example_module.hello(name) == f"Hello {name}"
