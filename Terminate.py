class Terminate:
    def __init__(self,
                 counter: list,
                 cec: list,
                 decrement: int = 0):
        self._cec = cec
        self._counter = counter
        self._decrement = decrement

    def can_enter(self):
        return True

    def can_exit(self):
        return True

    def enter(self, t):
        self._cec.remove(t)
        self._counter[0] -= self._decrement

    def exit(self, t):
        pass
