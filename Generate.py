from Transaction import Transaction
from operator import attrgetter


class Generate:
    _counter = 1

    def __init__(self,
                 fec: list,
                 mtc: list,
                 time_generator,
                 priority: int = 0):
        self._fec = fec
        self._mtc = mtc
        self._priority = priority
        self._time_generator = time_generator
        self.cur_transaction = None


    def generate(self, cur_block):
        self._fec.append(Transaction(num=Generate._counter,
                                     transition_time=self._mtc[0] + next(self._time_generator),
                                     current_block=-1,
                                     priority=self._priority,
                                     next_block=cur_block))
        Generate._counter += 1
        self._fec.sort(key=attrgetter('transition_time'))

    def can_enter(self):
        return True

    def can_exit(self):
        return True

    def enter(self, t):
        if self.cur_transaction is not None:
            print('Потеря транзакта', t)
            return
        t.current_block = t.next_block
        t.next_block = t.next_block + 1
        t.transition_time = -1
        self.cur_transaction = t

    def exit(self):
        t = self.cur_transaction
        self.generate(t.current_block)
        self.cur_transaction = None
        return t
