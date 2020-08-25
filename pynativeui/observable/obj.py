from typing import Callable, TypeVar, Generic, Union

T = TypeVar("T")
InitT = Union[T, "ObservableObj[T]"]


Observer = Callable[["Observable"], None]


def observable(obj: InitT):
    if isinstance(obj, Observable):
        return obj
    else:
        return Observable(obj)


def ensure_is_popo(obj):
    """
    Ensure that obj is a POPO (Plain Old Python Object) and not an Observable.
    """
    if isinstance(obj, Observable):
        raise ValueError(
            f"Value {obj!r} must be pure python object (not Observable)"
        )


class Observable(Generic[T]):
    def __init__(self, initval: T):
        ensure_is_popo(initval)
        super().__init__()
        self.__wrapped__ = self.__wrap__(initval)
        self.__observers__ = set()

    def __repr__(self):
        return f"{type(self).__name__}({self.__wrapped__})"

    def __notify__(self, identifier, old_value, new_value):
        for observer in self.__observers__:
            observer(self, identifier, old_value, new_value)

    def observe(self, observer: Observer):
        self.__observers__.add(observer)

    @property
    def wrapped(self) -> T:
        return self.__wrapped__

    @wrapped.setter
    def wrapped(self, newobj: T):
        ensure_is_popo(newobj)
        oldobj = self.__wrapped__
        self.__wrapped__ = self.__wrap__(newobj)
        self.__notify__(None, oldobj, newobj)

    def __wrap__(self, popo_obj):
        return popo_obj

    @property
    def __class__(self):
        return self.__wrapped__.__class__

    def __len__(self):
        return self.__wrapped__.__len__()

    def __getitem__(self, ndx):
        return self.__wrapped__.__getitem__(ndx)

    def __call__(self, *args, **kwargs):
        return self.__wrapped__.__call__(*args, **kwargs)

    def __eq__(self, other):
        return self.__wrapped__.__eq__(other)

    def __ne__(self, other):
        return self.__wrapped__.__ne__(other)

    def __gt__(self, other):
        return self.__wrapped__.__gt__(other)

    def __lt__(self, other):
        return self.__wrapped__.__lt__(other)

    def __ge__(self, other):
        return self.__wrapped__.__ge__(other)

    def __le__(self, other):
        return self.__wrapped__.__le__(other)

    def __add__(self, other):
        return self.__wrapped__.__add__(other)

    def __radd__(self, other):
        return self.__wrapped__.__radd__(other)

    def __sub__(self, other):
        return self.__wrapped__.__sub__(other)

    def __rsub__(self, other):
        return self.__wrapped__.__rsub__(other)

    def __mul__(self, other):
        return self.__wrapped__.__mul__(other)

    def __rmul__(self, other):
        return self.__wrapped__.__rmul__(other)

    def __truediv__(self, other):
        return self.__wrapped__.__truediv__(other)

    def __itruediv__(self, other):
        return self.__wrapped__.__itruediv__(other)

    def __rtruediv__(self, other):
        return self.__wrapped__.__rtruediv__(other)

    def __floordiv__(self, other):
        return self.__wrapped__.__floordiv__(other)

    def __rfloordiv__(self, other):
        return self.__wrapped__.__rfloordiv__(other)

    def __bool__(self):
        return self.__wrapped__.__bool__()
