import Board
from Constants import *
from GameState import GameState, Phase
from Adjudicator import Adjudicator

class Player3(object):
    def __init__(self, id=0):
        self.id = id  # Player 1 -> id=1, Player 2 ->id=2

    def getBMSTDecision(self, state):
        pass

    def respondTrade(self, state):
        pass

    def buyProperty(self, state):
        pass

    def auctionProperty(self, state):
        return 30

    def jailDecision(self, state):
        return "R"

    def receiveState(self, state):
        pass

    def respondMortgage(self, state):
        pass


class Player4(object):
    def __init__(self, id=0):
        self.id = id  # Player 1 -> id=1, Player 2 ->id=2

    def getBMSTDecision(self, state):
        pass

    def respondTrade(self, state):
        pass

    def buyProperty(self, state):
        pass

    def auctionProperty(self, state):
        return 40

    def jailDecision(self, state):
        pass

    def receiveState(self, state):
        pass

    def respondMortgage(self, state):
        pass



def testBankPaysDividendChanceCard(adjudicator):
    p1 = Player3(0)
    p2 = Player4(1)
    dice = [(6, 1)]

    # Player1 Lands on a Chance card in which bank pays divided, so player1 cash gets increased
    winner, state = adjudicator.run_game(p1, p2, dice, [6], [])
    state = adjudicator.game_state

    if state.players_position[0] != 7:
        return False

    if state.players_cash[0] != INITIAL_CASH_TO_THE_PLAYER + 50:
        return False

    return True


def testPlayerTwoWinsAuction(adjudicator):
    p1 = Player3(0)
    p2 = Player4(1)
    dice = [(5, 1)]

    # Player1 lands at "Oriental Avenue" decided to go for auction instead of buying it
    # player2 wins the auction, player2 cash gets deducted, player1 cash remains same
    winner, state = adjudicator.run_game(p1, p2, dice, [6], [])
    state = adjudicator.game_state
    if state.players_position[0] != 6:
        return False

    if state.players_cash[1] != INITIAL_CASH_TO_THE_PLAYER - 40:
        return False

    if state.players_cash[0] != INITIAL_CASH_TO_THE_PLAYER:
        return False

    return True

def testPlayerOnePaysPoorTax(adjudicator):
    p1 = Player3(0)
    p2 = Player4(1)
    dice = [(2, 5)]

    # Player1 lands at Chance card
    # Chest card action says to pay poor tax of 15$, Player1 Cash reduces by 15$
    winner, state = adjudicator.run_game(p1, p2, dice, [11], [])
    state = adjudicator.game_state
    if state.players_position[0] != 7:
        return False

    if state.players_cash[0] != INITIAL_CASH_TO_THE_PLAYER - 15:
        return False

    if state.players_cash[1] != INITIAL_CASH_TO_THE_PLAYER:
        return False

    return True

def testPlayerTwoHasMoreMoneyThanInitialCash(adjudicator):
    p1 = Player3(0)
    p2 = Player4(1)
    dice = [(2, 3),(1,1)]

    # Player1 Lands on Property Rail Road Decides not to buy
    # Goes for Auction, Player2 Wins Bid
    # Player2 lands at Community chest card
    # The Community Chest Card Action Says to Collect 200$ from Bank
    # Player 2 has more money than initial cash
    winner, state = adjudicator.run_game(p1, p2, dice, [], [1])
    state = adjudicator.game_state

    print(state.players_position)
    print(state.players_cash)
    if state.players_position[0] != 5:
        return False

    if state.players_position[1] != 2:
        return False

    if state.players_cash[0] != INITIAL_CASH_TO_THE_PLAYER:
        return False

    if state.players_cash[1] != INITIAL_CASH_TO_THE_PLAYER + 160:
        return False

    return True

tests = [
    testBankPaysDividendChanceCard,
    testPlayerTwoWinsAuction,
    testPlayerOnePaysPoorTax,
    testPlayerTwoHasMoreMoneyThanInitialCash
]


def runTests():
    allPassed = True
    for test in tests:
        adjudicator = Adjudicator()
        result = test(adjudicator)
        if not result:
            print(test.__name__ + " failed!")
            allPassed = False
    if allPassed: print("All tests passed!")


runTests()
