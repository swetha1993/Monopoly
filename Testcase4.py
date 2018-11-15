import Board
from Constants import *
from GameState import GameState, Phase
from Adjudicator import Adjudicator


class Player1(object):
    def __init__(self, id=0):
        self.id = id  # Player 1 -> id=1, Player 2 ->id=2

    def getBMSTDecision(self, state):
        return ("M", [3])

    def respondTrade(self, state):
        pass

    def buyProperty(self, state):
        return True

    def auctionProperty(self, state):
        pass

    def jailDecision(self, state):
        pass

    def respondTrade(self, state):
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
        return True

    def auctionProperty(self, state):
        pass

    def jailDecision(self, state):
        pass

    def respondTrade(self, state):
        pass

    def receiveState(self, state):
        pass

    def respondMortgage(self, state):
        pass


class Player3(object):
    def __init__(self, id=0):
        self.id = id  # Player 1 -> id=1, Player 2 ->id=2

    def getBMSTDecision(self, state):
        pass

    def respondTrade(self, state):
        pass

    def buyProperty(self, state):
        return True

    def auctionProperty(self, state):
        pass

    def jailDecision(self, state):
        pass

    def respondTrade(self, state):
        return True

    def receiveState(self, state):
        pass

    def respondMortgage(self, state):
        pass


class Player4(object):
    def __init__(self, id=0):
        self.id = id  # Player 1 -> id=1, Player 2 ->id=2

    def getBMSTDecision(self, state):
        return (T, [200, [], 0, [property_id]])

    def respondTrade(self, state):
        pass

    def buyProperty(self, state):
        return True

    def auctionProperty(self, state):
        pass

    def jailDecision(self, state):
        pass

    def respondTrade(self, state):
        pass

    def receiveState(self, state):
        pass

    def respondMortgage(self, state):
        pass


# player1 decides to mortgage a property 3 and pay rent for property 5 of player2
def testNoMoneyMortgage(adjudicator):
    p1 = Player1(0)
    p2 = Player2(1)
    dice = [(1, 2), (3, 2), (1, 1)]
    winner, state = adjudicator.run_game(p1, p2, dice, [], [])

    state = adjudicator.game_state
    if state.players_cash[0] != INITIAL_CASH_TO_THE_PLAYER - 60 - 25 + 30:
        return False

    if state.players_cash[1] == INITIAL_CASH_TO_THE_PLAYER - 200 + 25:
        return True
    print(state.players_cash)
    return False


tests = [
    testNoMoneyMortgage
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
