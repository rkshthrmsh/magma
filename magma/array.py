import weakref
from abc import ABCMeta
import magma as m
from .ref import AnonRef, ArrayRef
from .t import Type, Kind, deprecated, qualify, is_oriented
from .compatibility import IntegerTypes
from .bit import Bit
from .bitutils import seq2int
from .debug import debug_wire, get_callee_frame_info
from .port import report_wiring_error


class ArrayMeta(ABCMeta, Kind):
    # BitVectorType, size :  BitVectorType[size]
    _class_cache = weakref.WeakValueDictionary()

    def __new__(cls, name, bases, namespace, info=(None, None, None), **kwargs):
        # TODO: A lot of this code is shared with AbstractBitVectorMeta, we
        # should refactor to reuse
        if '_info_' in namespace:
            raise TypeError(
                'class attribute _info_ is reversed by the type machinery')

        N, T = info[1:3]
        for base in bases:
            if getattr(base, 'is_concrete', False):
                if (N, T) is (None, None):
                    (N, T) = (base.N, base.T)
                elif (N, T) != (base.N, base.T):
                    raise TypeError(
                        "Can't inherit from multiple arrays with different N and/or T")

        namespace['_info_'] = info[0], N, T
        type_ = super().__new__(cls, name, bases, namespace, **kwargs)
        if (N ,T) == (None, None):
            #class is abstract so t.abstract -> t
            type_._info_ = type_, N, T
        elif info[0] is None:
            #class inherited from concrete type so there is no abstract t
            type_._info_ = None, N, T

        return type_

    def __getitem__(cls, index: tuple) -> 'ArrayMeta':
        mcs = type(cls)
        try:
            return mcs._class_cache[cls, index]
        except KeyError:
            pass

        if not (isinstance(index, tuple) and len(index) == 2):
            raise TypeError('Parameters to array must be a tuple of length 2')
        if not isinstance(index[0], int) or index[0] <= 0:
            raise TypeError(f'Length of array must be an int greater than 0, got: {index[0]}')


        if cls.is_concrete:
            if index == (cls.N, cls.T):
                return cls
            else:
                return cls.abstract_t[index]

        bases = [cls]
        bases.extend(b[index] for b in cls.__bases__ if isinstance(b, mcs))
        bases = tuple(bases)
        orig_name = cls.__name__
        class_name = '{}[{}]'.format(cls.__name__, index)
        type_ = mcs(class_name, bases, {"orig_name": orig_name}, info=(cls, ) + index)
        type_.__module__ = cls.__module__
        mcs._class_cache[cls, index] = type_
        return type_

    @property
    def abstract_t(cls) -> 'ArrayMeta':
        t = cls._info_[0]
        if t is not None:
            return t
        else:
            raise AttributeError('type {} has no abstract_t'.format(cls))

    @property
    def N(cls) -> int:
        return cls._info_[1]

    @property
    def T(cls):
        return cls._info_[2]

    @property
    def is_concrete(cls) -> bool:
        return (cls.N, cls.T) != (None, None)

    def __len__(cls):
        return cls.N

    def __str__(cls):
        return f"Array[{cls.N}, {cls.T}]"

    def qualify(cls, direction):
        return cls[cls.N, qualify(cls.T, direction)]

    def __eq__(cls, rhs):
        if not isinstance(rhs, ArrayMeta):
            return NotImplemented
        return (cls.N == rhs.N) and (cls.T == rhs.T)

    __hash__ = type.__hash__


class Array(Type, metaclass=ArrayMeta):
    def __init__(self, *args, **kwargs):
        Type.__init__(self, **kwargs)
        self.ts = []
        if args:
            if len(args) == 1 and isinstance(args[0], (list, Array, m.Wire, int)):
                if isinstance(args[0], list):
                    if len(args[0]) != self.N:
                        raise ValueError("Array list constructor can only be used with list equal to array length")
                    self.ts = []
                    for elem in args[0]:
                        if isinstance(elem, int):
                            self.ts.append(m.VCC if elem else m.GND)
                        else:
                            self.ts.append(elem)
                elif isinstance(args[0], m.Wire) and \
                        isinstance(args[0]._value, Array) or \
                        isinstance(args[0], Array):
                    if len(args[0]) != len(self):
                        raise TypeError(f"Will not do implicit conversion of arrays")
                    arg = args[0]
                    if isinstance(arg, m.Wire):
                        arg = arg._value
                    self.ts = arg.ts[:]
                elif isinstance(args[0], int):
                    if not issubclass(self.T, Bit):
                        raise TypeError(f"Can only instantiate Array[N, Bit] "
                                        "with int, not Array[N, {self.T}]")
                    self.ts = []
                    for bit in m.bitutils.int2seq(args[0], self.N):
                        self.ts.append(m.VCC if bit else m.GND)
                elif self.N == 1:
                    t = args[0]
                    if isinstance(t, IntegerTypes):
                        t = m.VCC if t else m.GND
                    assert type(t) == self.T or type(t) == self.T.flip() or \
                        issubclass(type(type(t)), type(self.T)) or \
                        issubclass(type(self.T), type(type(t))), (type(t), self.T)
                    self.ts = [t]
                else:
                    raise NotImplementedError(args[0], type(args[0]))
            elif len(args) == self.N:
                self.ts = []
                for t in args:
                    if isinstance(t, IntegerTypes):
                        t = m.VCC if t else m.GND
                    assert type(t) == self.T or type(t) == self.T.flip() or \
                        issubclass(type(type(t)), type(self.T)) or \
                        issubclass(type(self.T), type(type(t))), (type(t), self.T)
                    self.ts.append(t)
            else:
                raise NotImplementedError(args)
        else:
            for i in range(self.N):
                T = self.T
                t = m.Wire(type_=T, name=ArrayRef(self, i))
                self.ts.append(t)

    @classmethod
    def is_oriented(cls, direction):
        if cls.T is None:
            return False
        return cls.T.is_oriented(direction)

    @classmethod
    @deprecated
    def isoriented(cls, direction):
        return cls.is_oriented(direction)

    def __eq__(self, rhs):
        if not isinstance(rhs, Array):
            return False
        return self.ts == rhs.ts

    __hash__ = Type.__hash__

    def __repr__(self):
        if not isinstance(self.name, AnonRef):
            return repr(self.name)
        ts = [repr(t) for t in self.ts]
        return 'array([{}])'.format(', '.join(ts))

    @property
    def T(self):
        return type(self).T

    @property
    def N(self):
        return type(self).N

    def __len__(self):
        return self.N

    def __getitem__(self, key):
        if isinstance(key, Array) and all(t in {m.VCC, m.GND} for t in key.ts):
            key = seq2int([0 if t is m.GND else 1 for t in key.ts])
        if isinstance(key, slice):
            _slice = [self[i] for i in range(*key.indices(len(self)))]
            return type(self)[len(_slice), self.T](_slice)
        else:
            if not (-self.N <= key and key < self.N):
                raise IndexError

            return self.ts[key]

    def __add__(self, other):
        other_len = other.N
        total = self.N + other_len
        res_bits = []
        for i in range(total):
            res_bits.append(self[i] if i < self.N else other[i - self.N])
        return array(res_bits)

    def __call__(self, o):
        return self.wire(o, get_callee_frame_info())

    @classmethod
    def is_oriented(cls, direction):
        return is_oriented(cls.T, direction)

    def as_list(self):
        return [self[i] for i in range(len(self))]

    @debug_wire
    def wire(i, o, debug_info):
        # print('Array.wire(', o, ', ', i, ')')

        if not isinstance(o, Array):
            if isinstance(o, IntegerTypes):
                report_wiring_error(f'Cannot wire {o} (type={type(o)}) to {i.debug_name} (type={type(i)}) because conversions from IntegerTypes are only defined for Bits, not general Arrays', debug_info)  # noqa
            else:
                report_wiring_error(f'Cannot wire {o.debug_name} (type={type(o)}) to {i.debug_name} (type={type(i)}) because {o.debug_name} is not an Array', debug_info)  # noqa
            return

        if i.N != o.N:
            report_wiring_error(f'Cannot wire {o.debug_name} (type={type(o)}) to {i.debug_name} (type={type(i)}) because the arrays do not have the same length', debug_info)  # noqa
            return

        for k in range(len(i)):
            i[k].wire(o[k], debug_info)

    def driven(self):
        for t in self.ts:
            if not t.driven():
                return False
        return True

    def wired(self):
        for t in self.ts:
            if not t.wired():
                return False
        return True

    # test whether the values refer a whole array
    def iswhole(self, ts):

        n = len(ts)

        for i in range(n):
            if ts[i].anon():
                return False

        for i in range(n):
            # elements must be an array reference
            if not isinstance(ts[i].name, ArrayRef):
                return False

        for i in range(1, n):
            # elements must refer to the same array
            if ts[i].name.array is not ts[i-1].name.array:
                return False

        if n > 0 and n != ts[0].name.array.N:
            # must use all of the elements of the base array
            return False

        for i in range(n):
            # elements should be numbered consecutively
            if ts[i].name.index != i:
                return False

        return True

    def trace(self):
        ts = [t.trace() for t in self.ts]

        for t in ts:
            if t is None:
                return None

        if self.iswhole(ts):
            return ts[0].name.array

        return type(self)(*ts)

    def value(self):
        ts = [t.value() for t in self.ts]

        for t in ts:
            if t is None:
                return None

        if self.iswhole(ts):
            return ts[0].name.array

        return type(self)(*ts)

    def const(self):
        for t in self.ts:
            if not t.const():
                return False

        return True

    def flatten(self):
        return sum([t.flatten() for t in self.ts], [])

    def concat(self, other) -> 'AbstractBitVector':
        return m.Wire(value=type(self)[len(self) + len(other), self.T](self.ts + other.ts))
