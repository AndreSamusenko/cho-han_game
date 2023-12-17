import typing

import bank
import dice
import player


class Game:
    HUMAN_PLAYERS_MESSAGE = 'Сколько будет играть людей?'
    AI_PLAYERS_MESSAGE = 'Сколько AI игроков будет?'
    START_MONEY = 1200

    def __init__(self):
        human_players_num, ai_players_num = self._start_input()

        self.players: typing.List[player.Player] = [player.HumanPlayer(Game.START_MONEY)
                                                    for _ in range(human_players_num)]
        self.players.extend([player.AIPlayer(Game.START_MONEY) for _ in range(ai_players_num)])

        self.dices = dice.Dices()

    def _one_round(self):
        bets = []
        for player_ in self.players:
            print(f'{player_} >> ', end='')
            bet = player_.make_bet()
            bets.append(bet)
            print(f'Сделанная ставка = {bet.amount} на {bet.cho_hun}')

        print(' =================== ')
        dices_result = self.dices.get_result()
        print(f'Результат броска кубиков: {dices_result}')

        for bet in bets:
            if bet.cho_hun == dices_result:
                bet.player.get_reward(bank.Bank.count_reward(bet.amount))
                print(f'{bet.player} выиграл. Остаток денег: {bet.player.get_left_money()}')
            else:
                bet.player.lose_money(bet.amount)
                print(f'{bet.player} проиграл. Остаток денег: {bet.player.get_left_money()}')

        self._check_losers()

    def start_game(self):
        while self.players:
            self._one_round()
            if len(self.players) == 1:
                print(f'Игрок {self.players[0]} победил!!!')
                return

        print('Все обеднели и проиграли...')

    def _check_losers(self):
        players_num = len(self.players)

        for i, player_ in zip(range(players_num - 1, -1, -1), self.players[::-1]):
            if player_.money < bank.Bank.MIN_BET:
                self.players.pop(i)
                print(f"Игрок {player_} обеднел и выбыл...")

    @staticmethod
    def _start_input() -> typing.Tuple[int, int]:
        human_players_num = int(input(Game.HUMAN_PLAYERS_MESSAGE))
        ai_players_num = int(input(Game.AI_PLAYERS_MESSAGE))
        return human_players_num, ai_players_num
