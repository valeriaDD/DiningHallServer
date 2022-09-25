from src.Waiter import Waiter
from src.Tables import Tables


class Waiters:

    def __init__(self, nr_of_waiters: int, tables: Tables):
        self.nr_of_waiters = nr_of_waiters
        self.tables = tables
        self.waiters = []

        for waiter_id in range(1, self.nr_of_waiters + 1):
            self.waiters.append(Waiter(waiter_id))
