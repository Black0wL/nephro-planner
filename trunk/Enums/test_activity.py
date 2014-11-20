from unittest import TestCase
from activity import Activity

__author__ = 'Christophe'


class TestActivity(TestCase):
    def test_intersect(self, _flag, _referential):
        pass

    def test_decompose(self):
        self.assertRaises(UserWarning, Activity.decompose, [])
        self.assertRaises(UserWarning, Activity.decompose, 4.3)
        self.assertRaises(UserWarning, Activity.decompose, 'nop')
        self.assertRaises(UserWarning, Activity.decompose, sum([x.value for x in Activity.flags()])+1)