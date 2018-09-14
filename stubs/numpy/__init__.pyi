import builtins
import sys

from numpy.core._internal import _ctypes
from typing import (
    Any,
    Container,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Sized,
    SupportsAbs,
    SupportsComplex,
    SupportsFloat,
    SupportsInt,
    Text,
    Tuple,
    Type,
    TypeVar,
    Union,
)

if sys.version_info[0] < 3:
    class SupportsBytes:
        ...
else:
    from typing import SupportsBytes

_Shape = Tuple[int, ...]

# Anything that can be coerced to a shape tuple
_ShapeLike = Union[int, Sequence[int]]

_DtypeLikeNested = Any  # TODO: wait for support for recursive types

# Anything that can be coerced into numpy.dtype.
# Reference: https://docs.scipy.org/doc/numpy/reference/arrays.dtypes.html
_DtypeLike = Union[
    dtype,
    # default data type (float64)
    None,
    # array-scalar types and generic types
    type,  # TODO: enumerate these when we add type hints for numpy scalars
    # TODO: add a protocol for anything with a dtype attribute
    # character codes, type strings or comma-separated fields, e.g., 'float64'
    str,
    # (flexible_dtype, itemsize)
    Tuple[_DtypeLikeNested, int],
    # (fixed_dtype, shape)
    Tuple[_DtypeLikeNested, _ShapeLike],
    # [(field_name, field_dtype, field_shape), ...]
    List[Union[
        Tuple[Union[str, Tuple[str, str]], _DtypeLikeNested],
        Tuple[Union[str, Tuple[str, str]], _DtypeLikeNested, _ShapeLike]]],
    # {'names': ..., 'formats': ..., 'offsets': ..., 'titles': ...,
    #  'itemsize': ...}
    # TODO: use TypedDict when/if it's officially supported
    Dict[str, Union[
        Sequence[str],  # names
        Sequence[_DtypeLikeNested],  # formats
        Sequence[int],  # offsets
        Sequence[Union[bytes, Text, None]],  # titles
        int,  # itemsize
    ]],
    # {'field1': ..., 'field2': ..., ...}
    Dict[str, Tuple[_DtypeLikeNested, int]],
    # (base_dtype, new_dtype)
    Tuple[_DtypeLikeNested, _DtypeLikeNested],
]


class dtype:
    names: Optional[Tuple[str, ...]]

    def __init__(self,
                 obj: _DtypeLike,
                 align: bool = ...,
                 copy: bool = ...) -> None: ...

    @property
    def alignment(self) -> int: ...

    @property
    def base(self) -> dtype: ...

    @property
    def byteorder(self) -> str: ...

    @property
    def char(self) -> str: ...

    @property
    def descr(self) -> List[Union[
        Tuple[str, str],
        Tuple[str, str, _Shape]]]: ...

    @property
    def fields(self) -> Optional[Mapping[
        str,
        Union[Tuple[dtype, int],
              Tuple[dtype, int, Any]]]]: ...

    @property
    def flags(self) -> int: ...

    @property
    def hasobject(self) -> bool: ...

    @property
    def isbuiltin(self) -> int: ...

    @property
    def isnative(self) -> bool: ...

    @property
    def isalignedstruct(self) -> bool: ...

    @property
    def itemsize(self) -> int: ...

    @property
    def kind(self) -> str: ...

    @property
    def metadata(self) -> Optional[Mapping[str, Any]]: ...

    @property
    def name(self) -> str: ...

    @property
    def num(self) -> int: ...

    @property
    def shape(self) -> _Shape: ...

    @property
    def ndim(self) -> int: ...

    @property
    def subdtype(self) -> Optional[Tuple[dtype, _Shape]]: ...

    def newbyteorder(self, new_order: str = ...) -> dtype: ...

    # Leave str and type for end to avoid having to use `builtins.str`
    # everywhere. See https://github.com/python/mypy/issues/3775
    @property
    def str(self) -> builtins.str: ...

    @property
    def type(self) -> Type[generic]: ...


_Dtype = dtype  # to avoid name conflicts with ndarray.dtype


class _flagsobj:
    aligned: bool
    updateifcopy: bool
    writeable: bool
    writebackifcopy: bool

    @property
    def behaved(self) -> bool: ...

    @property
    def c_contiguous(self) -> bool: ...

    @property
    def carray(self) -> bool: ...

    @property
    def contiguous(self) -> bool: ...

    @property
    def f_contiguous(self) -> bool: ...

    @property
    def farray(self) -> bool: ...

    @property
    def fnc(self) -> bool: ...

    @property
    def forc(self) -> bool: ...

    @property
    def fortran(self) -> bool: ...

    @property
    def num(self) -> int: ...

    @property
    def owndata(self) -> bool: ...

    def __getitem__(self, key: str) -> bool: ...

    def __setitem__(self, key: str, value: bool) -> None: ...


class flatiter:
    @property
    def base(self) -> ndarray: ...

    @property
    def coords(self) -> _Shape: ...

    @property
    def index(self) -> int: ...

    def copy(self) -> ndarray: ...

    def __iter__(self) -> flatiter: ...

    def __next__(self) -> Any: ...


_ArraySelf = TypeVar("_ArraySelf", bound=_ArrayOrScalarCommon)


class _ArrayOrScalarCommon(SupportsInt, SupportsFloat, SupportsComplex,
                           SupportsBytes, SupportsAbs[Any]):
    @property
    def T(self: _ArraySelf) -> _ArraySelf: ...

    @property
    def base(self) -> Optional[ndarray]: ...

    @property
    def dtype(self) -> _Dtype: ...

    @property
    def data(self) -> memoryview: ...

    @property
    def flags(self) -> _flagsobj: ...

    @property
    def size(self) -> int: ...

    @property
    def itemsize(self) -> int: ...

    @property
    def nbytes(self) -> int: ...

    @property
    def ndim(self) -> int: ...

    @property
    def shape(self) -> _Shape: ...

    @property
    def strides(self) -> _Shape: ...

    def __int__(self) -> int: ...

    def __float__(self) -> float: ...

    def __complex__(self) -> complex: ...
    if sys.version_info[0] < 3:
        def __oct__(self) -> str: ...

        def __hex__(self) -> str: ...

        def __nonzero__(self) -> bool: ...

        def __unicode__(self) -> Text: ...
    else:
        def __bool__(self) -> bool: ...

        def __bytes__(self) -> bytes: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __copy__(self: _ArraySelf, order: str = ...) -> _ArraySelf: ...

    def __deepcopy__(self: _ArraySelf, memo: dict) -> _ArraySelf: ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __add__(self, other): ...

    def __radd__(self, other): ...

    def __iadd__(self, other): ...

    def __sub__(self, other): ...

    def __rsub__(self, other): ...

    def __isub__(self, other): ...

    def __mul__(self, other): ...

    def __rmul__(self, other): ...

    def __imul__(self, other): ...

    if sys.version_info[0] < 3:
        def __div__(self, other): ...

        def __rdiv__(self, other): ...

        def __idiv__(self, other): ...

    def __truediv__(self, other): ...

    def __rtruediv__(self, other): ...

    def __itruediv__(self, other): ...

    def __floordiv__(self, other): ...

    def __rfloordiv__(self, other): ...

    def __ifloordiv__(self, other): ...

    def __mod__(self, other): ...

    def __rmod__(self, other): ...

    def __imod__(self, other): ...

    def __divmod__(self, other): ...

    def __rdivmod__(self, other): ...

    # NumPy's __pow__ doesn't handle a third argument
    def __pow__(self, other): ...

    def __rpow__(self, other): ...

    def __ipow__(self, other): ...

    def __lshift__(self, other): ...

    def __rlshift__(self, other): ...

    def __ilshift__(self, other): ...

    def __rshift__(self, other): ...

    def __rrshift__(self, other): ...

    def __irshift__(self, other): ...

    def __and__(self, other): ...

    def __rand__(self, other): ...

    def __iand__(self, other): ...

    def __xor__(self, other): ...

    def __rxor__(self, other): ...

    def __ixor__(self, other): ...

    def __or__(self, other): ...

    def __ror__(self, other): ...

    def __ior__(self, other): ...

    if sys.version_info[:2] >= (3, 5):
        def __matmul__(self, other): ...

        def __rmatmul__(self, other): ...

    def __neg__(self: _ArraySelf) -> _ArraySelf: ...

    def __pos__(self: _ArraySelf) -> _ArraySelf: ...

    def __abs__(self: _ArraySelf) -> _ArraySelf: ...

    def __invert__(self: _ArraySelf) -> _ArraySelf: ...

    # TODO(shoyer): remove when all methods are defined
    def __getattr__(self, name) -> Any: ...


class ndarray(_ArrayOrScalarCommon, Iterable, Sized, Container):
    real: ndarray
    imag: ndarray

    @property
    def dtype(self) -> _Dtype: ...

    @dtype.setter
    def dtype(self, value: _DtypeLike): ...

    @property
    def ctypes(self) -> _ctypes: ...

    @property
    def shape(self) -> _Shape: ...

    @shape.setter
    def shape(self, value: _ShapeLike): ...

    @property
    def flat(self) -> flatiter: ...

    @property
    def strides(self) -> _Shape: ...

    @strides.setter
    def strides(self, value: _ShapeLike): ...

    # Many of these special methods are irrelevant currently, since protocols
    # aren't supported yet. That said, I'm adding them for completeness.
    # https://docs.python.org/3/reference/datamodel.html
    def __len__(self) -> int: ...

    def __getitem__(self, key) -> Any: ...

    def __setitem__(self, key, value): ...

    def __iter__(self) -> Any: ...

    def __contains__(self, key) -> bool: ...

    def __index__(self) -> int: ...


class generic(_ArrayOrScalarCommon):
    def __init__(self, value: Any = ...) -> None: ...

    @property
    def base(self) -> None: ...


class _real_generic(generic):
    @property
    def real(self: _ArraySelf) -> _ArraySelf: ...

    @property
    def imag(self: _ArraySelf) -> _ArraySelf: ...


class number(generic):
    def __init__(
        self, value: Union[SupportsInt, SupportsFloat] = ...
    ) -> None: ...


class bool_(_real_generic):
    ...


class object_(generic):
    ...


class datetime64(_real_generic):
    ...


class integer(number, _real_generic):
    ...


class signedinteger(integer):
    ...


class int8(signedinteger):
    ...


class int16(signedinteger):
    ...


class int32(signedinteger):
    ...


class int64(signedinteger):
    ...


class timedelta64(signedinteger):
    ...


class unsignedinteger(integer):
    ...


class uint8(unsignedinteger):
    ...


class uint16(unsignedinteger):
    ...


class uint32(unsignedinteger):
    ...


class uint64(unsignedinteger):
    ...


class inexact(number):
    ...


class floating(inexact, _real_generic):
    ...


class float16(floating):
    ...


class float32(floating):
    ...


class float64(floating):
    ...


class complexfloating(inexact):
    def __init__(
        self,
        value: Union[SupportsInt, SupportsFloat, SupportsComplex,
                     complex] = ...,
    ) -> None: ...


class complex64(complexfloating):
    @property
    def real(self) -> float32: ...

    @property
    def imag(self) -> float32: ...


class complex128(complexfloating):
    @property
    def real(self) -> float64: ...

    @property
    def imag(self) -> float64: ...


class flexible(_real_generic):
    ...


class void(flexible):
    ...


class character(_real_generic):
    ...


class bytes_(character):
    ...


class str_(character):
    ...

# TODO(alan): Platform dependent types
# longcomplex, longdouble, longfloat
# bytes, short, intc, intp, longlong
# half, single, double, longdouble
# uint_, int_, float_, complex_
# float128, complex256
# float96


def array(
    object: object,
    dtype: _DtypeLike = ...,
    copy: bool = ...,
    subok: bool = ...,
    ndmin: int = ...) -> ndarray: ...


# TODO(shoyer): remove when the full numpy namespace is defined
def __getattr__(name: str) -> Any: ...
