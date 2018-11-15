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
        return "C"

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



def testCommunityChestCard(adjudicator):
    p1 = Player1(0)
    p2 = Player2(1)
    dice = [(1, 1)]
    winner, state = adjudicator.run_game(p1, p2, dice, [], [9])

    state = adjudicator.game_state
    if state.players_cash[0] != INITIAL_CASH_TO_THE_PLAYER + 100:
        return False;

    if state.players_cash[1] == INITIAL_CASH_TO_THE_PLAYER:
        return True;

    return False


def testChangePositionOnAChanceCard(adjudicator):
    p1 = Player1(0)
    p2 = Player2(1)
    dice = [(3, 4)]
    #Advance to Boardwalk
    winner, state = adjudicator.run_game(p1, p2, dice, [13], [])

    state = adjudicator.game_state
    if state.players_cash[0] != INITIAL_CASH_TO_THE_PLAYER:
        return False

    if state.players_position[0] == 40:
        return True

    return False



def testCollectMoneyOnAChanceCard(adjudicator):
    p1 = Player1(0)
    p2 = Player2(1)
    dice = [(3, 4)]
    # Advance to St. Charles Place. If you pass Go, collect $200
    winner, state = adjudicator.run_game(p1, p2, dice, [0], [])

    state = adjudicator.game_state
    if state.players_cash[0] != INITIAL_CASH_TO_THE_PLAYER + 200:
        return False

    return True


def testFreeJailExitUsingJailFreeCard(adjudicator):
    p1 = Player1(0)
    p2 = Player2(1)
    dice = [(1, 1),
            (2, 3)]
    # 4 - Get out of jail free, this card may be kept until needed
    # 9 - Go to Jail. Go directly to Jail. Do not pass GO, do not collect $200
    winner, state = adjudicator.run_game(p1, p2, dice, [9], [4])

    state = adjudicator.game_state
    if state.players_cash[0] != INITIAL_CASH_TO_THE_PLAYER :
        return False;

    # PLayer is sent back to GO when he uses Jail free card
    if state.players_position[0] == 0:
        return True

    return False



def testPlayerShouldExitJailOnThrowingDouble(adjudicator):
    p1 = Player1(0)
    p2 = Player2(1)
    dice = [(3, 4), (1,2),
            (2, 2)]

    # 9 - Go to Jail. Go directly to Jail. Do not pass GO, do not collect $200
    winner, state = adjudicator.run_game(p1, p2, dice, [9], [])
    state = adjudicator.game_state

    # current position = -1(jail) + (2+2) = 3
    if state.players_position[0] == 3:
        return True

    return False


def testPlayerInJailShouldNotCollect200WhenPassingThroughGO(adjudicator):
    p1 = Player1(0)
    p2 = Player2(1)
    dice = [(3, 4), (1, 2),
            (2, 2)]

    # 9 - Go to Jail. Go directly to Jail. Do not pass GO, do not collect $200
    winner, state = adjudicator.run_game(p1, p2, dice, [9], [])
    state = adjudicator.game_state

    # current position = -1(jail) + (2+2) = 3
    if state.players_position[0] != 3:
        return False

    if state.players_cash[0] != INITIAL_CASH_TO_THE_PLAYER - 4:
        return False

    if state.players_cash[1] != INITIAL_CASH_TO_THE_PLAYER - 26:
        return False

    return True



tests = [
    testAuctionAndReportWinner,
    testCommunityChestCard,
    testChangePositionOnAChanceCard,
    testCollectMoneyOnAChanceCard,
    testFreeJailExitUsingJailFreeCard,
    testPlayerShouldExitJailOnThrowingDouble,
    testPlayerInJailShouldNotCollect200WhenPassingThroughGO
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
