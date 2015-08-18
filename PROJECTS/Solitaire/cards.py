import random # needed for shuffling a Deck

class Card(object):
    """Denote a card with rank and suit"""
    """ Also, hidden indicates whether the card is face up or face down"""
    # Protocol
    #   1. 'no card' is represented by BOTH r = 0 and s = ''
    #   2. set_rank and set_suit should be commented out after development and debugging
    #   3  rank is int: 1=Ace, 2-10 face value, 11=Jack, 12=Queen, 13=King
    #   a person using this class should be able to create a card by saying
    #   card = Card('J', 'c')
    #   card = Card('j', 's')
    #   card = Card(4, 'd') 
    #   card = Card('a', 's')
    #   for jack, queen, king and ace you have to use single letter
    #   safely assume that the consumer of this class will always create it properly
    def __init__(self, r=0, s=''): 
       self.rank = r
       self.suit = s
       self.hidden = False

        
    def has_same_color(self, other):
        """ is the other card the same color as this instance """
        suit = self.get_suit()
        otherSuit = other.get_suit()
        if suit == 'D' or suit == 'H':
            if otherSuit == 'D' or otherSuit == 'H':
                return True
        elif suit == 'C' or suit == 'S':
            if otherSuit == 'C' or otherSuit == 'S':
                return True
        return False
        
    def set_hidden(self, val=True):
        """Set the card's hidden value, default True"""
        self.hidden = val

    def get_hidden(self):
        """Retrieve the card's hidden value"""
        return self.hidden
        
    def show_card(self):
        """Set the card as a non-hidden card"""
        self.hidden = False
        
    def set_rank(self, r):
        """For Development and Debugging only: Set the rank of the card: 0-13"""               
        self.rank = r
        
    def set_suit(self, s):
        """For Development and Debugging only: Set the suit of the card: C,S,D,H"""
        self.suit = s
        
    def get_rank(self):
        """Return rank of the card as int: 0-13"""
        if self.rank == 'K' or self.rank == 'k':
            return 13
        elif self.rank == 'Q' or self.rank == 'q':
            return 12
        elif self.rank == 'J' or self.rank == 'j':
            return 11
        elif self.rank == 'A' or self.rank == 'a':
            return 1
        return self.rank
        
    def get_suit(self):
        """Return suit of the card as string: C,S,D,H"""
        return self.suit.upper()
        
    def __str__(self):
        """String representation of card for printing: rank + suit,
           e.g. 7S or JD, 'blk' for 'no card' and 'xx' for a face down card"""
        if self.rank == 0:
            return 'blk'
        if self.hidden:
            return 'xx'
        if type(self.rank) == int:
            return str(self.rank) + self.suit.upper()
        return self.rank.upper() + self.suit.upper()


class Deck():
    """Denote a deck to play cards with"""
    
    def __init__(self):
        self.deck = []
        """Initialize deck as a list of all 52 cards: 13 cards in each of 4 suits"""
        for rank in range(2,11):
            for suit in ['h', 'c' , 'd' , 's']:
                card = Card(rank, suit)
                self.deck.append(card)
        for rank in ['j', 'q', 'k', 'a']:
            for suit in ['h', 'c' , 'd' , 's']:
                card = Card(rank, suit)
                self.deck.append(card)
        
    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.deck) 

    def deal(self):
        """Deal a card by returning the card that is removed off the top of the deck"""
        return self.deck.pop()
  
    def discard(self, n):
        """Remove n cards from the top of the deck"""
        self.deck = self.deck[:-n]

    def top(self):
        """Return the value of the top card -- do not remove from deck."""
        return self.deck[-1]

    def bottom(self):
        """Return the value of the bottom card -- do not remove from deck."""
        return self.deck[0]

    def add_card_top(self, c):
        """Place card c on top of deck"""
        self.deck.append(c)

    def add_card_bottom(self,c):
        """ Place card c on the bottom of the deck"""
        self.deck = [c] + self.deck

    def cards_left(self):
        """Return number of cards in deck"""
        return len(self.deck) 

    def empty(self):
        """Return True if the deck is empty, False otherwise"""
        return len(self.deck) == 0

    def __str__(self):
        """Represent the whole deck as a string for printing -- very useful during code development"""
        listofCards = [str(x) for x in self.deck]
        #after every 13th card add in a "\n"
        string = ''
        counter = 0
        for card in listofCards:
            if counter % 13 ==0:
                string += '\n'
            string += ' ' + card
            counter += 1 
        return string
    
