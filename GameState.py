from Constants import INITIAL_CASH_TO_THE_PLAYER
from enum import Enum
from Property import Status
import copy

class Phase(Enum):
    DICE_ROLL= 0
    BSMT = 1
    TRADE_OFFER = 2
    BUY_UNOWNED_PROPERTY = 3
    AUCTION_PROPERTY = 4
    PAY_RENT_UNOWNED_PROPERTY = 5
    JAIL = 6
    CHANCE_CARD = 7
    COMMUNITY_CARD = 8

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

    def update_player_position(self, moves):
        if self.turn_id % 2 == 0:
            self.players_position = (self.players_position[0] + moves, self.players_position[1])
        else:
            self.players_position = (self.players_position, self.players_position[1]+moves)

    def move_player_to_jail(self, jail_location):
        if self.turn_id % 2 == 0:
            self.players_position = (jail_location, self.players_position[1])
        else:
            self.players_position = (self.players_position[0], jail_location)

    def update_turn_id(self, turn_id):
        self.turn_id = turn_id

    def get_game_state(self, ):
        return copy.deepcopy(self)

    def addCash(self, cash):
        if self.turn_id % 2==0:
            self.players_cash = (self.players_cash[0] + cash, self.players_cash[1])
        else:
            self.players_cash = (self.players_cash[0], self.players_cash[1] + cash)

    def deductCash(self, cash):
        if self.turn_id % 2==0:
            self.players_cash = (self.players_cash[0] - cash, self.players_cash[1])
        else:
            self.players_cash = (self.players_cash[0], self.players_cash[1] - cash)

    def updateBoughtProperty(self, p):
        self.deductCash(p.price)
        if self.turn_id %2 ==0:
            self.property_status[p.id] = Status.OWNED_P1_NO_HOUSES
        else:
            self.property_status[p.id] = Status.OWNED_P2_NO_HOUSES
        self.phase= Phase.BUY_UNOWNED_PROPERTY


    def updateMortgagedProperty(self, p):
        if self.turn_id % 2 == 0:
            self.property_status[p.id] = Status.OWNED_P1_MORTGAGED
        else:
            self.property_status[p.id] = Status.OWNED_P2_MORTGAGED
        self.addCash(p.price)

    def updateBuiltHouse(self, p):
        num = self.property_status[p.id]
        if abs(num) >= 6:
            # Property is mortgaged or there is a hotel, cannot build
            return False
        if self.turn_id %2 == 0:
            self.property_status[p.id] = Status(num + 1)
        else:
            self.property_status[p.id] = Status(num - 1)
        self.deductCash(p.build_cost)
        return True

    def updateBuiltHotel(self, p):
        num = self.property_status[p.id]
        if abs(num) != 5:
            # Less than four houses or mortgaged, cannot build
            return False
        if self.turn_id %2 == 0:
            self.property_status[p.id] = Status.OWNED_P1_HOTEL
        else:
            self.property_status[p.id] = Status.OWNED_P2_HOTEL
        self.deductCash(p.build_cost)
        return True

    # encountered double value thrice
    def penalize_player(self):
        self.skip_player_turn = True

    def is_allowed_to_play(self):
        if self.skip_player_turn is True:
            self.skip_player_turn = False
            return False
        return True
