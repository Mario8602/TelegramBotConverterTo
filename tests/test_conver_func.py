from reunion import mourin
import pytest


@pytest.mark.parametrize("n, result", [
    (10, [2, 3, 5, 7]),
    (15, [2, 3, 5, 7, 11, 13]),
    (4, [2, 3]),
    (4, [2, 3])
])
def test_func_mobius(n, result):
    assert mourin(n) == result


@pytest.mark.parametrize("what_error, n", [
    (TypeError, '3')
])
def test_func_error(what_error, n):
    with pytest.raises(what_error):
        mourin(n)