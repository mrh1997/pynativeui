from __future__ import annotations
from typing import (
    Generic,
    TypeVar,
    Callable,
    Union,
    Set,
    List,
    Optional,
    Dict,
    Tuple,
)
from collections.abc import MutableSequence
from dataclasses import dataclass
from contextvars import ContextVar
from functools import wraps


T = TypeVar("T")


class Operation:
    pass


__reads: ContextVar[Optional[Set[Box]]] = ContextVar("reads", default=None)
__writes: ContextVar[Dict[Box, List[Tuple[int, Operation]]]] = ContextVar(
    "writes", default={}
)
__write_cntr: ContextVar[int] = ContextVar("write_cntr", default=0)


def readaccess(method):
    @wraps(method)
    def mark_read(self, *args, **kwargs):
        reads = __reads.get()
        if reads is not None:
            reads.add(self)
        return method(self, *args, **kwargs)

    return mark_read


def writeaccess(method):
    @wraps(method)
    def add_op(self, *args, **kwargs):
        writes = __writes.get()
        if writes is not None:
            writes.add(self)
        return method(self, *args, **kwargs)

    return add_op


class Box(Generic[T]):
    def __init__(self, observers):
        self.__observers__ = observers
        self.__delegate__ = None


class BoxedList(MutableSequence, Box[List[T]]):
    @readaccess
    def __iter__(self):
        pass

    @readaccess
    def __repr__(self):
        return repr(self.data)

    @readaccess
    def __lt__(self, other):
        return self.data < self.__cast(other)

    @readaccess
    def __le__(self, other):
        return self.data <= self.__cast(other)

    @readaccess
    def __eq__(self, other):
        return self.data == self.__cast(other)

    @readaccess
    def __gt__(self, other):
        return self.data > self.__cast(other)

    @readaccess
    def __ge__(self, other):
        return self.data >= self.__cast(other)

    @readaccess
    def __contains__(self, item):
        return item in self.data

    @readaccess
    def __len__(self):
        return len(self.data)

    @readaccess
    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self.data[i])
        else:
            return self.data[i]

    ###
    def __setitem__(self, i, item):
        self.data[i] = item

    ###
    def __delitem__(self, i):
        del self.data[i]

    @readaccess
    def __add__(self, other):
        if isinstance(other, UserList):
            return self.__class__(self.data + other.data)
        elif isinstance(other, type(self.data)):
            return self.__class__(self.data + other)
        return self.__class__(self.data + list(other))

    ###
    def __radd__(self, other):
        if isinstance(other, UserList):
            return self.__class__(other.data + self.data)
        elif isinstance(other, type(self.data)):
            return self.__class__(other + self.data)
        return self.__class__(list(other) + self.data)

    @readaccess
    def __iadd__(self, other):
        if isinstance(other, UserList):
            self.data += other.data
        elif isinstance(other, type(self.data)):
            self.data += other
        else:
            self.data += list(other)
        return self

    @readaccess
    def __mul__(self, n):
        return self.__class__(self.data * n)

    __rmul__ = __mul__

    ###
    def __imul__(self, n):
        self.data *= n
        return self

    @readaccess
    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        # Create a copy and avoid triggering descriptors
        inst.__dict__["data"] = self.__dict__["data"][:]
        return inst

    ###
    def append(self, item):
        self.data.append(item)

    ###
    def insert(self, i, item):
        self.data.insert(i, item)

    ###
    def pop(self, i=-1):
        return self.data.pop(i)

    ###
    def remove(self, item):
        self.data.remove(item)

    ###
    def clear(self):
        self.data.clear()

    @readaccess
    def copy(self):
        return self.__class__(self)

    @readaccess
    def count(self, item):
        return self.data.count(item)

    @readaccess
    def index(self, item, *args):
        return self.data.index(item, *args)

    ###
    def reverse(self):
        self.data.reverse()

    ###
    def sort(self, /, *args, **kwds):
        self.data.sort(*args, **kwds)

    ###
    def extend(self, other):
        if isinstance(other, UserList):
            self.data.extend(other.data)
        else:
            self.data.extend(other)
