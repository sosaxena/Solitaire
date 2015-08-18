from Solitaire import *
import unittest

class TestSolitaire(unittest.TestCase):  # use any meaningful name

    
    def setUp(self):
        self.myDeck = Deck()
        self.myGame = Solitaire()

    def testMoveBetweenTableau(self):

        cardList=self.myGame.tableau[2]
        cards=cardList[-1:]
        
        #Move one card
        self.myGame.moveBetweenTableau(1,2,3)
        self.assertTrue(cards[-1] in self.myGame.tableau[3])
        self.assertEqual(1,len(self.myGame.tableau[2]))
        self.assertEqual(4,len(self.myGame.tableau[3]))

        #Move 5 cards
        cardList2=self.myGame.tableau[6]
        cards2=cardList2[-5:]
        self.myGame.moveBetweenTableau(5,6,1)
        self.assertTrue(cards2[-1] in self.myGame.tableau[1])
        self.assertTrue(cards2[-4] in self.myGame.tableau[1])
        self.assertTrue(cards2[-5] in self.myGame.tableau[1])
        self.assertTrue(cards2[-2] in self.myGame.tableau[1])
        self.assertTrue(cards2[-3] in self.myGame.tableau[1])
        self.assertEqual(6,len(self.myGame.tableau[1]))
        self.assertEqual(1,len(self.myGame.tableau[6]))

    def testmoveTableauToFoundation(self):

        #Move from Tableau 1 to Foundation 1:
        cardList=self.myGame.tableau[1]
        card=cardList[-1]
        self.myGame.moveTableauToFoundation(1,1)
        self.assertEqual([],self.myGame.tableau[1])
        self.assertTrue(card in self.myGame.foundation[1])
        self.assertFalse(card in self.myGame.tableau[1])
        
        #Move from Tableau 6 to Foundation 4:
        cardList2=self.myGame.tableau[6]
        card2=cardList2[-1]
        self.myGame.moveTableauToFoundation(6,4)
        self.assertTrue(card2 in self.myGame.foundation[4])
        self.assertFalse(card2 in self.myGame.tableau[6])


    def testMoveWasteToTableau(self):
        
        self.myGame.drawFromDeck() #Draw a card from the deck to fill the waste
        card=self.myGame.waste[-1]
        self.myGame.moveWasteToTableau(7)
        #Check whether the card from waste moved to Tableau 7
        self.assertTrue(card in self.myGame.tableau[7])

    def testMoveWasteToFoundation(self):
        self.myGame.drawFromDeck()
        card=self.myGame.waste[-1]
        self.myGame.moveWasteToFoundation(2)
        self.assertTrue(card in self.myGame.foundation[2])

    def testDrawFromDeck(self):
        #Draw 2 cards 
        self.myGame.drawFromDeck()
        self.myGame.drawFromDeck()
        self.assertEqual(2,len(self.myGame.waste))
        

        self.myGame.drawFromDeck()
        self.myGame.drawFromDeck()
        self.myGame.drawFromDeck()
        self.myGame.drawFromDeck()
        #Draw 4 more cards
        self.assertEqual(6,len(self.myGame.waste))

    def testFlipWaste(self):
        self.myGame.drawFromDeck()
        self.myGame.drawFromDeck()
        card1=self.myGame.waste[-1]
        card2=self.myGame.waste[-2]
        self.myGame.flipWaste()
        #Check Wste is empty
        self.assertEqual([],self.myGame.waste)
        #Check the cards are not present
        self.assertFalse(card1 in self.myGame.waste)
        self.assertFalse(card2 in self.myGame.waste)

    def testCheckIfWon(self):
        ls=self.myGame.foundation.values()
        #Initially We don't win as Foundation does not have 52 cards, all ordered by suit and rank
        self.assertEqual(False,self.myGame.checkIfWon())
        self.myGame.foundation = {1:range(0,13),2:range(13,26),3:range(26,39),4:range(39,52)}
        self.assertTrue(self.myGame.checkIfWon())

    def testDetermineFunctionType(self):
        #Blank Input
        input1=''
        self.assertEqual(0,self.myGame.determineFunctionType(input1))

        #Restart command
        
        input2='r'
        self.assertEqual(3,self.myGame.determineFunctionType(input2))

        #Get input command
        
        input3='g'
        self.assertEqual(1,self.myGame.determineFunctionType(input3))

        #Move command
        
        input4='m t54 t6'
        self.assertEqual(2,self.myGame.determineFunctionType(input4))


    def testDetermineMoveType(self):
        #Tableau to Tableau move type
        string1='m t[1,2] t6'
        self.assertEqual(1,self.myGame.determineMoveType(string1))

        #Tableau to Foundation move type
        string2='m t[3] f2'
        self.assertEqual(2,self.myGame.determineMoveType(string2))

        #Waste to Tableau move type
        string3='m w t3'
        self.assertEqual(3,self.myGame.determineMoveType(string3))

        #Waste to Foundation move type
        string4='m wf1'
        self.assertEqual(4,self.myGame.determineMoveType(string4))

        #Invalid Move type

        string5='m t45 o9'
        self.assertEqual(0,self.myGame.determineMoveType(string5))
        
        #Invalid Input type
        string6='filjslkln  889op'
        self.assertEqual(0,self.myGame.determineMoveType(string6))

    def testWasteString(self):

        #Empty Waste
        self.assertEqual("  ",self.myGame.wasteString())

        #Fill 2 cards in the waste and print the top card
        self.myGame.drawFromDeck()
        self.myGame.drawFromDeck()
        wasteList=self.myGame.waste
        wasteCard=wasteList[-1]
        if type(wasteCard.rank)==int:
            self.assertEqual(str(wasteCard.rank)+wasteCard.suit.upper(),self.myGame.wasteString())
        else:
            self.assertEqual(str(wasteCard.rank.upper())+wasteCard.suit.upper(),self.myGame.wasteString())
            

    def testDeckString(self):
        #Card of the deck is hidden so it should print xx
        self.assertEqual('xx',self.myGame.deckString())
        self.myGame.mainDeck = []
        self.assertEqual('  ',self.myGame.deckString())

    def testFoundationString(self):
        self.assertEqual(self.myGame.foundationString(),"                ")
        self.myGame.moveTableauToFoundation(5,1)
        self.myGame.moveTableauToFoundation(3,1)
        cardList=self.myGame.foundation.values()
        firstList=cardList[0]
        topCard = firstList[-1]
        x = topCard.__str__()
        self.assertEqual(self.myGame.foundationString(),"  "  + x + "            ")
    
        

    def testGetValues(self):
        self.assertEqual([10,7,2],self.myGame.getValues('m t10,7 t2',1))
        self.assertEqual([6,7],self.myGame.getValues('m t6 t7',2))
        self.assertEqual([1],self.myGame.getValues('m w t1',3))
        self.assertEqual([2],self.myGame.getValues('m wf2',4))

    def testgetValuesWasteMove(self):
        #Waste to Tableau Move
        self.assertEqual([2],self.myGame.getValuesWasteMove('mw[]t2'))

        #Waste to Foundation Move
        self.assertEqual([2],self.myGame.getValuesWasteMove('m:wf2'))

    def testGetValuesFoundationMove(self):
        #Move from Tableau to foundation
        self.assertEqual([7,2],self.myGame.getValuesFoundationMove('m t7:f2'))
        self.assertEqual([1,4],self.myGame.getValuesFoundationMove('m t1f(4)'))

    def testGetValuesTableauMove(self):
        #Two Digit Case
        self.assertEqual([12,6,2],self.myGame.getValuesTableauMove('m t12,6t2'))

        #One Digit Case
        self.assertEqual([1,5,3],self.myGame.getValuesTableauMove('m t1,5t[3]'))

    def testCheckMoveInputValid(self):
        #Moving between Tableaux
        self.assertEqual(False,self.myGame.checkMoveInputValid('m t1f t6(4)',1))
        self.assertEqual(True,self.myGame.checkMoveInputValid('m t[1,7] t4',1))

  
        self.assertEqual(False,self.myGame.checkMoveInputValid('m t15 f4',2))
        self.assertEqual(True,self.myGame.checkMoveInputValid('m t5 f3',2))

        #Moving from Waste to Tableau 
        self.assertEqual(False,self.myGame.checkMoveInputValid('mw3 t6(4)',3))
        self.assertEqual(True,self.myGame.checkMoveInputValid('m w t4',3))

        #Move Waste to foundation
        self.assertEqual(True,self.myGame.checkMoveInputValid('m w f1',4))
        self.assertEqual(False,self.myGame.checkMoveInputValid('mw3f3',4))

        

        

        
        
    def testCheckWasteMoveValid(self):
        #We are assuming the the user has entered a waste move type input. We want to check the format.
        self.assertEqual(True,self.myGame.checkWasteMoveValid('m w f1'))
        self.assertEqual(False,self.myGame.checkWasteMoveValid('m w f71'))
        self.assertEqual(True,self.myGame.checkWasteMoveValid('m w f3'))
        self.assertEqual(False,self.myGame.checkWasteMoveValid('m w6 f1'))
        

    def testCheckTableauMoveValid(self):
        #We are assuming the the user has entered a tableau to tableau move type input. We want to check the format.
        self.assertEqual(True,self.myGame.checkTableuMoveValid('m t[5,6] t7'))
        self.assertEqual(False,self.myGame.checkTableuMoveValid('m t5  t7'))
        self.assertEqual(True,self.myGame.checkTableuMoveValid('m t3,4 f2'))
        self.assertEqual(False,self.myGame.checkTableuMoveValid('m t3,4 f80'))

    def testCheckFoundationMoveValid(self):
        
        #We are assuming the the user has entered a tableau to foundation move type input. We want to check the format.
        self.assertEqual(True,self.myGame.checkFoundationMoveValid('m t5 f3'))
        self.assertEqual(False,self.myGame.checkFoundationMoveValid('m t57f2'))
        self.assertEqual(True,self.myGame.checkFoundationMoveValid('m t[3] f1'))
        self.assertEqual(False,self.myGame.checkFoundationMoveValid('m t3,4 f80'))

    
        
                         
        
    def testGetNumbers(self):
        self.assertEqual(self.myGame.getNumbers('3432gfds1 n %^,^&$'),[3,4,3,2,1,','])


    def testGetLetters(self):
        self.assertEqual(self.myGame.getLetters('234b43534,,5'),['b'])
        
    def testRemoveSpaces(self):
        self.assertEqual(self.myGame.removeSpaces('   m w  t[]1,4'),'mwt1,4')

    def testIsInt(self):
        self.assertTrue(self.myGame.isInt(1))
        self.assertFalse(self.myGame.isInt('f'))

    


        
     
    def testCheckLegalTableauMove(self):
        self.myGame.tableau = {2:[],3:[],4:[],5:[],6:[]}
        self.myGame.tableau[1] = [Card(10,'h'),Card(7,'c')]
        self.myGame.tableau[7] = [Card(5,'c'),Card(1,'d'),Card(8,'h')]
        self.assertTrue(self.myGame.checkLegalTableauMove(1,1,7))
        self.assertFalse(self.myGame.checkLegalTableauMove(1,7,1))
        self.assertFalse(self.myGame.checkLegalTableauMove(1,2,1))
        self.assertFalse(self.myGame.checkLegalTableauMove(1,1,2))
        self.assertFalse(self.myGame.checkLegalTableauMove(2,7,2))
        self.assertFalse(self.myGame.checkLegalTableauMove(1,1,1))

    def testCheckLegalTableauFoundationMove(self):
        self.myGame.tableau = {2:[],3:[],4:[],5:[],6:[]}
        self.myGame.tableau[1] = [Card(10,'h'),Card(7,'c'),Card(1,'c')]
        self.myGame.tableau[2] = [Card(4,'c')]
        self.myGame.tableau[7] = [Card(5,'c'),Card(1,'d'),Card(8,'h')]
        self.myGame.foundation = {1:[],2:[Card(6,'h'),Card(7,'h')],3:[],4:[Card(3,'c')]}
        self.assertTrue(self.myGame.checkLegalTableauFoundationMove(2,4))
        self.assertTrue(self.myGame.checkLegalTableauFoundationMove(1,1))
        self.assertFalse(self.myGame.checkLegalTableauFoundationMove(7,1))
        self.assertTrue(self.myGame.checkLegalTableauFoundationMove(2,4))
        
    def testCheckLegalWasteFoundationMove(self):
        self.myGame.foundation = {1:[],2:[Card(6,'h'),Card(7,'h')],3:[],4:[Card(3,'c')]}
        self.myGame.waste = []
        self.assertFalse(self.myGame.checkLegalWasteFoundationMove(1))
        self.myGame.waste = [Card(2,'c'),Card(1,'h')]
        self.assertTrue(self.myGame.checkLegalWasteFoundationMove(1))
        self.myGame.waste = [Card(2,'c'),Card(4,'c')]
        self.assertTrue(self.myGame.checkLegalWasteFoundationMove(4))
        self.assertFalse(self.myGame.checkLegalWasteFoundationMove(3))

    def testCheckLegalWasteTableauMove(self):
        self.myGame.tableau = {2:[],3:[],4:[],5:[],6:[]}
        self.myGame.tableau[1] = [Card(10,'h'),Card(7,'c'),Card(1,'c')]
        self.myGame.tableau[2] = [Card(4,'c')]
        self.myGame.tableau[7] = [Card(5,'c'),Card(1,'d'),Card(8,'h')]
        self.myGame.waste = []
        self.assertFalse(self.myGame.checkLegalWasteTableauMove(1))
        self.myGame.waste = [Card(7,'c')]
        self.assertTrue(self.myGame.checkLegalWasteTableauMove(7))
        self.assertFalse(self.myGame.checkLegalWasteTableauMove(3))
        self.myGame.waste = [Card(2,'c'),Card(13,'c')]
        self.assertTrue(self.myGame.checkLegalWasteTableauMove(3))

    def testExecuteMove(self):
        self.myGame.tableau = {2:[],3:[],4:[],5:[],6:[]}
        self.myGame.tableau[1] = [Card(10,'h'),Card(7,'c'),Card(1,'c')]
        self.myGame.waste= [Card(10,'h'),Card(1,'s')]
        
        cardlist=self.myGame.tableau[1]
        card=cardlist[-1]
        self.myGame.tableau[2] = [Card(4,'c')]
        self.myGame.tableau[7] = [Card(5,'c'),Card(1,'d'),Card(8,'h')]
        self.myGame.foundation = {1:[],2:[Card(6,'h'),Card(7,'h')],3:[],4:[Card(3,'c')]}
        self.myGame.waste = [Card(2,'c'),Card(7,'c')]
        self.myGame.executeMove(1,[1,1,2])
        self.assertIn(card,self.myGame.tableau[2])
        self.assertNotIn(card,self.myGame.tableau[1])
        
        cardlist=self.myGame.tableau[7]
        card=cardlist[-1]
        self.myGame.executeMove(2,[7,1])
        self.assertIn(card,self.myGame.foundation[1])
        self.assertNotIn(card,self.myGame.tableau[7])
        
        card=self.myGame.waste[-1]
        self.myGame.executeMove(3,[7])
        self.assertIn(card,self.myGame.tableau[7])
        self.assertNotIn(card,self.myGame.waste)

        card=self.myGame.waste[-1]
        self.myGame.executeMove(4,[4])
        self.assertIn(card,self.myGame.foundation[4])
        self.assertNotIn(card,self.myGame.waste)
        
        
        
unittest.main() 
    


    

