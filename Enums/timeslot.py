__author__ = "Christophe"

from base import Base


class TimeSlot(Base):
    NONE = 0
    FIRST_SHIFT = 1 << 0
    SECOND_SHIFT = 1 << 1
    THIRD_SHIFT = 1 << 2

# print(TimeSlot.FIRST_SHIFT.value)
# print(TimeSlot.SECOND_SHIFT.value)
# print(TimeSlot.THIRD_SHIFT.value)
# print(TimeSlot.contains(2, 5))