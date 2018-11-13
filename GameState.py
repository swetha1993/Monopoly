import Constants
import Player


class PlayerState:
    def __init__(self, player_id, player_position, player_cash, player_turn):
        self.player_id = player_id
        self.player_cash = player_cash
        self.player_position = player_position
        self.player_turn = player_turn


class GameState:
    def __init__(self, player_instances):
        self.turn_id = 0
        self.property_ownership = [None] * 40
        self.player_info = dict()
        self.initialize_players(player_instances)
        self.initialize_properties()

    def initialize_players(self, player_instances):
        for i in range(len(player_instances)):
            player_id = player_instances[i].get_id()
            self.player_info[player_id] = PlayerState(player_instances[i].get_id(),
                                                player_instances[i].get_position(),
                                                player_instances[i].get_cash(),
                                                player_instances[i].get_turn_no()
                                                )

    def initialize_properties(self):
        pass

    def get_turn_id(self):
        return self.turn_id

    def update_turn_id(self, turn_id):
        self.turn_id = turn_id
