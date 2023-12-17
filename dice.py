import random

import bank


class Dices:
    @staticmethod
    def _get_random() -> int:
        return random.randint(1, 6)

    def get_result(self) -> bank.ChoHan:
        first_dice = self._get_random()
        second_dice = self._get_random()
        sum_dice = first_dice + second_dice
        return bank.ChoHan(sum_dice % 2)
