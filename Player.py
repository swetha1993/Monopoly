class Player(object):
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

'''		
    def movePosition(self, moves):
        self.position += moves

    def addCash(self, cash):
        self.cash += cash

    def deductCash(self, cash):
        self.cash -= cash

    def buyProperty(self, p):
        if self.cash < p.price or p.status != Status.UNOWNED:
            return False
        self.deductCash(p.price)
        self.properties[p.id] = p

    def setTurnNo(self, turn_no):
        self.turn_no = turn_no

    def sellProperty(self, property_id):
        self.addCash(self.properties[property_id].price)
        del self.properties[property_id]

    def mortgageProperty(self, property_id):
        if self.id == 1:
            self.properties[property_id].status = Status.OWNED_P1_MORTGAGED
        else:
            self.properties[property_id].status = Status.OWNED_P2_MORTGAGED
        self.addCash(self.properties[property_id].price)

    def buildHouse(self, property_id, house_cost):
        num = self.properties[property_id].status.value
        if abs(num) >= 6:
            # Property is mortgaged or there is a hotel, cannot build
            return False
        if self.id == 1:
            self.properties[property_id].status = Status(num + 1)
        else:
            self.properties[property_id].status = Status(num - 1)
        self.deductCash(house_cost)
        return True

    def buildHotel(self, property_id, hotel_cost):
        num = self.properties[property_id].status.value
        if abs(num) != 5:
            # Less than four houses or mortgaged, cannot build
            return False
        if self.id == 1:
            self.properties[property_id].status = Status.OWNED_P1_HOTEL
        else:
            self.properties[property_id].status = Status.OWNED_P2_HOTEL
        self.deductCash(hotel_cost)
        return True

    def get_id(self):
        return self.id
		

    def get_position(self):
        return self.position

    def get_cash(self):
        return self.cash

    def get_turn_no(self):
        return self.turn_no

    # encountered double value thrice
    def penalize_player(self):
        self.skip_player_turn = True

    def is_allowed_to_play(self):
        if self.skip_player_turn is True:
            self.skip_player_turn = False
            return False
        return True
'''


