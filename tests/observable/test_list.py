import pytest
from unittest.mock import Mock
from pynativeui.observable.list import ObservableList
from pynativeui.observable.obj import Observable


class TestObservableList:
    @pytest.fixture
    def obs_list(self):
        return ObservableList([1, 22])

    def test_getWrapped_retrievesListOfObservables(self):
        obs_list = ObservableList([123])
        assert obs_list.wrapped == [123]

    def test_setList_replacesListElementsByObservable(self, obs_list):
        obs_list.wrapped = [1, 2, 3, 4]
        assert isinstance(obs_list[0], Observable)
        assert obs_list[0] == 1

    def test_len_forwardsToList(self):
        assert len(ObservableList([1, 2, 3, 4, 5])) == 5

    def test_getitem_onIndex_returnsAlwaysSameObservableToValue(self):
        obs_list = ObservableList([1, 2, 3])
        obs_obj_at_index_1 = obs_list[1]
        assert isinstance(obs_obj_at_index_1, Observable)
        assert obs_obj_at_index_1.wrapped == 2
        assert obs_obj_at_index_1 is obs_list.wrapped[1]

    def test_getItem_onSlice_createsObserviableListWithSameObservers(self):
        obs_list = ObservableList([1, 2, 3])
        obs_list.observe(observer := Mock())
        sliced_obs_list = obs_list[1:2]
        sliced_obs_list.__notify__(None, 123, 456)
        observer.assert_called_once_with(sliced_obs_list, None, 123, 456)

    def test_setItem_onIndex_createsObservableProxy(self, obs_list):
        obs_list[1] = 123
        assert isinstance(obs_list[1], Observable)
        assert obs_list[1] == 123

    def test_setItem_onSlice_createsObservableProxy(self, obs_list):
        obs_list[1] = 123
        assert isinstance(obs_list[1], Observable)
        assert obs_list[1] == 123

    def test_setItem_onSlice_notifyChanges(self):
        obs_list = ObservableList([1, 2, 3, 4])
        obs_list.observe(observer := Mock())
        obs_list[1] = 11
        observer.assert_called_once_with(obs_list, slice(1, 2), [2], [11])

    def test_setItem_onSlice_notifyChangesWithNewSliceAndOldValues(self):
        obs_list = ObservableList([1, 2, 3, 4])
        obs_list.observe(observer := Mock())
        obs_list[1:3] = [11, 22, 33]
        observer.assert_called_once_with(
            obs_list, slice(1, 3), [2, 3], [11, 22, 33]
        )

    def test_delItem_removesItemsAndNotifies(self):
        obs_list = ObservableList([1, 2, 3, 4])
        obs_list.observe(observer := Mock())
        del obs_list[1:3]
        observer.assert_called_once_with(obs_list, slice(1, 3), [2, 3], [])
        assert obs_list == [1, 4]

    def test_insert_addsWrappedElementAndNotifies(self):
        obs_list = ObservableList([1, 2, 3])
        obs_list.observe(observer := Mock())
        obs_list.insert(1, 11)
        observer.assert_called_once_with(obs_list, slice(1, 1), [], [11])
        assert obs_list == [1, 11, 2, 3]
        assert isinstance(obs_list[1], Observable)

    def test_extend_addsListAndCallsNotify(self):
        obs_list = ObservableList([1, 2, 3])
        obs_list.observe(observer := Mock())
        obs_list.extend([11, 22])
        observer.assert_called_with(obs_list, slice(3, 3), [], [11, 22])
        assert obs_list == [1, 2, 3, 11, 22]
        assert isinstance(obs_list[3], Observable)

    def test_reverse_notifiesForAllObjs(self):
        obs_list = ObservableList([1, 2, 3])
        obs_list.observe(observer := Mock())
        obs_list.reverse()
        observer.assert_called_with(
            obs_list, slice(0, 3), [1, 2, 3], [3, 2, 1]
        )
        assert obs_list == [3, 2, 1]
