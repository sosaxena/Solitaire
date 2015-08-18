from cards import *
import unittest

class TestCards(unittest.TestCase):  # use any meaningful name

    def setUp(self):
        self.myCard = Card('J', 's')
        self.myHiddenCard = Card(2, 'c')
        self.myHiddenCard.set_hidden()
        self.myNumericCard = Card('3', 'D')
        self.myHeartsCard = Card('Q', 'H')
        self.myDiamondsCard = Card('a', 'd')

        self.myDeck = Deck()
    
    def testInitializer(self):
        '''the initializer test is testing the rank and the suit '''
        #for the initialize test we will not rely on setUp
        card = Card('K', 'c')
        self.assertEqual(card.get_rank(), 13)
        card = Card(4 , 'd')
        self.assertEqual(card.get_rank(), 4)
        card = Card('Q', 's')
        self.assertEqual(card.get_rank(), 12)
        card = Card('J', 'h')
        self.assertEqual(card.get_rank(), 11)
        card = Card('a', 'h')
        self.assertEqual(card.get_rank(), 1)

    def testSuit(self):
        self.assertEqual(self.myHeartsCard.get_suit(), 'H')
        self.assertEqual(self.myDiamondsCard.get_suit(), 'D')

    def testStringFunction(self):
        self.assertEqual(str(self.myCard), 'JS')
        self.assertEqual(str(self.myHiddenCard), 'xx')
        self.assertEqual(str(self.myNumericCard), '3D')
        blankCard = Card()
        self.assertEqual(str(blankCard), 'blk')

    def testHasSameColor(self):
        self.assertTrue(self.myCard.has_same_color(self.myHiddenCard))
        self.assertFalse(self.myCard.has_same_color(self.myNumericCard))
        self.assertFalse(self.myCard.has_same_color(self.myHeartsCard))
        self.assertTrue(self.myHeartsCard.has_same_color(self.myDiamondsCard))

    def testSetHidden(self):
        self.myHiddenCard.set_hidden(False)
        self.assertFalse(self.myHiddenCard.get_hidden())

    def testSetHiddenAndStringify(self):
        self.myHiddenCard.set_hidden(False)
        self.assertEqual(str(self.myHiddenCard), '2C')  
        
######################## unit tests for deck ##############################
    def testDeckInitializer(self):
        myDeck = Deck()
        listOfCards = myDeck.deck
        #make sure you have the right number of cards
        self.assertEqual(len(listOfCards), 52)
        for c in listOfCards:
            self.assertTrue(isinstance(c, Card))
        ranks = ['a'] + range(2,11) + ['j', 'q', 'k']
        suits = ['c', 'd', 'h', 's']
        stringifiedCards = [str(x) for x in listOfCards]
        #make sure that every rank,suit combination is in the deck
        #our method of asserting equality is to use the string function
        for rank in ranks:
            for suit in suits:
                self.assertTrue(str(Card(rank,suit)) in stringifiedCards)

    def testShuffle(self):
        currentDeck = self.myDeck.deck[:]
        self.myDeck.shuffle()
        #make sure something got rearranged
        #using a helper function here to show some more examples
        self.assertFalse(self.compareTwoDecks(self.myDeck.deck, currentDeck))

    def testDeal(self):
        expectedCard = self.myDeck.deck[51]
        dealtCard = self.myDeck.deal()
        self.assertTrue(isinstance(dealtCard, Card))
        #assert one card was taken from the deck
        self.assertEqual(51, len(self.myDeck.deck))
        self.assertEqual(expectedCard, dealtCard)

    def testDiscard(self):
        top4Cards = self.myDeck.deck[:-4]
        self.myDeck.discard(4)
        self.assertEqual(48, len(self.myDeck.deck))
        #assert that none of the top 4 cards are in still in the deck
        listOfCards = [str(c) for c in self.myDeck.deck]
        for cards in top4Cards:
            self.assertFalse(str(cards) not in listOfCards)

    def testTop(self):
        #this unit test relies on the fact that
        #we tested the deal method first. 
        topCard = self.myDeck.top()
        dealtCard = self.myDeck.deal()
        self.assertEqual(topCard, dealtCard)

    def testBottom(self):
        bottomCard = self.myDeck.deck[0]
        self.assertEqual(bottomCard, self.myDeck.bottom())

    def testadd_card_top(self):
        #assume discard works before you get here
        topCard = self.myDeck.deal()
        self.myDeck.add_card_top(topCard)
        self.assertEqual(self.myDeck.top(), topCard)

    def testadd_card_bottom(self):
        bottomCard = Card('Q', 'h')
        self.myDeck.add_card_bottom(bottomCard)
        #deal out all the cards and ensure that the last one is this bottomCard
        while len(self.myDeck.deck) > 0:
            card = self.myDeck.deal()
        self.assertEqual(card, bottomCard)

    def testCardsLeft(self):
        self.myDeck.discard(10)
        self.assertEqual(42, self.myDeck.cards_left())
        card = self.myDeck.deal()
        self.assertEqual(41, self.myDeck.cards_left())

    def testEmpty(self):
        self.assertFalse(self.myDeck.empty())
        while len(self.myDeck.deck) > 0:
            card = self.myDeck.deal()
        self.assertTrue(self.myDeck.empty())

    def compareTwoDecks(self, deck1, deck2):
        strDeck1 = self.stringifyDeck(deck1)
        strDeck2 = self.stringifyDeck(deck2)
        return strDeck1 == strDeck2

    def stringifyDeck(self, listOfCards):
        cards = [str(x) for x in listOfCards]
        concatCards = reduce(lambda x,y: x+y, cards)
        return concatCards
    
unittest.main() 
