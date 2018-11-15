import Board
import Constants
from GameState import GameState, Phase
import Utility
import Player
from Property import Status
from Constants import DOUBLES_COUNT

class Adjudicator:

    def __init__(self):
        self.turn_limit = Constants.TURN_LIMIT
        self.player_count = Constants.PLAYER_COUNT
        self.player_instances = []
        self.game_state = None
        self.board_instance = Board.Board()

    def runPlayerOnState(self, player, state):

        # Fetch player position
        player_id = state.turn_id % 2
        position = state.players_position[player_id]

        if self.board_instance.board_dict[position].name == Constants.COMMUNITY_CHEST:
            self.communityChestAction(state, player_id)

        elif position == Constants.JAIL_LOCATION:  # Check if player is in jail
            jail_decision = player.jailDecision(state)
            if jail_decision == "R":
                pass
            elif jail_decision == "C":
                pass
            elif jail_decision == "P":
                pass

        elif position == Constants.VISITING_JAIL_LOCATION:
            #no action
            return

        elif state.property_status[position] == Status.UNOWNED:
            if player.buyProperty(state):
                state.updateBoughtProperty(self.board_instance.board_dict[position])
            else:
                self.auction(state)

        elif state.property_status[position] != Status.UNOWNED:
            # Owned property

            if player_id == 0:
                if state.property_status[position] < 0:
                    # Owned by p2 and p1 landed on it
                    rent_amt = self.board_instance.get_rent(position)
                    state.phase = Phase.PAY_RENT_UNOWNED_PROPERTY

                    if state.checkCash(rent_amt, self.player_instances[player_id]):
                        state.deductCash(rent_amt, player_id)
                        state.addCash(rent_amt, (player_id + 1) % 2)
                        # TODO: additional info source, cash
                    else:
                        # TODO: Phase = BSMT (Mortgage or lose)
                        pass
                else:
                    #TODO: Phase = BSMT & additional info
                    pass
            else:
                if state.property_status[position] > 0:
                    # Owned by p1 and p2 landed on it
                    rent_amt = self.board_instance.get_rent(position)
                    state.phase = Phase.PAY_RENT_UNOWNED_PROPERTY

                    if state.checkCash(rent_amt, self.player_instances[player_id]):
                        state.deductCash(rent_amt, player_id)
                        state.addCash(rent_amt, (player_id + 1) % 2)
                        # TODO: additional info source, cash
                    else:
                        # TODO: Phase = BSMT (Mortgage or lose)
                        pass
                else:
                    # TODO: Phase = BSMT & additional info
                    pass

        bmst = player.getBMSTDecision(state)

    def communityChestAction(self, state, player_id):
        card= self.board_instance.community_cards.pop(0)
        self.board_instance.community_cards.append(card)
        if card.id == 0:
            #Advance to Go (Collect $200)
            state.move_player_to_position(card.position)
            state.addCash(card.money, player_id)
        elif card.id == 1:
            #Bank error in your favor, collect $200
            state.addCash(card.money)
        elif card.id == 2:
            #Doctor's fees, Pay $50
            state.deductCash(abs(card.money), player_id)
        elif card.id == 3:
            #From sale of stock you get $50
            state.addCash(abs(card.money), player_id)
        elif card.id == 4:
            #Get out of jail free, this card may be kept until needed
            state.move_player_to_position(card.position)
        elif card.id == 5:
            #Go to jail, go directly to jail – Do not pass Go, do not collect $200
            state.move_player_to_position(card.position)
        elif card.id == 6:
            #Grand Opera Night. Collect $50 from every player for opening night seats.
            state.addCash(card.money, player_id)
        elif card.id == 7:
            #Holiday Fund matures - Receive $100
            state.addCash(card.money, player_id)
        elif card.id == 8:
            #Income Tax refund. Collect $20
            state.addCash(card.money, player_id)
        elif card.id == 9:
            #Life Insurance Matures - Collect $100
            state.addCash(card.money, player_id)
        elif card.id == 10:
            #Pay Hospital Fees of $50
            state.deductCash(abs(card.money), player_id)
        elif card.id == 11:
            #Pay School Fees of $50
            state.deductCash(abs(card.money), player_id)
        elif card.id == 12:
            #Receive $25 Consultancy Fee
            state.addCash(card.money, player_id)
        elif card.id == 13:
            #You are assessed for street repairs: Pay $40 per house and $115 per hotel you own.
            to_pay=0
            for property_status in state.property_status:
                property_status = abs(property_status)
                if abs(property_status) > 1 and property_status < 6 :
                    to_pay += abs(card.money) * (property_status-1)
                elif property_status == 6:
                    to_pay += abs(card.money2)
            state.deductCash(to_pay, player_id)
        elif card.id == 14:
            #You have won second prize in a beauty contest– collect $10
            state.addCash(card.money, player_id)
        elif card.id == 15:
            #You inherit $100
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

    def broad_cast_state(self, player1, player2, state):
        pass

    def get_current_player(self, turn_id):
        player_id = turn_id % self.player_count
        return self.player_instances[player_id]

    def run_game(self, player1, player2, dice_rolls=None, chance_cards=None, community_chest_cards=None):
        self.player_instances = [player1, player2]
        self.game_state = GameState()
        turn_id = self.game_state.turn_id
        while turn_id < self.turn_limit:
            self.game_state.past_states.append(self.game_state)
            sub_turn_id = 0
            current_player = self.get_current_player(turn_id)
            while True:
                dice = None
                if dice_rolls is not None:
                    dice = Utility.Dice(dice_rolls[turn_id][0], dice_rolls[turn_id][1])
                else:
                    dice = Utility.Dice()
                    dice.perform_roll()

                new_game_state = self.game_state.get_game_state()

                if dice.is_double():
                    new_game_state.additional_info[DOUBLES_COUNT][turn_id % 2] += 1
                else:
                    new_game_state.additional_info[DOUBLES_COUNT][turn_id % 2] = 0

                self.game_state.update_turn_id(turn_id)
                if new_game_state.additional_info[DOUBLES_COUNT][turn_id % 2] == 3:
                    new_game_state.additional_info[DOUBLES_COUNT][turn_id % 2] = 0
                    new_game_state.move_player_to_position(Constants.JAIL_LOCATION)
                else:
                    # Updating position of player
                    new_game_state.update_player_position(dice.get_dice_roll1() + dice.get_dice_roll2())

                self.runPlayerOnState(current_player, new_game_state)

                self.game_state = new_game_state
                if current_player.doubles_count == 0:
                    break
                sub_turn_id += 1

            print(turn_id, current_player.get_id(), dice.get_dice_roll1(), dice.get_dice_roll2(),
                  current_player.doubles_count)
            turn_id += 1
        return 1,2	# Needs to be changed to winner, gamestate

    def complete_player_move(self):
        pass


if __name__ == '__main__':
    player_one = Player.Player(0)
    player_two = Player.Player(1)
    Adjudicator().run_game(player_one, player_two)
