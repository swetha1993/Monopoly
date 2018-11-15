import Board
from GameState import GameState, Phase
import Utility
import Player
from Property import Status
import bisect
from Constants import *


class Adjudicator:
    def __init__(self):
        self.turn_limit = TURN_LIMIT
        self.player_count = PLAYER_COUNT
        self.player_instances = []
        self.game_state = None
        self.dice_index = 0
        self.dice_rolls = None
        self.board_instance = Board.Board()
        self.community_chest_cards = None
        self.chance_cards = None

    @staticmethod
    def get_nearest_railroad(current_position):
        index = bisect.bisect_right(RAIL_ROAD_LOCATIONS, current_position)
        if index == len(RAIL_ROAD_LOCATIONS):
            index = 0
        next_position = RAIL_ROAD_LOCATIONS[index]
        return next_position

    @staticmethod
    def get_nearest_utility(current_position):
        index = bisect.bisect_right(UTILITY_LOCATIONS, current_position)
        if index == len(UTILITY_LOCATIONS):
            index = 0
        next_position = UTILITY_LOCATIONS[index]
        return next_position

    def perform_chance_card_action(self, chance_card, state):
        next_position = chance_card.position
        id = chance_card.id
        player_id = state.turn_id % 2
        current_position = state.get_player_position()
        bsmt_required = False
        rent_amt = None
        if id == 0:
            state.move_player_to_position(next_position)
            state.addCash(chance_card.money, player_id)
        elif id == 1:
            if current_position > CHANCE_LOCATIONS[1]:
                state.addCash(chance_card.money, player_id)
            state.move_player_to_position(next_position)
        elif id == 2:
            if current_position > CHANCE_LOCATIONS[0]:
                state.addCash(chance_card.money, player_id)
            state.move_player_to_position(next_position)
        elif id == 3:
            next_position = self.get_nearest_utility(current_position)
            state.move_player_to_position(next_position)
            dice = Utility.Dice()
            dice.perform_roll()
            dice_value = dice.get_dice_roll1() + dice.get_dice_roll2()
            rent_amt = 10 * dice_value
        elif id in [4, 5]:
            next_position = self.get_nearest_railroad(current_position)
            state.move_player_to_position(next_position)
            bsmt_required = True
            rent_factor = 2
            rent_amt = rent_factor * self.board_instance.get_rent(next_position)
            state.move_player_to_position(next_position)
        elif id == 6:
            state.addCash(chance_card.money, player_id)
        elif id == 7:
            state.update_jail_free_card(True)
        elif id == 8:
            next_position = current_position - 3
            state.move_player_to_position(next_position)
        elif id == 9:
            state.move_player_to_position(next_position)
        elif id == 10:
            to_pay = 0
            for property_status in state.property_status:
                property_status = abs(property_status)
                if abs(property_status) > 1 and property_status < 6:
                    to_pay += abs(chance_card.money) * (property_status - 1)
                elif property_status == 6:
                    to_pay += abs(chance_card.money2)
            state.deductCash(to_pay, player_id)
        elif id == 11:
            state.deductCash(chance_card.money, player_id)
        elif id == 12:
            # TODO: pending bsmt required ?
            state.move_player_to_position(next_position)
        elif id == 13:
            # TODO: pending bsmt required ?
            state.move_player_to_position(next_position)
        elif id == 14:
            next_player_id = (player_id + 1) % 2
            state.addCash(chance_card.money, next_player_id)
            state.deductCash(chance_card.money, player_id)
        elif id == 15:
            state.addCash(chance_card.money, player_id)
        return bsmt_required, rent_amt

    def get_chance_card(self):
        chance_index = self.chance_cards[0]
        del self.chance_cards[0]
        self.chance_cards.append(chance_index)
        return self.board_instance.chance_cards[chance_index]

    def perform_bsmt_action(self, bsmtaction, state):
        action = bsmtaction[0]

        if action == "B":
            self.handle_buy(bsmtaction, state)
        elif action == "S":
            self.handle_sell(bsmtaction, state)
        elif action == "M":
            self.handle_mortgage(bsmtaction, state)
        elif action == "T":
            self.handle_trade(bsmtaction, state)

    def can_trade(self, bsmtaction, state):
        current_player_id = state.turn_id % 2
        other_player = (current_player_id + 1) % 2

        cashoffer, propoffer, cashreq, propreq = bsmtaction[1]
        if state.players_cash[current_player_id] < cashoffer:
            return False
        elif state.players_cash[other_player] < cashreq:
            return False

        for pid in propoffer:
            property_obj = self.board_instance.board_dict[pid]
            if property_obj.owner != current_player_id:
                return False

        for pid in propreq:
            property_obj = self.board_instance.board_dict[pid]
            if property_obj.owner != other_player:
                return False

        return True

    def handle_trade(self, bsmtaction, state):
        current_player_id = state.turn_id % 2
        cur_player_obj = self.player_instances[current_player_id]
        cashoffer, propoffer, cashreq, propreq = bsmtaction[1]
        if self.can_trade(bsmtaction, state):
            is_accepted = cur_player_obj.respondTrade(state)
            if not is_accepted:
                return
            state.players_cash[current_player_id] += cashreq - cashoffer
            state.players_cash[(current_player_id + 1) % 2] += cashoffer - cashreq
            for pid in propoffer:
                state.property_status[pid] *= -1
            for pid in propreq:
                state.property_status[pid] *= -1

    def can_mortgage(self, property_obj, current_player_id):
        if property_obj.owner != current_player_id:
            return False
        if abs(property_obj.status) == Status.OWNED_P1_MORTGAGED.value:
            return False
        return True

    def handle_mortgage(self, bsmtaction, state):
        current_player_id = state.turn_id % 2
        for id in bsmtaction[1]:
            property_obj = self.board_instance.board_dict[id]
            if self.can_mortgage(property_obj, current_player_id):
                # TODO: Handle houses
                state.players_cash[current_player_id] += int(self.board_instance.board_dict[id].price / 2)
                property_obj.status = Status.OWNED_P1_MORTGAGED.value if not \
                    current_player_id else Status.OWNED_P2_MORTGAGED.value

    def can_buy(self, id, numhouses, player_id):
        # TODO: Check group and color properties
        property_obj = self.board_instance.board_dict[id]
        req_houses = numhouses + abs(property_obj.status.value) - 1
        if property_obj.owner != player_id:
            return False
        if req_houses < 0 or req_houses > 5:
            return False
        if abs(property_obj.status) in [Status.OWNED_P1_MORTGAGED.value, Status.OWNED_P1_NO_HOUSES.value]:
            return False
        return True

    def handle_buy(self, bsmtaction, state):
        current_player_id = state.turn_id % 2
        player_debt = state.debt[current_player_id]
        player_cash = state.players_cash[current_player_id] - player_debt

        cost = 0
        for id, prop in bsmtaction[1]:
            if self.can_buy(id, prop, current_player_id):
                cost += prop * int(self.board_instance.board_dict[id].build_cost / 2)

        if cost < player_cash:
            return

        for id, prop in bsmtaction[1]:
            if current_player_id == 0:
                state.property_status[id] += prop
            else:
                state.property_status[id] -= prop
            state.deductCash(self.board_instance.board_dict[id].build_cost * prop, current_player_id)

    def can_sell(self, id, numhouses, player_id):
        property_obj = self.board_instance.board_dict[id]
        if property_obj.owner != player_id:
            return False
        if numhouses < 0 or numhouses > 5:
            return False
        if abs(property_obj.status) in [Status.OWNED_P1_MORTGAGED.value, Status.OWNED_P1_NO_HOUSES.value]:
            return False
        if numhouses > abs(property_obj.status) - 1:
            return False
        return True

    def handle_sell(self, bsmtaction, state):
        current_player_id = state.turn_id % 2
        player_debt = state.debt[current_player_id]

        cost = 0
        for id, prop in bsmtaction[1]:
            if self.can_sell(id, prop, current_player_id):
                cost = cost + prop * int(self.board_instance.board_dict[id].build_cost / 2)
        cost = cost - player_debt
        state.players_cash[current_player_id] += cost

    def runPlayerOnState(self, player, state):
        # Fetch player position
        player_id = state.turn_id % 2
        position = state.players_position[player_id]
        _rent_amt = None
        if position in COMMUNITY_CHEST_LOCATIONS:
            self.communityChestAction(state, player_id)
            return
        elif position in CHANCE_LOCATIONS:
            if len(self.chance_cards) ==0:
                return
            chance_card = self.get_chance_card()
            bsmt_action, _rent_amt = state.perform_chance_card_action(chance_card, state)
            if bsmt_action is False:
                return
        if position in TAX_LOCATIONS:
            tax = self.board_instance.board_dict[position].tax
            if state.checkCash(tax, player_id):
                state.deductCash(tax, player_id)
            else:
                # TODO: Phase = BSMT (Mortgage or lose)
                pass

        elif position == JAIL_LOCATION:  # Check if player is in jail
            jail_decision = player.jailDecision(state)
            if jail_decision == "R":
                limit = max(self.turn_limit, self.dice_index + 3, len(self.dice_rolls))
                while self.dice_index < limit:
                    dice = Utility.Dice(self.dice_rolls[self.dice_index][0], self.dice_rolls[self.dice_index][1])
                    if self.dice_rolls[self.dice_index][0] == self.dice_rolls[self.dice_index][1]:
                        #TODO: Phase = BSMT (Mortgage or lose)
                        pass
                    self.dice_index += 1
            elif jail_decision == "C":
                if state.additional_info[JAIL_FREE_CARD][player_id]:
                    state.additional_info[JAIL_FREE_CARD][player_id] = False
                    state.move_player_to_position(0)
            elif jail_decision == "P":
                if state.checkCash(50, player_id):
                    state.deductCash(50, player_id)
                    state.move_player_to_position(0)
                else:
                    # TODO: phase = BSMT (Mortgage or lose)
                    pass

        # no action to be taken
        elif position == VISITING_JAIL_LOCATION:
            return None, state

        # Unowned property
        elif state.property_status[position] == Status.UNOWNED.value:
            # check buy property decision from player
            if player.buyProperty(state):
                state.updateBoughtProperty(self.board_instance.board_dict[position])
            # Start auction
            elif player.auctionProperty(state):
                self.auction(state)

        # Owned property
        elif state.property_status[position] != Status.UNOWNED.value:
            # First Player
            if player_id == 0:
                # Owned by p2 and p1 landed on it
                if state.property_status[position] < 0:
                    # Get rent amt
                    if _rent_amt is not None:
                        rent_amt = _rent_amt
                    else:
                        rent_amt = self.board_instance.get_rent(position)

                    # Go for BSMT
                    state.phase = Phase.BSMT
                    state.debt[player_id] += rent_amt
                    bsmt_action = player.getBMSTDecision(state)

                    # If BSMT action is None
                    if not bsmt_action:
                        # Pay rent using player cash
                        if state.checkCash(rent_amt, self.player_instances[player_id]):
                            state.deductCash(rent_amt, player_id)
                            state.addCash(rent_amt, (player_id + 1) % 2)
                            # TODO: additional info source, cash
                        else:
                            # Declare winner!!
                            return self.player_instances[(player_id + 1) % 2], state
                    else:
                        # Execute BSMT action according to player
                        self.perform_bsmt_action(bsmt_action, state)
                        # Pay rent using player cash
                        if state.checkCash(rent_amt, self.player_instances[player_id]):
                            state.deductCash(rent_amt, player_id)
                            state.addCash(rent_amt, (player_id + 1) % 2)
                        else:
                            # Declare winner!!
                            return self.player_instances[(player_id + 1) % 2], state
                else:
                    # Owned by p1 and p1 landed on it
                    # Go for BSMT
                    state.phase = Phase.BSMT
                    bsmt_action = player.getBMSTDecision(state)
                    self.perform_bsmt_action(bsmt_action, state)
            # Second player
            else:
                # Owned by p1 and p2 landed on it
                if state.property_status[position] > 0:
                    # Get rent amt
                    if _rent_amt is not None:
                        rent_amt = _rent_amt
                    else:
                        rent_amt = self.board_instance.get_rent(position)

                    # Go for BSMT
                    state.phase = Phase.BSMT
                    state.debt[player_id] += rent_amt
                    bsmt_action = player.getBMSTDecision(state)

                    # If BSMT action is None
                    if not bsmt_action:
                        # Pay rent using player cash
                        if state.checkCash(rent_amt, self.player_instances[player_id]):
                            state.deductCash(rent_amt, player_id)
                            state.addCash(rent_amt, (player_id + 1) % 2)
                            # TODO: additional info source, cash
                        else:
                            # Declare winner!!
                            return self.player_instances[(player_id + 1) % 2], state
                    else:
                        # Execute BSMT action according to player
                        self.perform_bsmt_action(bsmt_action, state)
                        # Pay rent using player cash
                        if state.checkCash(rent_amt, self.player_instances[player_id]):
                            state.deductCash(rent_amt, player_id)
                            state.addCash(rent_amt, (player_id + 1) % 2)
                        else:
                            # Declare winner!!
                            return self.player_instances[(player_id + 1) % 2], state
                else:
                    # Owned by p2 and p2 landed on it
                    # Go for BSMT
                    state.phase = Phase.BSMT
                    bsmt_action = player.getBMSTDecision(state)
                    self.perform_bsmt_action(bsmt_action, state)

    def communityChestAction(self, state, player_id):
        if len(self.community_chest_cards) == 0:
            return
        id = self.community_chest_cards.pop(0)
        self.community_chest_cards.append(id)
        card = self.board_instance.community_cards[id]
        if card.id == 0:
            # Advance to Go (Collect $200)
            state.move_player_to_position(card.position)
            state.addCash(card.money, player_id)
        elif card.id == 1:
            # Bank error in your favor, collect $200
            state.addCash(card.money, player_id)
        elif card.id == 2:
            # Doctor's fees, Pay $50
            state.deductCash(abs(card.money), player_id)
        elif card.id == 3:
            # From sale of stock you get $50
            state.addCash(abs(card.money), player_id)
        elif card.id == 4:
            # Get out of jail free, this card may be kept until needed
            state.move_player_to_position(card.position)
        elif card.id == 5:
            # Go to jail, go directly to jail – Do not pass Go, do not collect $200
            state.move_player_to_position(card.position)
        elif card.id == 6:
            # Grand Opera Night. Collect $50 from every player for opening night seats.
            state.addCash(card.money, player_id)
            if player_id == 1:
                state.deductCash(card.money, 0)
            else:
                state.deductCash(card.money, 1)
        elif card.id == 7:
            # Holiday Fund matures - Receive $100
            state.addCash(card.money, player_id)
        elif card.id == 8:
            # Income Tax refund. Collect $20
            state.addCash(card.money, player_id)
        elif card.id == 9:
            # Life Insurance Matures - Collect $100
            state.addCash(card.money, player_id)
        elif card.id == 10:
            # Pay Hospital Fees of $50
            state.deductCash(abs(card.money), player_id)
        elif card.id == 11:
            # Pay School Fees of $50
            state.deductCash(abs(card.money), player_id)
        elif card.id == 12:
            # Receive $25 Consultancy Fee
            state.addCash(card.money, player_id)
        elif card.id == 13:
            # You are assessed for street repairs: Pay $40 per house and $115 per hotel you own.
            to_pay = 0
            for property_status in state.property_status:
                property_status = abs(property_status)
                if abs(property_status) > 1 and property_status < 6:
                    to_pay += abs(card.money) * (property_status - 1)
                elif property_status == 6:
                    to_pay += abs(card.money2)
            state.deductCash(to_pay, player_id)
        elif card.id == 14:
            # You have won second prize in a beauty contest– collect $10
            state.addCash(card.money, player_id)
        elif card.id == 15:
            # You inherit $100
            state.addCash(card.money, player_id)

    def auction(self, state):
        cur_player = self.player_instances[state.turn_id % 2]
        opponent = self.player_instances[(state.turn_id + 1) % 2]

        # Fetch player position
        prop_id = state.players_position[state.turn_id % 2]
        # add as additional prop_id
        state.additional_info.update({'property_id': prop_id})

        # TODO: Handle timeouts
        cur_bid = cur_player.auctionProperty(state)
        opp_bid = opponent.auctionProperty(state)

        if cur_bid > opp_bid:
            state.assign_property(cur_player, prop_id, cur_bid)
        else:
            state.assign_property(opponent, prop_id, opp_bid)

    def get_current_player(self, turn_id):
        player_id = turn_id % self.player_count
        return self.player_instances[player_id]

    def run_game(self, player1, player2, dice_rolls=None,
                 chance_cards=None, community_chest_cards=None):
        self.player_instances = [player1, player2]
        self.game_state = GameState()
        turn_id = self.game_state.turn_id
        self.chance_cards = chance_cards
        self.dice_rolls = dice_rolls
        self.community_chest_cards = community_chest_cards

        if dice_rolls is not None:
            self.turn_limit = len(dice_rolls)
        while self.dice_index < self.turn_limit:

            self.game_state.past_states.append(self.game_state)
            sub_turn_id = 0
            current_player = self.get_current_player(turn_id)
            while True:
                if dice_rolls is not None:
                    dice = Utility.Dice(dice_rolls[self.dice_index][0], dice_rolls[self.dice_index][1])
                    self.dice_index += 1
                else:
                    dice = Utility.Dice()
                    dice.perform_roll()
                new_game_state = self.game_state.get_game_state()

                if dice.is_double():
                    new_game_state.additional_info[DOUBLES_COUNT][turn_id % 2] += 1
                else:
                    new_game_state.additional_info[DOUBLES_COUNT][turn_id % 2] = 0
                new_game_state.update_turn_id(turn_id)
                if new_game_state.additional_info[DOUBLES_COUNT][turn_id % 2] == 3:
                    new_game_state.additional_info[DOUBLES_COUNT][turn_id % 2] = 0
                    new_game_state.move_player_to_position(JAIL_LOCATION)
                else:
                    # Updating position of player
                    new_game_state.update_player_position(dice.get_dice_roll1() + dice.get_dice_roll2())
                self.runPlayerOnState(current_player, new_game_state)
                print(new_game_state.players_cash, new_game_state.players_position)

                self.game_state = new_game_state
                if new_game_state.additional_info[DOUBLES_COUNT][turn_id % 2] == 0 or \
                        self.turn_limit == self.dice_index:
                    break
                sub_turn_id += 1

            turn_id += 1
        return 1, 2  # TODO: Needs to be changed to winner, gamestate

    def complete_player_move(self):
        pass


if __name__ == '__main__':
    player_one = Player.Player(0)
    player_two = Player.Player(1)
    Adjudicator().run_game(player_one, player_two)
