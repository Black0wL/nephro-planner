__author__ = "Christophe"

from enum import Enum


class TimeSlot(Enum):
    NONE = 0
    FIRST_SHIFT = 1
    SECOND_SHIFT = 2
    THIRD_SHIFT = 4
    ALL_DAY = 8
    ALL_WEEKEND = 16

    @classmethod
    def intersect(cls, _flag, _referential):
        __flag = list(TimeSlot.decompose(_flag))
        __referential = list(TimeSlot.decompose(_referential))
        # print(__flag)
        # print(__referential)
        for _mask in __referential:
            if _mask in __flag:
                yield _mask

    @classmethod
    def contains(cls, _flag, _referential):
        return TimeSlot.intersect(_flag, _referential) is not []

    @classmethod
    def decompose(cls, _flag):
        if type(_flag) is not int:
            raise UserWarning("flag must be of type integer.")
        else:
            highest = sum([x.value for x in TimeSlot.flags()])
            if _flag > highest:
                raise UserWarning("flag's value: {} is higher than the total sum of enum's flags: {}.".format(
                    _flag,
                    highest
                ))
        for _mask in TimeSlot.flags():
            if _mask.value & _flag:
                yield _mask

    @classmethod
    def flags(cls):
        _list = list(TimeSlot)
        _list.remove(TimeSlot.NONE)
        return _list
