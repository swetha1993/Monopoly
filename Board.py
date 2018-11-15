import json
import Utility
import Property
from pprint import pprint


class Board:
    def __init__(self):
        self.board_dict = dict()
        self.monopoly_groups = dict()
        self.chance_cards = []
        self.community_cards = []
        self.load_board_information()
        self.load_chance_cards()
        self.load_community_cards()

    def load_chance_cards(self):
        with open('ChanceCardsData.json') as f:
            data = json.load(f)
        chance_cards = data["chanceCards"]
        for chance_item in chance_cards:
            id = chance_item["id"]
            content = chance_item["content"]
            type = chance_item["type"]
            position = chance_item["position"]
            money = chance_item["money"]
            money2 = chance_item["money2"]
            self.chance_cards.append(Utility.ChanceCard(id, content, type, position, money, money2))
        # for card in self.chance_cards:
        #     print(card)

    def load_community_cards(self):
        with open('CommunityChestData.json') as f:
            data = json.load(f)
        community_chest_cards = data["communityChestCards"]
        for community_chest_item in community_chest_cards:
            id = community_chest_item["id"]
            content = community_chest_item["content"]
            type = community_chest_item["type"]
            position = community_chest_item["position"]
            money = community_chest_item["money"]
            money2 = community_chest_item["money2"]
            self.community_cards.append(Utility.CommunityChestCard(id, content, type, position, money, money2))
        # for card in self.community_cards:
        #     print(card)

    def load_board_information(self):
        with open('BoardData.json') as f:
            data = json.load(f)
        board_data = data["board"]
        for key in data["board"]:
            board_item = board_data[key]
            owner = None
            id = int(key)
            name = board_item["name"]
            colour = board_item["monopoly"]
            monopoly_size = board_item["monopoly_size"]
            price = board_item["price"]
            build_cost = board_item["build_cost"]
            rent = board_item["rent"]
            rent_house_1 = board_item["rent_house_1"]
            rent_house_2 = board_item["rent_house_2"]
            rent_house_3 = board_item["rent_house_3"]
            rent_house_4 = board_item["rent_house_4"]
            rent_hotel = board_item["rent_hotel"]
            tax = board_item["tax"]
            self.board_dict[id] = Property.Property(id, owner, name, colour, monopoly_size, price, build_cost, rent,
                                                     rent_house_1, rent_house_2, rent_house_3, rent_house_4,
                                                     rent_hotel, tax)
            if colour not in self.monopoly_groups:
                self.monopoly_groups[colour] = []
            self.monopoly_groups[colour].append(self.board_dict[id])

        # for key in self.board_dict:
        #     print(key, self.board_dict[key])

    def get_rent(self, position):
        return self.board_dict[position].rent

    def get_chance_card(self):
        chance_item = self.chance_cards[0]
        del self.chance_cards[0]
        self.chance_cards.append(chance_item)
        return chance_item
