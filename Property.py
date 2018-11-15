from enum import Enum


class Status(Enum):
    UNOWNED = 0
    OWNED_P1_NO_HOUSES = 1
    OWNED_P1_1_HOUSE = 2
    OWNED_P1_2_HOUSES = 3
    OWNED_P1_3_HOUSES = 4
    OWNED_P1_4_HOUSES = 5
    OWNED_P1_HOTEL = 6
    OWNED_P1_MORTGAGED = 7
    OWNED_P2_NO_HOUSES = -1
    OWNED_P2_1_HOUSE = -2
    OWNED_P2_2_HOUSES = -3
    OWNED_P2_3_HOUSES = -4
    OWNED_P2_4_HOUSES = -5
    OWNED_P2_HOTEL = -6
    OWNED_P2_MORTGAGED = -7


class Property(object):
    def __init__(self, id, name, colour, monopoly_size,
                 price, build_cost, default_rent,
                 rent_house_1, rent_house_2, rent_house_3,
                 rent_house_4, rent_hotel, tax):
        self.name = name
        self.id = id
        self.colour = colour
        self.monopoly_size = monopoly_size
        self.price = price
        self.build_cost = build_cost
        self.default_rent = default_rent
        self.rent = default_rent
        self.rent_house_1 = rent_house_1
        self.rent_house_2 = rent_house_2
        self.rent_house_3 = rent_house_3
        self.rent_house_4 = rent_house_4
        self.rent_hotel = rent_hotel
        self.tax = tax
