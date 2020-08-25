from dataclasses import dataclass
from typing import TypeVar, Union, Type, Any, Generic, Optional, Callable


T = TypeVar('T')


EventHandler = Callable[[Cell[T], str, Any], None]


class DataNode(Generic[T]):
    pass


class Immutable(DataNode[T]):

    __slots__ = '__content__', '__observers__'

    def __init__(self, value:T):
        self.__content__ = value
        self.__observers__ = None

    def __set_content__(self, value:T):
        self.__content__ = value

    def __add_observer__(self, observer:):

    def __str__(self):
        return self.__content__.__str__()

    def __repr__(self):
        return self.__content__.__repr__()

    def __getitem__(self, item):
        return self.__content__.__getitem__()

    def __setitem__(self, item):
        self.__content__.__setitem__()

    def __add__(self, other):
        return self.__content__.__add__(other)

    def __sub__(self, other):
        return self.__content__.__add__(other)

    def __mul__(self, other):
        return self.__content__.__add__(other)

    def __bool__(self):
        return self.__content__.__bool__()

    def __int__(self):
        return self.__content__.__int__()

    def __call__(self, *args, **kwargs):
        return self.__content__.__call__(*args, **kwargs)

    def __getattr__(self, item):
        return getattr(self.__content__, item)


class List(DataNode[T], list):

    def __init__(self):
        pass


def set(cell:Cell[T], value:T):
    cell.__set_content__(value)


EventHandlerDecorator = Callable[[EventHandler[T]], EventHandler[T]]
def observe(cell:Cell[T], observer:Optional[EventHandler[T]]=None)
    -> Union[EventHandler[T], EventHandlerDecorator]:
    if observer is not None:
        cell.__add_observer__(observer)
    else:
        def decorate(observer):
            cell.__add_observer__(observer)
        return decorate


class observable(Generic[T]):

    __NODEFAULT = object()

    __slots__ = 'name', 'default',

    def __init__(self, default:T=__NODEFAULT):
        self.default = None if default is self.__NODEFAULT else default

    def __set__(self, instance, value:T):
        if value is self:
            # workaround for dataclass with default value
            value = self.default
        try:
            cell = instance.__dict__[self.name]
        except KeyError:
            instance.__dict__[self.name] = Cell(value)
        else:
            set(cell, value)

    def __get__(self, instance, owner) -> T:
        if instance is None:
            return self
        try:
            cell = instance.__dict__[self.name]
        except KeyError:
            cell = instance.__dict__[self.name] = Cell(self.default)
        return cell

    def __set_name__(self, owner, name):
        self.name = name

    def __repr__(self):
        return f"observable({self.default})"


@dataclass
class Test:
    p1:int = observable(3)
    p2:str = observable("TEST")


def main():
    print("HALLO")
    t = Test(p1=99)
    t.p1 = 2
    print(t.p2)

if __name__ == '__main__':
    main()