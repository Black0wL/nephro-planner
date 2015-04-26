__author__ = 'Christophe'


class Preferences(dict):
   def __init__(self,*arg,**kw):
      super(Preferences, self).__init__(*arg, **kw)