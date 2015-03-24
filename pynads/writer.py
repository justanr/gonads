from .monad import Monad
from .functor import fmap

class Writer(Monad):
    """Stores a value as well as a log of events that have transpired
    with the value.
    """
    def __init__(self, v, log):
        self.v = v

        if not isinstance(log, list):
            self.log = [log]
        else:
            self.log = log

    @classmethod
    def unit(cls, v):
        return cls(v, [])

    def fmap(self, f):
        return Writer(f(self.v), self.log)

    def apply(self, applicative):
        return fmap(self.v, applicative)

    def bind(self, f):
        v, msg = f(self.v)
        return Writer(v, self.log + [msg])

    def __repr__(self):
        return "Writer({!r}, {!r})".format(self.v, self.log)