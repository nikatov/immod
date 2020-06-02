class Transaction:
    def __init__(self,
                 num: int,
                 transition_time: float,
                 current_block: int,
                 priority: int,
                 next_block: int):
        self.num = num
        self.transition_time = transition_time
        self.current_block = current_block
        self.priority = priority
        self.next_block = next_block

    def __str__(self):
        string = '[' + str(self.num) + ','
        if self.transition_time == -1:
            string += 'КМР'
        else:
            string += str(self.transition_time)
        string += ','
        if self.current_block == -1:
            string += 'нет'
        else:
            string += str(self.current_block)

        string += ',' + str(self.priority) + ',' + str(self.next_block) + ']'
        return string

    def __repr__(self):
        return str(self)
