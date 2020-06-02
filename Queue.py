from collections import deque


class Queue:
    def __init__(self, max_len: int = None):
        self._m_len = max_len
        self._q = deque()

    def can_enter(self):
        if self._m_len is None:
            return True
        return len(self._q) < self._m_len

    def can_exit(self):
        return True

    def enter(self, t):
        t.current_block = t.next_block
        t.next_block = t.next_block + 1
        t.transition_time = -1
        self._q.appendleft(t)

    def exit(self):
        return self._q.pop()
