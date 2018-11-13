import json
import Property
import Board
import Constants
import GameState
import Utility
import Player
from pprint import pprint


class Adjudicator:
   
    def __init__(self):
        self.turn_limit = Constants.TURN_LIMIT
        self.player_count = Constants.PLAYER_COUNT
        self.player_instances = []
        self.game_state = None
        self.board_instance = Board.Board()

    def run_player_on_state(self, player, state):
        pass

    def broad_cast_state(self, player1, player2, state):
        pass

    def get_current_player(self, turn_id):
        player_id = turn_id % self.player_count
        return self.player_instances[player_id]

    def init_game_state(self, player_instances):
        self.game_state = GameState.GameState(player_instances)

    def run_game(self, player1, player2, dice_rolls=None, chance_cards=None, community_chest_cards=None):

        self.player_instances = [player1, player2]
        self.init_game_state(self.player_instances)
        turn_id = self.game_state.get_turn_id()
        while turn_id < self.turn_limit:
            dice = None
            if dice_rolls is not None:
                dice = Utility.Dice(dice_rolls[turn_id][0], dice_rolls[turn_id][1])
            else:
                dice = Utility.Dice()
                dice.perform_roll()

            current_player = self.get_current_player(turn_id)

            if dice.is_double():
                current_player.doubles_count += 1
            else:
                current_player.doubles_count = 0
            self.game_state.update_turn_id(turn_id)
            print(turn_id, current_player.get_id(), dice.get_dice_roll1(), dice.get_dice_roll2(),
                  current_player.doubles_count)
            turn_id += 1

    def perform_jail_activity(self):
        pass

    def complete_player_move(self):
        pass


if __name__ == '__main__':
    player_one = Player.Player(0, 0, Constants.INITIAL_CASH_TO_THE_PLAYER, [], 0)
    player_two = Player.Player(1, 0, Constants.INITIAL_CASH_TO_THE_PLAYER, [], 1)
    Adjudicator().run_game(player_one, player_two)
