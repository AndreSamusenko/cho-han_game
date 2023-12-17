import enum


class ChoHan(enum.Enum):
    cho = 0
    han = 1

    def __str__(self):
        return str(self.value)


class Bank:
    MIN_BET = 100
    WIN_COEFFICIENT = 1.9

    @staticmethod
    def count_reward(money):
        return int(money * Bank.WIN_COEFFICIENT)
