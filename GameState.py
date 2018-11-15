from Constants import *
import Constants
from enum import Enum
from Property import Status
import copy
import numpy as np


class Phase(Enum):
    DICE_ROLL = 0
    BSMT = 1
    TRADE_OFFER = 2
    BUY_UNOWNED_PROPERTY = 3
    AUCTION_PROPERTY = 4
    PAY_RENT_UNOWNED_PROPERTY = 5
    JAIL = 6
    CHANCE_CARD = 7
    COMMUNITY_CARD = 8


class GameState:
    def __init__(self, turn_id=0, property_status= np.zeros(42, dtype=int), players_position=(0,0),
                 players_cash=(INITIAL_CASH_TO_THE_PLAYER, INITIAL_CASH_TO_THE_PLAYER),
                 phase=Phase.DICE_ROLL, additional_info={}, debt=(0, 0), past_states=[]):
        self.turn_id = turn_id
        self.property_status = property_status
        self.players_position = players_position
        self.players_cash = players_cash
        self.phase = phase
        self.additional_info = additional_info
        self.additional_info[DOUBLES_COUNT] = {0: 0, 1: 0}
        self.additional_info[JAIL_FREE_CARD] = {0: False, 1: False}
        self.debt = debt
        self.past_states = past_states

    def update_jail_free_card(self, status):
        if self.turn_id % 2 == 0:
            self.additional_info[JAIL_FREE_CARD][0] = status
        else:
            self.additional_info[JAIL_FREE_CARD][1] = status

    def update_player_position(self, moves):
        player_id = self.turn_id % 2
        new_position = self.players_position[player_id] + moves
        if new_position > 39:
            self.addCash(200, player_id)
            new_position = new_position % 39
        if player_id == 0:
            self.players_position = (new_position, self.players_position[1])
        else:
            self.players_position = (self.players_position[0], new_position)

    def move_player_to_position(self, position):
        if self.turn_id % 2 == 0:
            self.players_position = (position, self.players_position[1])
        else:
            self.players_position = (self.players_position[0], position)

    def update_turn_id(self, turn_id):
        self.turn_id = turn_id

    def get_game_state(self, ):
        return copy.deepcopy(self)

    def addCash(self, cash, player_id):
        if player_id == 0:
            self.players_cash = (self.players_cash[0] + cash, self.players_cash[1])
        else:
            self.players_cash = (self.players_cash[0], self.players_cash[1] + cash)

    def deductCash(self, cash, player_id):
        if player_id == 0:
            self.players_cash = (self.players_cash[0] - cash, self.players_cash[1])
        else:
            self.players_cash = (self.players_cash[0], self.players_cash[1] - cash)

    def updateBoughtProperty(self, p):
        player_id = self.turn_id % 2
        self.deductCash(p.price, player_id)
        if player_id == 0:
            self.property_status[p.id] = Status.OWNED_P1_NO_HOUSES.value
        else:
            self.property_status[p.id] = Status.OWNED_P2_NO_HOUSES.value
        self.phase = Phase.BUY_UNOWNED_PROPERTY.value

    def assign_property(self, player_id, prop_id, bid_amt):
        # Assigning the property with prop_id to player_id in given state
        if player_id == 0:
            self.property_status[prop_id] = Status.OWNED_P1_NO_HOUSES.value
        else:
            self.property_status[prop_id] = Status.OWNED_P2_NO_HOUSES.value
        self.deductCash(bid_amt, player_id)
        self.phase = Phase.BUY_UNOWNED_PROPERTY.value

    def checkCash(self, amt_req, player_obj):
        pass

    def updateMortgagedProperty(self, p):
        player_id = self.turn_id % 2
        if player_id == 0:
            self.property_status[p.id] = Status.OWNED_P1_MORTGAGED.value
        else:
            self.property_status[p.id] = Status.OWNED_P2_MORTGAGED.value
        self.addCash(p.price, player_id)

    def updateBuiltHouse(self, p):
        num = self.property_status[p.id]
        if abs(num) >= 6:
            # Property is mortgaged or there is a hotel, cannot build
            return False
        player_id = self.turn_id % 2
        if player_id == 0:
            self.property_status[p.id] = Status(num + 1)
        else:
            self.property_status[p.id] = Status(num - 1)
        self.deductCash(p.build_cost, player_id)
        return True

    def updateBuiltHotel(self, p):
        num = self.property_status[p.id]
        if abs(num) != 5:
            # Less than four houses or mortgaged, cannot build
            return False
        player_id = self.turn_id % 2
        if player_id == 0:
            self.property_status[p.id] = Status.OWNED_P1_HOTEL.value
        else:
            self.property_status[p.id] = Status.OWNED_P2_HOTEL.value
        self.deductCash(p.build_cost, player_id)
        return True

    # encountered double value thrice
    def penalize_player(self):
        self.skip_player_turn = True

    def is_allowed_to_play(self):
        if self.skip_player_turn is True:
            self.skip_player_turn = False
            return False
        return True

    def get_player_position(self):
        pos = None
        if self.turn_id % 2 == 0:
            pos = self.players_position[0]
        else:
            pos = self.players_position[1]
        return pos

    def checkCash(self, cash, player_id):
        if player_id == 0:
            return cash >= self.players_position[0]
        else:
            return cash >= self.players_position[1]