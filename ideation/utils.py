import random

colour = ['RED', 'GREEN', 'BLUE', 'YELLOW']
value = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'Skip', 'Reverse', 'Draw2', 'Wild', 'WildDraw4']

# cat = category of cards
cat = {
    0: 'zero', 1: 'number', 2: 'number', 3: 'number', 4: 'number',
    5: 'number', 6: 'number', 7: 'number', 8: 'number', 9: 'number',
    'Skip': 'special', 'Reverse': 'special', 'Draw2': 'special', 'Wild': ['wild','special'],
    'WildDraw4': ['wild', 'special']
}

# Each individual card
class Card:
    '''
        Class to represent a single card.
        
        Attributes:
        ---
            colour (str): 
                A string form of a colour
            value (int or str): 
                An int or a string
                e.g. ('BLUE', 4) or ('RED', 'Reverse')

        Methods:
        ---
            get_value:
                returns the value of the card: (colour, value)
            __str__:
                returns string representation of the object.
        '''
    # initialize - assign colour, value
    def __init__(self, colour, value):
        self.value = value
        # numbers from 0-9 are coloured
        if cat[value] == 'zero' or cat[value] == 'number' or cat[value] == 'special':
            self.colour = colour
        else:
            self.colour = 'BLACK'
    # get the value of the card
    def get_value(self):
        return (self.colour, self.value)
    # string function for this class output:e.g. 'BLUE 4'
    def __str__(self):
        return self.colour+" "+str(self.value)

# The deck of cards
class Deck:
    '''
        Class to represent a deck of cards.
        
        Methods:
        ---
            __str__:
                Returns string representation of the object.
            shuffle:
                Uses random library to shuffle the Deck.
            deal:
                Returns the last card from the Deck.
            count_deck:
                Returns the size (length) of the Deck
            
        '''
    def __init__(self):
        self.deck = []
        # iterate through each colour
        for c in colour:
            # whilst iterating through colour, iterate through each value
            for v in value:
                # add twice if number or action e.g. 1 or Draw2
                if cat[v] == 'number' or cat[v] == 'special':
                    for _ in range(2):
                        self.deck.append(Card(c,v))
                # add once if anything else e.g. 0 or Wild
                else:
                    self.deck.append(Card(c,v))

    # string function returns a list of cards in the deck
    def __str__(self):
        cards = [card.__str__() for card in self.deck]
        return str(cards)

    # shuffle the deck to randomise cards
    def shuffle(self):
        random.shuffle(self.deck)

    # deal from the top of the deck
    def deal(self):
        return self.deck.pop()

    # count deck size
    def count_deck(self):
      return len(self.deck)

# The player's hand
class Hand:
    '''
        Class to represent a hand of cards.
        
        Methods:
        ---
            add_card:
                Adds a card to the Hand.
            remove_card:
                Removes a card based on an index from the Hand.
            count_cards:
                Returns the number of cards in the Hand.
            last_card:
                Returns "Uno" if the player is on their second to last card.
            player_cards:
                Returns a string representation of the object.
            
    '''
    def __init__(self):
        self.cards = []
    # add a card to the player's hand
    def add_card(self, card):
        self.cards.append(card)
    # play card/remove card from the player's hand at chosen index (dependent on player choice in discard process)
    def remove_card(self, index):
        self.cards.pop(index)
    # counts the number of cards in the hand.
    def count_cards(self):
        return len(self.cards)
    # checks for last card in Hand
    def last_card(self):
        if len(self.cards) == 2:
            return "Uno"
    def player_cards(self):
        stringify = [str(card) for card in self.cards]
        return str(stringify)
    
# list of CPU Players
computer = {1:'Bot1', 2: 'Bot2', 3: 'Bot3', 4: 'Bot4', 5: 'Bot5', 6: 'Bot6', 7: 'Bot7', 8: 'Bot8', 9: 'Bot9'}

        

# discardTop = {top of discard pile (where the cards are played)}
# discardBot = {bottom of the discard pile (where new rule cards are played in each turn)}


# How To Use Classes Example:
deck = Deck()
player1 = Hand()
player2 = Hand()
player3 = Hand()
player4 = Hand()
players = [player1, player2, player3, player4]
# loop in a circular motion between players
# deal to one -> move -> deal to two -> move ...
# deckTop = card on top of dealing deck (the one being dealt)
deckTop = []
deck.shuffle()
# repeating the dealing process as rules state 7 times (for 7 cards per player)
for i in range(7):
  for player in players:
    # use deal method to add last card from deck to deckTop (the list will always have a single card)
    deckTop.append(deck.deal())
    # now use the add_card method (from Hand class) to add from deckTop to the player's hand
    player.add_card(deckTop.pop(-1))

print(player1.player_cards())
print(player2.player_cards())
print(player3.player_cards())
print(player4.player_cards())
print(deck.count_deck())