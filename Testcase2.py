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
        return True

    def auctionProperty(self, state):
        pass

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
        return True

    def auctionProperty(self, state):
        pass

    def jailDecision(self, state):
        pass

    def receiveState(self, state):
        pass

    def respondMortgage(self, state):
        pass



class Player3(Player1):
    def __init__(self, id=0):
        super().__init__(id)

    def buyProperty(self, state):
        return True


class Player4(Player1):
    def __init__(self, id=0):
        super().__init__(id)

    def buyProperty(self, state):
        return False

    def auctionProperty(self, state):
        return False


def testSuccessiveDoubles(adjudicator):
    p1 = Player1(0)
    p2 = Player2(1)
    dice = [(6, 6), (6, 6),
            (6, 6), (2, 3)]

    winner, state = adjudicator.run_game(p1, p2, dice, [], [])
    state = adjudicator.game_state
    if state.players_position[0] == -1:
        return True

    return False


def testCollectSalaryOnPassingThroughGo(adjudicator):
    p1 = Player1(0)
    p2 = Player2(1)
    dice = [(6, 6), (1, 2),
            (6, 6), (1, 2),
            (6, 4), (1, 2),
            (3, 4)]

    winner, state = adjudicator.run_game(p1, p2, dice, [], [])
    state = adjudicator.game_state
    if state.players_cash[0] != INITIAL_CASH_TO_THE_PLAYER + 200:
        return False

    return True


def testPlayerBankruptcy(adjudicator):
    p3 = Player3(3)
    p4 = Player4(4)
    dice = [(2, 3),(1, 2),
            (6, 4),(1, 2),
            (3, 1),(1, 2),
            (2, 4), (2, 3),
            (6,4)]

    winner, state = adjudicator.run_game(p3, p4, dice, [], [])
    state = adjudicator.game_state
    if state.players_cash[0] == 0:
        return True

    return False


tests = [
    # testSuccessiveDoubles,
    # testCollectSalaryOnPassingThroughGo,
    testPlayerBankruptcy
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
