from pynads import Writer, Mempty, List
from pynads.funcs import identity
import pytest


add_two = lambda x: x+2
m_add_two = lambda x: Writer(x+2, List.unit('added two'))


str_add_two = lambda x: Writer(add_two(x), ' added two')
int_add_two = lambda x: Writer(add_two(x), 4)
dict_add_two = lambda x: Writer(add_two(x), {'added': 2})
dict_div_two = lambda x: Writer(x//2, {'divided': 2})


def test_writer_unit():
    w = Writer.unit(2)
    assert w.v == (2, Mempty)


def test_fmap_id():
    w = Writer.unit(2).fmap(identity)
    assert w.v == (2, Mempty) 


def test_writer_fmap():
    w = Writer.unit(2).fmap(add_two)
    assert w.v == (4, Mempty)


def test_writer_apply():
    w = (Writer.unit(add_two)) * (Writer.unit(2))
    assert w.v == (4, Mempty)


def test_writer_bind():
    w = Writer.unit(2) >> m_add_two
    assert w.v == (4, List.unit('added two'))


@pytest.mark.parametrize('writer, func, value, log', [
    (Writer(2, ''), str_add_two, 4, ' added two'),
    (Writer(2, 0), int_add_two, 4, 4),
    (Writer(2, {}), dict_add_two, 4, {'added': 2})
])
def test_writer_log_with_monoids(writer, func, value, log):
    w = writer >> func
    assert w.v == (value, log)


def test_writer_dict_updates_multiple_times():
    w = Writer.unit(4) >> dict_add_two >> dict_div_two
    assert w.v == (3, {'added': 2, 'divided': 2})
