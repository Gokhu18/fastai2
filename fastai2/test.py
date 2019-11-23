#AUTOGENERATED! DO NOT EDIT! File to edit: dev/00_test.ipynb (unless otherwise specified).

__all__ = ['test_fail', 'test', 'nequals', 'test_eq', 'test_eq_type', 'test_ne', 'is_close', 'test_close', 'test_is',
           'test_shuffled', 'test_stdout', 'test_warns', 'TEST_IMAGE', 'TEST_IMAGE_BW', 'test_fig_exists']

#Cell
from .core.imports import *

#Cell
def test_fail(f, msg='', contains=''):
    "Fails with `msg` unless `f()` raises an exception and (optionally) has `contains` in `e.args`"
    try: f()
    except Exception as e:
        assert not contains or contains in str(e)
        return
    assert False,f"Expected exception but none raised. {msg}"

#Cell
def test(a, b, cmp,cname=None):
    "`assert` that `cmp(a,b)`; display inputs and `cname or cmp.__name__` if it fails"
    if cname is None: cname=cmp.__name__
    assert cmp(a,b),f"{cname}:\n{a}\n{b}"

#Cell
def nequals(a,b):
    "Compares `a` and `b` for `not equals`"
    return not equals(a,b)

#Cell
def test_eq(a,b):
    "`test` that `a==b`"
    test(a,b,equals, '==')

#Cell
def test_eq_type(a,b):
    "`test` that `a==b` and are same type"
    test_eq(a,b)
    test_eq(type(a),type(b))
    if isinstance(a,(list,tuple)): test_eq(map(type,a),map(type,b))

#Cell
def test_ne(a,b):
    "`test` that `a!=b`"
    test(a,b,nequals,'!=')

#Cell
def is_close(a,b,eps=1e-5):
    "Is `a` within `eps` of `b`"
    if hasattr(a, '__array__') or hasattr(b,'__array__'):
        return (abs(a-b)<eps).all()
    if isinstance(a, (Iterable,Generator)) or isinstance(b, (Iterable,Generator)):
        return is_close(np.array(a), np.array(b), eps=eps)
    return abs(a-b)<eps

#Cell
def test_close(a,b,eps=1e-5):
    "`test` that `a` is within `eps` of `b`"
    test(a,b,partial(is_close,eps=eps),'close')

#Cell
def test_is(a,b):
    "`test` that `a is b`"
    test(a,b,operator.is_, 'is')

#Cell
def test_shuffled(a,b):
    "`test` that `a` and `b` are shuffled versions of the same sequence of items"
    test_ne(a, b)
    test_eq(Counter(a), Counter(b))

#Cell
def test_stdout(f, exp, regex=False):
    "Test that `f` prints `exp` to stdout, optionally checking as `regex`"
    s = io.StringIO()
    with redirect_stdout(s): f()
    if regex: assert re.search(exp, s.getvalue()) is not None
    else: test_eq(s.getvalue(), f'{exp}\n' if len(exp) > 0 else '')

#Cell
def test_warns(f, show=False):
    with warnings.catch_warnings(record=True) as w:
        f()
        test_ne(len(w), 0)
        if show:
            for e in w: print(f"{e.category}: {e.message}")

#Cell
TEST_IMAGE = 'images/puppy.jpg'

#Cell
TEST_IMAGE_BW = 'images/mnist3.png'

#Cell
def test_fig_exists(ax):
    "Test there is a figure displayed in `ax`"
    assert ax and len(np.frombuffer(ax.figure.canvas.tostring_argb(), dtype=np.uint8))