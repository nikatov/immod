from operator import attrgetter


class Storage:
    def __init__(self,
                 cec: list,
                 fec: list,
                 mtc: list,
                 time_generator,
                 max_len: int = None):
        self._cec = cec
        self._fec = fec
        self._mtc = mtc
        self._time_generator = time_generator
        self._m_len = max_len
        self._s = 0

    def can_enter(self):
        if self._m_len is None:
            return True
        return self._s < self._m_len

    def can_exit(self):
        return True

    def enter(self, t):
        self._s += 1
        t.current_block = t.next_block
        t.next_block = t.next_block + 1
        t.transition_time = self._mtc[0] + next(self._time_generator)
        self._fec.append(t)
        self._cec.remove(t)
        self._fec.sort(key=attrgetter('transition_time'))

    def exit(self):
        self._s -= 1
