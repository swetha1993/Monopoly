from enum import Enum

class Status(Enum):
    UNOWNED = 0
    OWNED_P1_NO_HOUSES = 1
    OWNED_P1_1_HOUSE = 2
    OWNED_P1_2_HOUSES = 3
    OWNED_P1_3_HOUSES = 4
    OWNED_P1_4_HOUSES = 5
    OWNED_P1_HOTEL = 6
    OWNED_P1_MORTGAGED= 7
    OWNED_P2_NO_HOUSES = -1
    OWNED_P2_1_HOUSE = -2
    OWNED_P2_2_HOUSES = -3
    OWNED_P2_3_HOUSES = -4
    OWNED_P2_4_HOUSES = -5
    OWNED_P2_HOTEL = -6
    OWNED_P2_MORTGAGED = -7

class Property(object):
    def __init__(self, id, name, colour, price, status):
        self.id=id
        self.name=name
        self.colour=colour
        self.price=price
        self.status=status