from .time_source_base import TimeSourceBase
import time

class RealTimeSource(TimeSourceBase):
    _counter: int = int(time.monotonic() * 1000)

    def advance(self, duration: int):
        # can't arbitrarily control time in real life
        self._counter = int(time.monotonic() * 1000)

    def now(self):
        return self._counter