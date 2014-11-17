__author__ = "Christophe"


# using duck typing at our advantage to serve generic logic to several enumeration classes
class BaseEnumeration():
    def __init__(self):
        pass

    @classmethod
    def intersect(cls, _flag, _referential):
        __flag = list(cls.decompose(_flag))
        __referential = list(cls.decompose(_referential))
        # print(__flag)
        # print(__referential)
        for _mask in __referential:
            if _mask in __flag:
                yield _mask

    @classmethod
    def contains(cls, _flag, _referential):
        return cls.intersect(_flag, _referential) is not []

    @classmethod
    def decompose(cls, _flag):
        if type(_flag) is not int:
            raise UserWarning("flag must be of type integer.")
        else:
            highest = sum([x.value for x in cls.flags()])
            if _flag > highest:
                raise UserWarning("flag's value: {} is higher than the total sum of enum's flags: {}.".format(
                    _flag,
                    highest
                ))
        for _mask in cls.flags():
            # _flag is Activity and (_mask.value & _flag.value) or
            if _mask.value & _flag:
                yield _mask

    @classmethod
    def flags(cls):
        _list = vars(cls).iteritems()
        _list.remove(cls.NONE)
        return _list

    @classmethod
    def tostring(cls, val):
        for k,v in cls.flags():
            if v == val:
                return k

    @classmethod
    def fromstring(cls, str):
        return getattr(cls, str.upper(), None)