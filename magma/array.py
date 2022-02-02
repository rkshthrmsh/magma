import weakref
from functools import reduce, lru_cache
from abc import ABCMeta
from hwtypes import BitVector
from .common import deprecated
from .ref import AnonRef, ArrayRef
from .t import Type, Kind, Direction, In, Out
from .compatibility import IntegerTypes
from .digital import Digital
from .bit import Bit
from .bitutils import int2seq, seq2int
from .debug import debug_wire, get_callee_frame_info
from .logging import root_logger
from .protocol_type import magma_type, magma_value

from magma.operator_utils import output_only
from magma.wire_container import WiringLog, Wire, Wireable
from magma.protocol_type import MagmaProtocol


_logger = root_logger()


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
                if (N, T) == (None, None):
                    (N, T) = (base.N, base.T)
                elif N != base.N:
                    raise TypeError(
                        "Can't inherit from multiple arrays with different N")
                elif not issubclass(T, base.T):
                    raise TypeError(
                        "Can't inherit from multiple arrays with different T")

        namespace['_info_'] = info[0], N, T
        type_ = super().__new__(cls, name, bases, namespace, **kwargs)
        if (N, T) == (None, None):
            # class is abstract so t.abstract -> t
            type_._info_ = type_, N, T
        elif info[0] is None:
            # class inherited from concrete type so there is no abstract t
            type_._info_ = None, N, T

        return type_

    def __getitem__(cls, index: tuple) -> 'ArrayMeta':
        mcs = type(cls)

        # If cls.T is a direction, and the new T (index[1])
        if isinstance(cls.T, Direction):
            # If we're replacing a direction (e.g. `In(Out(Array)))`, just use
            # the default direction logic
            if not isinstance(index[1], Direction):
                # Otherwise, we expect that we're qualifying a Type with the
                # direction (e.g. In(Array)[5, Bit])
                if not issubclass(index[1], Type):
                    raise TypeError("Expected Type as second index to Array")
                if not index[1].is_oriented(cls.T):
                    _logger.warning(
                        f"Parametrizing qualifed Array {cls} with inner type "
                        f" {index[1]} which doesn't match, will use array "
                        "qualifier"
                    )
                index = index[0], index[1].qualify(cls.T)
        elif cls.T is None:
            # Else, it index[1] should be  Type (e.g. In(Bit)) or a Direction
            # (used internally for In(Array))
            valid_second_index = (isinstance(index[1], Direction) or
                                  issubclass(magma_type(index[1]), Type))
            if not valid_second_index:
                raise TypeError(
                    "Expected Type or Direction as second index to Array"
                    f" got: {index[1], type(index[1])}"
                )

        try:
            return mcs._class_cache[cls, index]
        except KeyError:
            pass

        if not (isinstance(index, tuple) and len(index) == 2):
            raise TypeError('Parameters to array must be a tuple of length 2')

        # index[0] (N) can be None (used internally for In(Array))
        if index[0] is not None:
            if isinstance(index[0], tuple):
                if len(index[0]) == 0:
                    raise ValueError("Cannot create array with length 0 tuple "
                                     "for N")
                if len(index[0]) > 1:
                    T = index[1]
                    # ND Array
                    for N in index[0]:
                        T = Array[N, T]
                    return T
                # len(index[0]) == 1, Treat as normal Array
                index = index[0]

            if (not isinstance(index[0], int) or index[0] <= 0):
                raise TypeError(
                    'Length of array must be an int greater than 0, got:'
                    f' {index[0]}'
                )

        if cls.is_concrete:
            if index[0] == cls.N and index[1] is cls.T:
                return cls
            else:
                return cls.abstract_t[index]

        bases = []
        bases.extend(b[index] for b in cls.__bases__ if isinstance(b, mcs))
        # only add base classes if we're have a child type
        # (skipped in the case of In(Array))
        if not isinstance(index[1], Direction):
            bases.extend(cls[index[0], b] for b in index[1].__bases__ if
                         isinstance(b, type(magma_type(index[1]))))
        if not any(issubclass(b, cls) for b in bases):
            bases.insert(0, cls)
        bases = tuple(bases)
        orig_name = cls.__name__
        if isinstance(index[1], Direction):
            class_name = f'{index[1].name}({cls.__name__})'
        else:
            class_name = '{}[{}]'.format(cls.__name__, index)
        type_ = mcs(class_name, bases, {"orig_name": orig_name},
                    info=(cls, ) + index)
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
    def undirected_t(cls) -> 'ArrayMeta':
        T = cls.T
        if cls.is_concrete:
            return cls[cls.N, cls.T.qualify(Direction.Undirected)]
        else:
            raise AttributeError('type {} has no undirected_t'.format(cls))

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

    def __repr__(cls):
        # Emit In/Out/InOut(Array)
        if isinstance(cls.T, Direction):
            assert cls.N is None
            return f"{cls.T.name}(Array)"
        # Class name logic provides Array[N, T], Bits[N], etc...
        return cls.__name__

    @lru_cache()
    def qualify(cls, direction):
        if cls.direction == direction:
            # For performance, avoid requalifying if not necessary
            return cls
        if cls.T is None or isinstance(cls.T, Direction):
            # Handle qualified, unsized/child e.g. In(Array) and In(Out(Array))
            return cls[None, direction]
        return cls[cls.N, cls.T.qualify(direction)]

    @lru_cache()
    def flip(cls):
        return cls[cls.N, cls.T.flip()]

    @property
    @lru_cache()
    def direction(cls):
        if cls.T is None:
            return None
        if isinstance(cls.T, Direction):
            return cls.T
        return cls.T.direction

    def __eq__(cls, rhs):
        if not isinstance(rhs, ArrayMeta):
            return NotImplemented
        return (cls.N == rhs.N) and (cls.T == rhs.T)

    @lru_cache()
    def is_wireable(cls, rhs):
        rhs = magma_type(rhs)
        if not isinstance(rhs, ArrayMeta) or cls.N != rhs.N:
            return False
        return cls.T.is_wireable(rhs.T)

    def is_bindable(cls, rhs):
        rhs = magma_type(rhs)
        if not isinstance(rhs, ArrayMeta) or cls.N != rhs.N:
            return False
        return cls.T.is_bindable(rhs.T)

    __hash__ = type.__hash__


def _is_valid_slice(N, key):
    start, stop = key.start, key.stop
    return (((start is None or (start < N and start >= -N))) and
            (stop is None or (stop <= N and stop > -N)))


def _make_array_from_list(N, T, arg):
    if len(arg) != N:
        raise ValueError("Array list constructor can only be used "
                         "with list equal to array length")
    return [elem if not isinstance(elem, int) else T(elem)
            for elem in arg]


def _make_array_from_array(N, arg):
    if len(arg) != N:
        raise TypeError(f"Will not do implicit conversion of arrays")
    return arg.ts[:]


def _make_array_from_bv(N, T, arg):
    if not issubclass(T, Bit):
        raise TypeError(f"Can only instantiate Array[N, Bit] "
                        f"with int/bv, not Array[N, {T}]")
    if isinstance(arg, BitVector) and len(arg) != N:
        raise TypeError(
            f"Cannot construct Array[{N}, {T}] with BitVector of length "
            f"{len(arg)} (sizes must match)")
    if isinstance(arg, int) and arg.bit_length() > N:
        raise ValueError(
            f"Cannot construct Array[{N}, {T}] with integer {arg} "
            f"(requires truncation)")
    bits = int2seq(arg, N) if isinstance(arg, int) else arg.bits()
    return [T(bit) for bit in bits]


def _check_arg(N, T, arg):
    assert (type(arg) == T or type(arg) == T.flip() or
            issubclass(type(type(arg)), type(T)) or
            issubclass(type(T), type(type(arg)))), (type(arg), T)


def _make_array_length_one(T, arg):
    if isinstance(arg, IntegerTypes):
        arg = T(arg)
    return [arg]


def _make_array_length_n(N, T, args):
    ts = [T(t) if isinstance(t, IntegerTypes) else t for t in args]
    for t in ts:
        _check_arg(N, T, t)
    return ts


def _make_array_no_args(array):
    T = array.T
    refs = [ArrayRef(array, i) for i in range(array.N)]
    if not issubclass(T, MagmaProtocol):
        return [T(name=ref) for ref in refs]
    return [T._from_magma_value_(T._to_magma_()(name=ref)) for ref in refs]


def _make_array_from_args(N, T, args):
    if len(args) == 1 and isinstance(args[0], (list, Array, int, BitVector)):
        if isinstance(args[0], list):
            return _make_array_from_list(N, T, args[0])
        if isinstance(args[0], Array):
            return _make_array_from_array(N, args[0])
        if isinstance(args[0], (BitVector, int)):
            return _make_array_from_bv(N, T, args[0])
        if N == 1:
            return _make_array_length_one(T, args[0])
    if len(args) == N:
        return _make_array_length_n(N, T, args)
    raise TypeError(f"Constructing array with {args} not supported")


def _make_array(array, args):
    if args:
        return _make_array_from_args(array.N, array.T, args)
    return _make_array_no_args(array)


def _is_slice_child(child):
    return isinstance(child, Array) and child._is_slice()


class Array(Type, Wireable, metaclass=ArrayMeta):
    """
    Wireable class allows Array values to be "bulk wired" like a Digital value

    The `self._ts` attribute contains a lazily constructed mapping from index
    to child value.

    The `self._slices` attribute contains a list of slice objects that
    reference an array value.  Slices are lazily expanded in order to optimize
    performance in the commons case.  Slices are expanded by constructing the
    child objects and populating the corresponding entries in the `._ts`
    dictionary of both the slice object the parent array object.

    A large portion of the Array logic for the Wireable interface must dispatch
    on `self._ts` and `self._slices` to see if the Array has been expanded
    (requiring the logic to be implemented recursively over the children),
    otherwise the logic will treat the Array as a "bulk wired" value.
    """
    def __init__(self, *args, **kwargs):
        # Pass name= kwarg to Type constructor
        Type.__init__(self, **kwargs)
        Wireable.__init__(self)
        if args:
            # If args is not empty, that means this array is being constructed
            # with existing values, so populate the `_ts` dictionary eagerly
            self._ts = {i: t for i, t in enumerate(_make_array(self, args))}
        else:
            self._ts = {}

        self._slices = {}
        self._unresolved_slices = {}
        # Store mapping from slice start index to object for faster lookup when
        # checking overlapping indicies/slices
        self._slices_by_start_index = {}

    @classmethod
    def is_oriented(cls, direction):
        if cls.T is None:
            return False
        return cls.T.is_oriented(direction)

    @classmethod
    def is_clock(cls):
        return False

    @output_only("Cannot use == on an input")
    def __eq__(self, rhs):
        if not isinstance(rhs, ArrayType):
            return False
        return self.ts == rhs.ts

    @output_only("Cannot use != on an input")
    def __ne__(self, rhs):
        return ~(self == rhs)

    __hash__ = Type.__hash__

    @property
    def T(self):
        return type(self).T

    @property
    def N(self):
        return type(self).N

    def __len__(self):
        return self.N

    @classmethod
    def flat_length(cls):
        return cls.N * cls.T.flat_length()

    def _is_whole_slice(self, key):
        # check if it's any of `x[:], x[0:], x[:len(x)], x[0:len(x)]`
        return (isinstance(key[-1], slice) and
                (key[-1] == slice(None) or
                 key[-1] == slice(0, None) or
                 key[-1] == slice(None, len(self)) or
                 key[-1] == slice(0, len(self))))

    def __setitem__(self, key, val):
        """
        Validate when the user attempts to mutate the array.  This is done by
        default by using the @= operator, so the simplest check is to validate
        val is self[key] since this should return the same value except in one
        case (the ndarray slicing logic will return a new array).

        If it's not the same value, we can recursively check the array values
        to verify they are the same.

        *Technically* the user could "fake" these properties but the hope is
        that if they satisfy the conditions and call __setitem__, then the
        expected behavior should be the same (also it doesn't actually mutate
        the array, so it's "safe" in that sense).

        This does incur a performance cost, so it does raise the questions as
        to whether it's really necessary, or if there's a simpler way to ensure
        __setitem__ is only called with @= and not directly (maybe return a
        private "setinel" object from the @ operator?).
        """
        old = self[key]
        error = False
        if old is val:
            # Early "exit" in the common case to avoid recursion in other
            # branches
            pass
        elif isinstance(old, Array):
            if len(old) != len(val):
                error = True
            elif issubclass(old.T, Array):
                # If array of array, check that we can do elementwise setitem
                # (will return true if there's an error)
                # We can't just do an `is` check on the children since those
                # might be slices that return new anon values (so x[1:2] is not
                # x[1:2], but their recursive leaf contents should be the same)
                error = any(old.__setitem__(i, val[i])
                            for i in range(len(old)))
            elif any(old[i] is not val[i] for i in range(len(old))):
                error = True
        else:
            error = True

        if error:
            _logger.error(
                WiringLog(f"May not mutate array, trying to replace "
                          f"{{}}[{key}] ({{}}) with {{}}", self, old, val)
            )
        return error

    def __add__(self, other):
        other_len = other.N
        total = self.N + other_len
        res_bits = []
        for i in range(total):
            res_bits.append(self[i] if i < self.N else other[i - self.N])
        return type(self)[len(res_bits), self.T](res_bits)

    def __call__(self, o):
        return self.wire(o, get_callee_frame_info())

    def as_list(self):
        return [self[i] for i in range(len(self))]

    def _check_wireable(self, o, debug_info):
        i = self
        if not isinstance(o, ArrayType):
            if isinstance(o, IntegerTypes):
                _logger.error(
                    WiringLog(f"Cannot wire {o} (type={type(o)}) to {{}} "
                              f"(type={type(i)}) because conversions from "
                              f"IntegerTypes are only defined for Bits, not "
                              f"general Arrays", i),
                    debug_info=debug_info
                )
            else:
                o_str = getattr(o, "debug_name", str(o))
                _logger.error(
                    WiringLog(f"Cannot wire {{}} (type={type(o)}) to {{}} "
                              f"(type={type(i)}) because {{}} is not an Array",
                              o, i, o),
                    debug_info=debug_info
                )
            return False

        if i.N != o.N:
            _logger.error(
                WiringLog(f"Cannot wire {{}} (type={type(o)}) to {{}} "
                          f"(type={type(i)}) because the arrays do not have "
                          f"the same length", o, i),
                debug_info=debug_info
            )
            return False
        return True

    def driving(self):
        if self._has_elaborated_children():
            return [t.driving() for t in self]
        return Wireable.driving(self)

    def wired(self):
        if self._has_elaborated_children():
            return all(t.wired() for t in self)
        return Wireable.wired(self)

    # test whether the values refer a whole array
    @staticmethod
    def _iswhole(ts):

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
            if ts[i].name.array is not ts[i - 1].name.array:
                return False

        if n > 0 and n != ts[0].name.array.N:
            # must use all of the elements of the base array
            return False

        for i in range(n):
            # elements should be numbered consecutively
            if ts[i].name.index != i:
                return False

        return True

    @classmethod
    def unflatten(cls, value):
        size_T = cls.T.flat_length()
        if len(value) != size_T * cls.N:
            raise TypeError("Width mismatch")
        ts = [cls.T.unflatten(value[i:i + size_T])
              for i in range(0, size_T * cls.N, size_T)]
        return cls(ts)

    def concat(self, other) -> 'AbstractBitVector':
        return type(self)[len(self) + len(other), self.T](self.ts + other.ts)

    def undriven(self):
        for elem in self:
            elem.undriven()

    def unused(self):
        for elem in self:
            elem.unused()

    @classmethod
    def is_mixed(cls):
        return cls.T.is_mixed()

    def _wire_children(self, o):
        for i, child in self._enumerate_children():
            curr_value = child.value()
            new_value = o[i]
            if curr_value is not new_value:
                # Skip updating wire in the case that it's the same value
                # (avoids an error message)
                child.wire(new_value)

    @debug_wire
    def wire(self, o, debug_info):
        o = magma_value(o)
        if not self._check_wireable(o, debug_info):
            return
        if self._has_elaborated_children():
            # Ensure the children maintain consistency with the bulk wire
            self._wire_children(o)
        else:
            # Perform a bulk wire
            Wireable.wire(self, o, debug_info)

    def unwire(self, o):
        if self._has_elaborated_children():
            for i, child in self._enumerate_children():
                child.unwire(o[i])
        else:
            Wireable.unwire(self, o)

    def iswhole(self):
        if self._has_elaborated_children():
            return Array._iswhole(self._collect_children(lambda x: x))
        return True

    def const(self):
        if self._has_elaborated_children():
            return all(child.const()
                       for _, child in self._enumerate_children())
        return False

    def _resolve_bulk_wire(self):
        """
        If a child reference is made, we "expand" a bulk wire into the
        constiuent children to maintain consistency
        """
        if self._wire.driven():
            # Remove bulk wire since children will now track the wiring
            value = self._wire.value()
            Wireable.unwire(self, value)

            # Update children
            for i in range(len(self)):
                self._get_t(i).wire(value[i])

    def _make_t(self, index):
        if issubclass(self.T, MagmaProtocol):
            return self.T._from_magma_value_(
                self.T._to_magma_()(name=ArrayRef(self, index)))
        else:
            return self.T(name=ArrayRef(self, index))

    def _resolve_slice_children(self, start, stop, slice_value):
        for i in range(start, stop):
            slice_value._ts[i - start] = self._get_t(i)

    def _resolve_slice_driver(self, start, stop, value):
        # When we encounter an overlapping slice that is already bulk driven,
        # we ensure the corresponding children are updated to their current values
        if value._wire.driven():
            driver = value._wire.value()
            Wireable.unwire(value, driver)
            for i in range(start, stop):
                self._ts[i] @= driver[i - start]

    def _remove_slice(self, key):
        # Remove slice since we don't need to track it anymore (handled
        # by child logic) to optimize other slice iteration logic
        # This avoids having to iterate over slices when we are just
        # using their children instead
        del self._unresolved_slices[key]
        del self._slices_by_start_index[key[0]]

    def _update_overlapping_slices(self, t, index):
        # Update existing slices to have matching child references
        for k, v in list(self._unresolved_slices.items()):
            if k[0] <= index < k[1]:
                self._remove_slice(k)
                assert v._ts.get(index - k[0], t) is t
                v._ts[index - k[0]] = t
                self._resolve_slice_children(k[0], k[1], v)
                self._resolve_slice_driver(k[0], k[1], v)
                # TODO(leonardt/array2): I think there should only ever be one
                # so we can break here

    def _get_t(self, index):
        if index not in self._ts:
            if self._is_slice():
                # Maintain consistency by always fetching child object from top
                # level array
                return self.name.array._get_t(self.name.index.start + index)
            self._ts[index] = t = self._make_t(index)
            self._update_overlapping_slices(t, index)
        return self._ts[index]

    def _resolve_overlapping_indices(self, slice_, value):
        """
        If there's any overlapping children or slices, collect the total range
        of the children and realize them so slices are "expanded" and maintain
        consistency
        """
        start = slice_.start
        stop = slice_.stop

        overlapping = any(i in self._ts for i in range(start, stop))

        def range_overlapping(x, y):
            return x[0] < y[1] and y[0] < x[1]

        if not overlapping:
            # As soon as we find an overlap we resolve the whole slice so no
            # need to check twice since any other overlaps will be resolved
            for k, v in list(self._unresolved_slices.items()):
                if range_overlapping(k, (start, stop)):
                    overlapping = True
                    break
        if overlapping:
            for i in range(start, stop):
                # _get_t to populate slice children and resolve any overlaps
                value._ts[i - start] = self._get_t(i)
        return overlapping

    def _get_slice(self, slice_):
        key = (slice_.start, slice_.stop)
        slice_value = self._slices.get(key, None)
        if slice_value is None:
            slice_T = type(self)[slice_.stop - slice_.start, self.T]
            slice_value = slice_T(name=ArrayRef(self, slice_))
            self._slices[key] = slice_value
            if not self._resolve_overlapping_indices(slice_, slice_value):
                self._slices_by_start_index[key[0]] = slice_value
                self._unresolved_slices[key] = slice_value
        return slice_value

    def _normalize_slice_key(self, key):
        # Normalize slice by mapping None to concrete int values
        start = key.start if key.start is not None else 0
        if start < 0:
            start = self.N + start
            if start < 0:
                raise IndexError(key)
        stop = key.stop if key.stop is not None else len(self)
        if stop < 0:
            stop = self.N + stop
            if stop < 0:
                raise IndexError(key)
        if key.step is not None:
            raise NotImplementedError("Variable slice step not implemented")
        return slice(start, stop, key.step)

    def _ndarray_getitem(self, key: tuple):
        # tuple -> ND Array key

        if len(key) == 1:
            return self[key[0]]
        if not isinstance(key[-1], slice):
            return self[key[-1]][key[:-1]]
        if not self._is_whole_slice(key):
            # If it's not a slice of the whole array, first slice the
            # current array (self), then replace with a slice of the whole
            # array (this is how we determine that we're ready to traverse
            # into the children)
            this_key = key[-1]
            result = self[this_key][key[:-1] + (slice(None), )]
            return result
        # Last index is selecting the whole array, recurse into the
        # children and slice off the inner indices
        inner_ts = [t[key[:-1]] for t in self.ts]
        # Get the type from the children and return the final value
        return type(self)[len(self), type(inner_ts[0])](inner_ts)

    def _variable_step_slice_getitem(self, key):
        # Use Python indexing logic
        indices = [i for i in range(len(self))][key]
        return type(self)[len(indices), self.T](
            [self[i] for i in indices])

    def _get_arr_and_offset(self):
        # For nested references of slice objects, we compute the offset from
        # the original array to simplify bookkeeping as well as reducing the
        # size of the select in the backend
        arr = self
        offset = 0
        if arr._is_slice():
            offset = arr.name.index.start
            arr = arr.name.array
        return arr, offset

    def _normalize_int_key(self, key):
        if isinstance(key, BitVector):
            key = int(key)
        if isinstance(key, int) and key < 0:
            key += len(self)
        return key

    def __getitem__(self, key):
        if isinstance(key, Type):
            # indexed using a dynamic magma value, generate mux circuit
            return self.dynamic_mux_select(key)
        if isinstance(key, tuple):
            return self._ndarray_getitem(key)
        if isinstance(key, int) and key > self.N - 1:
            raise IndexError()
        if isinstance(key, slice):
            if key.step is not None:
                return self._variable_step_slice_getitem(key)
            if not _is_valid_slice(self.N, key):
                raise IndexError(f"array index out of range "
                                 f"(type={type(self)}, key={key})")
            key = self._normalize_slice_key(key)

        arr, offset = self._get_arr_and_offset()

        if isinstance(key, (int, BitVector)):
            result = arr._get_t(offset + self._normalize_int_key(key))
        elif isinstance(key, slice):
            result = arr._get_slice(slice(offset + key.start,
                                          offset + key.stop))
        else:
            raise NotImplementedError(key, type(key))
        self._resolve_bulk_wire()
        return result

    def flatten(self):
        ts = []
        for _, child in self._enumerate_children():
            ts.extend(child.flatten())
        return ts

    def __repr__(self):
        if self.name.anon():
            t_strs = ', '.join(repr(t) for t in self.ts)
            return f'array([{t_strs}])'
        return Type.__repr__(self)

    @property
    def ts(self):
        return [elem for elem in self]

    def _collect_children(self, func):
        """
        Recursive traversal that is aware of slice objects (rather than normal
        iter that always goes one index at a time)

        `func` is called on the child
            e.g. to fetch the value of the children, use lambda x: x.value()

        Returns None if func(child) returns None
            e.g. the value is None if any of the children have a value None
        """
        ts = []
        for _, child in self._enumerate_children():
            result = func(child)
            if result is None:
                return None
            if _is_slice_child(child) and child.name.array is self:
                ts.extend(result.ts)
            else:
                ts.append(result)

        # Pack whole array together for readability
        if Array._iswhole(ts):
            return ts[0].name.array

        # Pack into Bits const if possible for readability
        if all(t.const() for t in ts):
            return type(self).flip()(ts)

        return Array[self.N, self.T.flip()](ts)

    def _has_elaborated_children(self):
        return bool(self._ts) or bool(self._slices)

    def value(self):
        if self._has_elaborated_children():
            return self._collect_children(lambda x: x.value())
        return super().value()

    def _make_trace_child(self, skip_self):
        def _trace_child(t):
            """
            This handles the case where certain children trace further than
            others.

            Suppose we have an intermediate trace Array([GND, GND, y]) where
            y.value() is VCC.

            Default trace logic for GND would return None since it's an output,
            whereas old-style array logic would trace each child invidually (so
            stopping at GND for the first two indices, and VCC for the final).

            This trace function emulates the old-style logic in the case where
            an Array is constructed with existing values (as in the above
            example)
            """
            result = t.trace(skip_self)
            if result is not None:
                return result
            if not skip_self and (t.is_output() or t.is_inout()):
                return t
            return None
        return _trace_child

    def trace(self, skip_self=True):
        if self._has_elaborated_children():
            result = self._collect_children(self._make_trace_child(skip_self))
            return result
        return super().trace()

    def driven(self):
        if self._has_elaborated_children():
            for _, child in self._enumerate_children():
                if child is None:
                    return False
                if not child.driven():
                    return False
            return True
        return super().driven()

    def _is_slice(self):
        return (isinstance(self.name, ArrayRef) and
                isinstance(self.name.index, slice))

    def _enumerate_children(self):
        i = 0
        while i < self.N:
            if i in self._ts:
                yield i, self._ts[i]
                i += 1
            elif i in self._slices_by_start_index:
                # We only need to lookup one slice by start index because if
                # multiple slices overlap, they're children will be realized
                # and in self._ts
                value = self._slices_by_start_index[i]
                slice_ = value.name.index
                yield slice_, value
                i = slice_.stop
            else:
                # Create the child using default getitem logic
                yield i, self[i]
                i += 1

    def connection_iter(self, only_slice_bits=False):
        if self._wire.driven():
            driver = self.trace()
            if driver is None:
                return
            # Anon whole driver, e.g. Bit to Bits[1]
            yield from zip(self, driver)
            return
        for _, child in self._enumerate_children():
            if (_is_slice_child(child) and only_slice_bits and
                    not issubclass(self.T, Bit)):
                yield from zip(child, child.trace())
            else:
                yield child, child.trace()

    def has_children(self):
        return True


ArrayType = Array
