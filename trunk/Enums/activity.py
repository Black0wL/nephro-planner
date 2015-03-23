__author__ = "Christophe"

from base import Base


class Activity(Base):
    NONE = 0
    NEPHROLOGY = 1 << 0
    DIALYSIS = 1 << 1
    CONSULTATION = 1 << 2
    OTHERS = 1 << 3
    OBLIGATION = 1 << 4
    OBLIGATION_HOLIDAY = 1 << 5
    OBLIGATION_WEEKEND = 1 << 6
    OBLIGATION_RECOVERY = 1 << 7

# print(1 << 1)
# print(list(Activity.intersect(47, 31)))
# print(list(Activity.decompose(49)))
# print(Activity.flags().pop())
# print(Activity.contains(1, 4))