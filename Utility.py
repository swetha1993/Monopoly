import random


class ChanceCard:
    def __init__(self, id, content, type, position, money, money2):
        self.id = id
        self.content = content
        self.type = type
        self.position = position
        self.money = money
        self.money2 = money2

    def print_card(self):
        print(self.id, self.content, self.type, self.position, self.money, self.money2)

class CommunityChestCard:
    def __init__(self, id, content, type, position, money, money2):
        self.id = id
        self.content = content
        self.type = type
        self.position = position
        self.money = money
        self.money2 = money2


class Dice:
    def __init__(self, dice_roll1=0, dice_roll2=0):
        self.dice_roll1 = dice_roll1
        self.dice_roll2 = dice_roll2
        self.doubles = 0
        self.update_doubles()

    def perform_roll(self):
        self.dice_roll1 = random.randint(1, 6)
        self.dice_roll2 = random.randint(1, 6)
        self.update_doubles()

    def update_doubles(self):
        if self.dice_roll1 == self.dice_roll2:
            self.doubles = 1
        else:
            self.doubles = 0

    def is_double(self):
        return self.doubles

    def get_dice_roll1(self):
        return self.dice_roll1

    def get_dice_roll2(self):
        return self.dice_roll2
