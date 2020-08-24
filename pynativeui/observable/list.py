from typing import TypeVar, Generic, List, Union, SupportsIndex
from collections.abc import MutableSequence
from .obj import Observable, observable, InitT, ensure_is_popo


T = TypeVar("T")


class ObservableList(Observable, MutableSequence, Generic[T]):
    def __init__(self, initlist: List[InitT]):
        ensure_is_popo(initlist)
        super().__init__(initlist)

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

    def __wrap__(self, popo_lst):
        return list(map(observable, popo_lst))

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

    def insert(self, index: int, obj: T):
        ensure_is_popo((obj))
