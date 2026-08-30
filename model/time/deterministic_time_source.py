from .time_source_base import TimeSourceBase

class DeterministicTimeSource(TimeSourceBase):
    _counter: int = 0

    def advance(self, duration: int):
        self._counter += duration

    def now(self):
        return self._counter