import dataclasses
import random

import bank


MoneyAmount = int


@dataclasses.dataclass
class PlayerBet:
    amount: MoneyAmount
    cho_hun: bank.ChoHan
    player: 'Player'


class Player:
    number = 0

    def __new__(cls, *args, **kwargs):
        cls.number += 1
        return super().__new__(cls)

    def __init__(self, start_money: MoneyAmount):
        self.money = start_money

    def _ask_amount(self) -> MoneyAmount:
        raise NotImplemented

    def _ask_cho_or_han(self) -> bank.ChoHan:
        raise NotImplemented

    def make_bet(self) -> PlayerBet:
        money_amount = self._ask_amount()
        cho_or_hun = self._ask_cho_or_han()
        return PlayerBet(money_amount, cho_or_hun, self)

    def get_reward(self, money: MoneyAmount) -> None:
        self.money += money

    def lose_money(self, money: MoneyAmount) -> None:
        self.money -= money
    
    def get_left_money(self) -> MoneyAmount:
        return self.money


class HumanPlayer(Player):
    INPUT_MESSAGE = 'Введите размер ставки(не более {left_money} и не менее {min_bet}): '

    def __init__(self, start_money):
        super().__init__(start_money)
        self.number = HumanPlayer.number

    def _ask_amount(self) -> MoneyAmount:
        amount = None
        while not amount:
            amount = MoneyAmount(input(HumanPlayer.INPUT_MESSAGE.format(left_money=self.money, min_bet=bank.Bank.MIN_BET)))
            if amount > self.money or amount < bank.Bank.MIN_BET:
                print('Ваша ставка не подходит по лимитам, введите другую!')
                amount = None

        print('Ставка принята')
        return amount

    def _ask_cho_or_han(self) -> bank.ChoHan:
        cho_or_han = None
        while not cho_or_han:
            cho_or_han = MoneyAmount(input('Выберите чётное или не чётное. Если чётное, то введите 0, иначе 1: '))

            try:
                cho_or_han = bank.ChoHan(cho_or_han)
            except Exception:
                print('Введённое значение не подходит. Введите 0 или 1.')
                cho_or_han = None

        return cho_or_han

    def __str__(self):
        return f'HumanPlayer({self.number})'


class AIPlayer(Player):
    def __init__(self, start_money):
        super().__init__(start_money)
        self.number = AIPlayer.number

    def _ask_amount(self) -> MoneyAmount:
        return random.randint(bank.Bank.MIN_BET, self.money)

    def _ask_cho_or_han(self) -> bank.ChoHan:
        return bank.ChoHan(random.randint(0, 1))

    def __str__(self):
        return f'AIPlayer({self.number})'
