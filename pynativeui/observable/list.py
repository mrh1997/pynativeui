from typing import TypeVar, Generic, List, Union, SupportsIndex
from collections.abc import MutableSequence
from .obj import Observable, observable, InitT, ensure_is_popo


T = TypeVar("T")


class ObservableList(MutableSequence, Observable, Generic[T]):
    def __init__(self, initlist: List[InitT]):
        ensure_is_popo(initlist)
        super().__init__(initlist)

    @staticmethod
    def __wrap__(popo_lst):
        return list(map(observable, popo_lst))

    def __len__(self):
        return len(self.__wrapped__)

    def __getitem__(
        self, index: Union[SupportsIndex, slice]
    ) -> Union["ObservableList[T]", Observable[T]]:
        if isinstance(index, slice):
            sliced_lst = ObservableList([])
            sliced_lst.__observers__ = self.__observers__.copy()
            sliced_lst.__wrapped__ = self.__wrapped__[index]
            return sliced_lst
        else:
            return self.wrapped[index]

    def __setitem__(
        self, index: Union[SupportsIndex, slice], value: InitT,
    ):
        if isinstance(index, slice):
            old_value = self.__wrapped__[index]
            new_value = self.__wrap__(value)
        else:
            old_value = [self.__wrapped__[index]]
            new_value = [observable(value)]
            index = slice(index, index + 1)
        self.__wrapped__.__setitem__(index, new_value)
        self.__notify__(index, old_value, new_value)

    def __delitem__(self, ndx):
        old_value = self.__wrapped__[ndx]
        del_slice = ndx if isinstance(ndx, slice) else slice(ndx, ndx + 1)
        self.__wrapped__.__delitem__(ndx)
        self.__notify__(del_slice, old_value, [])

    def insert(self, index: int, obj: T):
        ensure_is_popo((obj))
        wrapped_obj = observable(obj)
        self.__wrapped__.insert(index, wrapped_obj)
        self.__notify__(slice(index, index), [], [wrapped_obj])

    def extend(self, newobjs):
        size = len(self.__wrapped__)
        ensure_is_popo(newobjs)
        wrapped_objs = self.__wrap__(newobjs)
        self.__wrapped__.extend(wrapped_objs)
        self.__notify__(slice(size, size), [], wrapped_objs)

    def reverse(self):
        oldlist = self.__wrapped__
        newlist = list(reversed(self.__wrapped__))
        self.__wrapped__ = newlist
        self.__notify__(slice(0, len(oldlist)), oldlist, newlist)
