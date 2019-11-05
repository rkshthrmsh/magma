from collections import OrderedDict
import functools
import warnings
import enum
from abc import abstractmethod
from .ref import Ref, AnonRef, DefnRef, InstRef
from .port import INOUT, INPUT, OUTPUT
from .compatibility import IntegerTypes, StringTypes
from hwtypes.adt import TupleMeta, ProductMeta


# From http://code.activestate.com/recipes/391367-deprecated/
def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""
    @functools.wraps(func)
    def newFunc(*args, **kwargs):
        warnings.warn("Call to deprecated function %s." % func.__name__,
                      category=DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)
    newFunc.__name__ = func.__name__
    newFunc.__doc__ = func.__doc__
    newFunc.__dict__.update(func.__dict__)
    return newFunc


class Direction(enum.Enum):
    In = 0
    Out = 1
    InOut = 2
    Flip = 3
    Undirected = 4


class Type(object):
    def __init__(self, **kwargs):
        name = kwargs.get('name', None)
        if name is None or isinstance(name, str):
            name = AnonRef(name=name)
        self.name = name

    __hash__ = object.__hash__

    def __repr__(self):
        return repr(self.name)

    def __str__(self):
        return str(self.name)

    # an instance has an anon name
    def anon(self):
        return self.name.anon()

    # abstract method - must be implemented by subclasses
    @classmethod
    def is_oriented(cls, direction):
        raise NotImplementedError()

    @classmethod
    def is_input(cls):
        return cls.is_oriented(Direction.In)

    @classmethod
    def is_output(cls):
        return cls.is_oriented(Direction.Out)

    @classmethod
    def is_inout(cls):
        return cls.is_oriented(Direction.InOut)

    @classmethod
    @deprecated
    def isoriented(cls, direction):
        return cls.is_oriented(direction)

    @classmethod
    @deprecated
    def isinput(cls):
        return cls.is_input()

    @classmethod
    @deprecated
    def isoutput(cls):
        return cls.is_output()

    @classmethod
    @deprecated
    def isinout(cls):
        return cls.is_inout()

    @property
    def debug_name(self):
        defn_str = ""
        inst_str = ""
        if isinstance(self.name, DefnRef):
            defn_str = str(self.name.defn.name) + "."
        elif isinstance(self.name, InstRef):
            inst_str = str(self.name.inst.name) + "."
            defn_str = str(self.name.inst.defn.name) + "."
        return f"{defn_str}{inst_str}{str(self)}"

    def __le__(self, other):
        if not self.is_output():
            self.wire(other)
        else:
            raise TypeError(f"Cannot use <= to assign to output: {self.debug_name} (trying to assign {other.debug_name})")


class Kind(type):
    # subclasses only need to implement one of these methods
    def __eq__(cls, rhs):
        return cls is rhs

    __hash__ = type.__hash__

    def __repr__(cls):
        return cls.__name__

    def __str__(cls):
        return cls.__name__

    @abstractmethod
    def qualify(cls, direction):
        raise NotImplementedError()

    def flip(cls):
        return cls.qualify(Direction.Flip)


def In(T):
    if isinstance(T, TupleMeta):
        return qualify(T, Direction.In)
    return T.qualify(Direction.In)


def Out(T):
    if isinstance(T, TupleMeta):
        return qualify(T, Direction.Out)
    return T.qualify(Direction.Out)


def InOut(T):
    if isinstance(T, TupleMeta):
        return qualify(T, Direction.In)
    return T.qualify(Direction.InOut)


def Flip(T):
    if isinstance(T, TupleMeta):
        return qualify(T, Direction.Flip)
    return T.qualify(Direction.Flip)


def Undirected(T):
    if isinstance(T, TupleMeta):
        return qualify(T, Direction.Undirected)
    return T.qualify(Direction.Undirected)


def qualify(T, direction):
    if isinstance(T, ProductMeta):
        new_fields = OrderedDict()
        for k, v in T.field_dict.items():
            new_fields[k] = qualify(v, direction)
        result = T.unbound_t.from_fields(T.__name__, new_fields,
                                         cache=T.is_cached)
        return result
    elif isinstance(T, TupleMeta):
        new_fields = []
        for field in T.fields:
            new_fields.append(qualify(field, direction))
        return T.unbound_t[new_fields]
    return T.qualify(direction)

def is_oriented(T, direction):
    if isinstance(T, TupleMeta):
        return all(is_oriented(x, direction) for x in T.field_dict.values())
    else:
        return T.is_oriented(direction)
