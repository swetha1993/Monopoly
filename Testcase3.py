import Board
from Constants import *
from GameState import GameState, Phase
from Adjudicator import Adjudicator


class Player1(object):
    def __init__(self, id=0):
        self.id = id  # Player 1 -> id=1, Player 2 ->id=2

    def getBMSTDecision(self, state):
        pass

    def respondTrade(self, state):
        pass

    def buyProperty(self, state):
        pass

    def auctionProperty(self, state):
        return 20

    def jailDecision(self, state):
        pass

    def receiveState(self, state):
        pass

    def respondMortgage(self, state):
        pass


class Player2(object):
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
        pass

    def receiveState(self, state):
        pass

    def respondMortgage(self, state):
        pass



def testAuctionAndReportWinner(adjudicator):
    p1 = Player1(0)
    p2 = Player2(1)
    dice = [(3, 3)]

    winner, state = adjudicator.run_game(p1, p2, dice, [], [])
    state = adjudicator.game_state
    print(state.players_cash)
    if state.players_cash[0] != INITIAL_CASH_TO_THE_PLAYER:
        return False

    if state.players_cash[1] == INITIAL_CASH_TO_THE_PLAYER - 30:
        return True

    return False


tests = [
    testAuctionAndReportWinner
]


def runTests():
    adjudicator = Adjudicator()
    allPassed = True
    for test in tests:
        result = test(adjudicator)
    if not result:
        print(test.__name__ + " failed!")
        allPassed = False
    if allPassed: print("All tests passed!")


runTests()
