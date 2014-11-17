__author__ = "Christophe"

from enum import Enum


class Activity(Enum):
    NONE = 0
    NEPHROLOGY = 1 << 1
    DIALYSIS = 1 << 2
    CONSULTATION = 1 << 3
    OTHERS = 1 << 4
    OBLIGATION = 1 << 5
    OBLIGATION_HOLIDAY = 1 << 6
    OBLIGATION_WEEKEND = 1 << 7

    @classmethod
    def intersect(cls, _flag, _referential):
        __flag = list(Activity.decompose(_flag))
        __referential = list(Activity.decompose(_referential))
        # print(__flag)
        # print(__referential)
        for _mask in __referential:
            if _mask in __flag:
                yield _mask

    @classmethod
    def contains(cls, _flag, _referential):
        return Activity.intersect(_flag, _referential) is not []

    @classmethod
    def decompose(cls, _flag):
        if type(_flag) is not int:
            raise UserWarning("flag must be of type integer.")
        else:
            highest = sum([x.value for x in Activity.flags()])
            if _flag > highest:
                raise UserWarning("flag's value: {} is higher than the total sum of enum's flags: {}.".format(
                    _flag,
                    highest
                ))
        for _mask in Activity.flags():
            # _flag is Activity and (_mask.value & _flag.value) or
            if _mask.value & _flag:
                yield _mask

    @classmethod
    def flags(cls):
        _list = list(Activity)
        _list.remove(Activity.NONE)
        return _list

    @classmethod
    def tostring(cls, val):
        for k,v in vars(cls).iteritems():
            if v == val:
                return k

    @classmethod
    def fromstring(cls, str):
        return getattr(cls, str.upper(), None)

# print(list(Activity.intersect(47, 31)))
# print(Activity.flags().pop())