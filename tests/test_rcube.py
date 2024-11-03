import random

from src.minpycube import RCube


def test_rotate():
    c = RCube()
    ops = list(c.op_function_map.keys())
    for op in ops:
        c.rotate(op)
        c.rotate(RCube.invert_op(op))
        assert c.calc_fit() == 54


def test_run_list():
    c = RCube()
    all_ops = list(c.op_function_map.keys())
    ops = [random.choice(all_ops) for _ in range(20)]
    for op in ops:
        c.rotate(op)
    ops.reverse()
    ops = list(map(RCube.invert_op, ops))
    for op in ops:
        c.rotate(op)
    assert c.calc_fit() == 54


def test_calc_fit():
    c = RCube()
    assert c.calc_fit() == 54
