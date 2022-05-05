from magma.common import Stack


WHEN_COND_STACK = Stack()
_PREV_WHEN_COND = None


def reset_context():
    global WHEN_COND_STACK, _PREV_WHEN_COND
    WHEN_COND_STACK.clear()
    _PREV_WHEN_COND = None


class WhenCtx:
    def __init__(self, cond, base_cond=None, prev_conds=None):
        self._cond = cond
        self._assignments = []
        if base_cond is None:
            base_cond = cond
        self._base_cond = base_cond
        if prev_conds is None:
            prev_conds = []
        self._prev_conds = prev_conds

        global _PREV_WHEN_COND
        # Reset when to avoid a nested `elsewhen` or `otherwise` continuing a
        # chain
        _PREV_WHEN_COND = None

    def __enter__(self):
        WHEN_COND_STACK.push(self)

    def __exit__(self, exc_type, exc_value, traceback):
        print("Foo")
        global _PREV_WHEN_COND
        _PREV_WHEN_COND = WHEN_COND_STACK.pop()

    @property
    def cond(self):
        return self._cond


when = WhenCtx


def _check_prev_when_cond(name):
    global _PREV_WHEN_COND
    if _PREV_WHEN_COND is None:
        raise SyntaxError(f"Cannot use {name} without a previous when")


def elsewhen(cond):
    _check_prev_when_cond('elsewhen')

    global _PREV_WHEN_COND
    inv_cond = ~_PREV_WHEN_COND._base_cond
    for prev in _PREV_WHEN_COND._prev_conds:
        inv_cond &= ~prev
    return WhenCtx(inv_cond & cond, cond,
                   _PREV_WHEN_COND._prev_conds + [_PREV_WHEN_COND._base_cond])


def otherwise():
    _check_prev_when_cond('otherwise')

    global _PREV_WHEN_COND
    inv_cond = ~_PREV_WHEN_COND._base_cond
    for prev in _PREV_WHEN_COND._prev_conds:
        inv_cond &= ~prev
    # TODO(when): Enforce this context isn't used again
    return WhenCtx(inv_cond, True,
                   _PREV_WHEN_COND._prev_conds + [_PREV_WHEN_COND._base_cond])
