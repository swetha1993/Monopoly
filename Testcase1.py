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
        pass
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


def testPayRent(adjudicator):
    p1 = Player1(0)
    p2 = Player2(1)
    dice = [(1, 2), (1, 2)]

    winner, state = adjudicator.run_game(p1, p2, dice, [], [])
    state = adjudicator.game_state
    if state.players_cash[0] != INITIAL_CASH_TO_THE_PLAYER - 60 + 4:
    	return False

    if state.players_cash[1] == INITIAL_CASH_TO_THE_PLAYER -  4:
    	return True;
    	
    return False  


def testCommunityChestCard(adjudicator):
    p1 = Player1(0)
    p2 = Player2(1)
    dice = [(1,1)]
    winner, state = adjudicator.run_game(p1, p2, dice, [], [6])

    state = adjudicator.game_state
    if state.players_cash[0] != INITIAL_CASH_TO_THE_PLAYER  + 50:
        return False;

    if state.players_cash[1] == INITIAL_CASH_TO_THE_PLAYER - 50:
        return True;
    print(state.players_cash)
    return False


def testIncomeTax(adjudicator):
    p1 =  Player1(0)
    p2 =  Player2(1)
    dice = [(1, 1)]

    winner, state = adjudicator.run_game(p1, p2, dice, [], [])
    state = adjudicator.game_state
    if state.players_cash[0] == INITIAL_CASH_TO_THE_PLAYER - 200:
    	return True;
    	
    return False  
	
tests = [
	testIncomeTax,
	testPayRent,
    testCommunityChestCard
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
