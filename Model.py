from Generate import Generate
from Terminate import Terminate
from Queue import Queue
from Storage import Storage
import random


def time_generator(avg, first_one=False):
    if first_one:
        yield 1
    while True:
        yield random.expovariate(1./avg)


def const_generator(number):
    while True:
        yield number


class Model:
    def __init__(self):
        self._cec = []  # Сurrent Events Chain (цепь текущих событий)
        self._fec = []  # Future  Events Chain (цепь будущих событий)
        self._mtc = [0]  # Model Time Counter (счетчик времени моделирования)
        self._count = [1]
        self._blocks = []

    def init(self):
        self._blocks.append(Generate(fec=self._fec,
                                     mtc=self._mtc,
                                     time_generator=time_generator(39, first_one=True)))
        self._blocks.append(Queue())
        self._blocks.append(Storage(cec=self._cec,
                                    fec=self._fec,
                                    mtc=self._mtc,
                                    time_generator=time_generator(229),
                                    max_len=2))
        self._blocks.append(Terminate(cec=self._cec,
                                      counter=self._count))
        self._blocks.append(Generate(fec=self._fec,
                                     mtc=self._mtc,
                                     time_generator=const_generator(240)))
        self._blocks.append(Terminate(cec=self._cec,
                                      counter=self._count,
                                      decrement=1))

    def run(self):
        self.print_info('До стадии ввода')
        self._insert()
        self.print_info('После стадии ввода')
        while self._count[0] != 0:
            self._timer_correction()
            self.print_info('После стадии коррекции таймера')
            self._view()
            self.print_info('После стадии просмотра')

    def _insert(self):
        for i, block in enumerate(self._blocks):
            if isinstance(block, Generate):
                block.generate(cur_block=i)

    def _timer_correction(self):
        if len(self._fec) == 0:
            exit('Произошла ошибка. Цепь будущих событий опустела раньше окончания программы.')
        t = self._fec[0]
        self._mtc[0] = t.transition_time
        self._fec.remove(t)
        t.transition_time = -1
        self._cec.append(t)
        while len(self._fec) != 0 and self._fec[0].transition_time == self._mtc[0]:
            t = self._fec[0]
            self._fec.remove(t)
            t.transition_time = -1
            self._cec.append(t)

    def _view(self):
        f_change = True
        while f_change:
            f_change = False
            for t in self._cec:
                while self._blocks[t.current_block].can_exit() and self._blocks[t.next_block].can_enter():
                    f_change = True
                    # print('Переход транзакта', t.num, 'из блока', t.current_block, 'в блок', t.next_block)
                    if t.current_block != -1:
                        self._blocks[t.current_block].exit()
                    self._blocks[t.next_block].enter(t)
                    if len(self._cec) == 0:
                        return
                    t = self._cec[0]

    def print_info(self, stage: str):
        print(stage + ':')
        print('ТМВ:', self._mtc[0])
        print('ЦТС:', self._cec)
        print('ЦБС:', self._fec)
        print()
