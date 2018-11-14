from Constants import INITIAL_CASH_TO_THE_PLAYER
import copy
from enum import Enum

class Phase(Enum):
    DICE_ROLL= 0
    BSMT = 1
    TRADE_OFFER = 2
    DICE_ROLL = 3
    BUY_UNOWNED_PROPERTY = 4
    AUCTION_PROPERTY = 5
    PAY_RENT_UNOWNED_PROPERTY = 6
    JAIL = 7
    CHANCE_CARD = 8
    COMMUNITY_CARD = 9

class GameState:
    def __init__(self, turn_id=0, property_status= ()*42, players_position=(0,0),
                 players_cash=(INITIAL_CASH_TO_THE_PLAYER, INITIAL_CASH_TO_THE_PLAYER),
                 phase= Phase.DICE_ROLL, additional_info={}, debt=None, past_states=[]):
        self.turn_id = turn_id
        self.property_status = property_status
        self.players_position = players_position
        self.players_cash = players_cash
        self.phase=phase
        self.additional_info= additional_info
        self.debt=debt
        self.past_states=past_states

    def update_player_position(self, turn_id, moves):
        if turn_id % 2 == 0:
            self.players_position = (self.players_position[0] + moves, self.players_position[1])
        else:
            self.players_position = (self.players_position, self.players_position[1]+moves)

    def update_turn_id(self, turn_id):
        self.turn_id = turn_id

    def get_game_state(self, ):
        return copy.deepcopy(self)


