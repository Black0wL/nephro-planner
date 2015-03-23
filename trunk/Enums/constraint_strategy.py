__author__ = "Christophe"

from base import Base

class ConstraintStrategy(Base):
    NONE = 0
    FOCUS_ON_PREFERENCES = 1 << 0
    DISCARD_COUNTERS = 1 << 1

# print (ConstraintStrategy.contains(ConstraintStrategy.FOCUS_ON_PREFERENCES, ConstraintStrategy.DISCARD_AVERSIONS))
# print (list(ConstraintStrategy.decompose(ConstraintStrategy.FOCUS_ON_PREFERENCES.value)))
# print (list(ConstraintStrategy.decompose(ConstraintStrategy.DISCARD_AVERSIONS.value)))