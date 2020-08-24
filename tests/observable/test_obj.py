import pytest
from unittest.mock import Mock
from pynativeui.observable.obj import Observable


class TestObj:
    def test_getWrapped_retrievesObjPassedToInit(self):
        obs_obj = Observable(123)
        assert obs_obj.wrapped == 123

    def test_setWrapped_modifiesValue(self):
        obs_obj = Observable(123)
        obs_obj.wrapped = 22
        assert obs_obj.wrapped == 22

    def test_setWrapped_onObserved_callsObserver(self):
        obs_obj = Observable(123)
        obs_obj.observe(observer := Mock())
        obs_obj.wrapped = 2
        observer.assert_called_once_with(obs_obj, None, 123, 2)

    def test_isinstance_onObservable_returnsTrue(self):
        obs_obj = Observable(123)
        assert isinstance(obs_obj, Observable)

    def test_isinstance_onWrappedType_returnsTrue(self):
        assert isinstance(Observable(1), int)
