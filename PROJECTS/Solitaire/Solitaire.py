# -*- coding: cp1252 -*-

from cards import *
import random
import string

#------------------Code Written by Soumya Saxena and Guðrún Gylfadóttir----------------
def main():
    '''Prints introduction, calls the play() function, asks user whether they want to play again.'''
    printIntroMessage()
    solitaire = Solitaire()
    solitaire.play()
    choice = raw_input('Do you want to play again? y/n')
    while choice != 'n':
        solitaire.play()
    confirmation = raw_input('\nDo you really want to quit? Enter q to exit the game.')
    if confirmation == 'q':
        choice = 'n'
    else:
        choice = 'y'



def printIntroMessage():
    '''Prints an introductory message'''
    print '''Welcome to solitaire!
Your goal is to get all of your cards to the foundation at the top,
with one column for each suit, and with the cards organized in ascending order.
You can move cards from the drawpile to the tableau at the bottom,
but you have to remember the rules.
\nAny card that you move to the tableau has to be:
-one number less than the card you place it on
-a different color than the card you place it on
\nAny card that you move to the foundation has to be:
-one number greater than the card you place it on
-the same suit than the card you place it on'''
    print '''\nThis is how gameplay works: \n---------------------------
\nEnter r to start another game \n\nEnter g to draw from the deck \n\nEnter m to make a move, followed by a source and then a destination:\n
    Move the top card from the drawpile by entering w\n
    Move a card FROM the tableau by first entering t,
        then the column number and card number, separated by a comma\n
    Move a card TO a tableau column by entering t and the column number\n
    Move a card to the foundation by entering f and the column number'''
    print '''-------------------------------\nSome example moves:
\n'm w t4' \nwill move a card from the drawpile to the 5th column in the tableau
\n'm t2,3 f4' \nwill move 2 cards from the 3rd column in the tableau to the 4th column of the foundaton
\n'm t7,2 t4' \nwill move 7 cards from the 2nd column to the 4th column of the tableau'''

class Solitaire():

    'Waste= All cards show, Foundation: All cards show, Tableau : Top card shows, Deck: Top card is hidden'
    
    def __init__(self):
        '''establishes a deck, deals from the deck to create a tableau dictionary, creates an empty foundation dictionary'''
        self.mainDeck= Deck()
        self.mainDeck.shuffle()
        self.waste=[]
        self.foundation={1:[],2:[],3:[],4:[]}
        self.tableau = {}
        for i in range(1,8):
            stack = []
            for j in range(0,i):
                stack.append(self.mainDeck.deal())
            self.tableau[i]=stack
        for cardList in self.tableau.values():
            for card in cardList:
                card.set_hidden(True)
        for otherCardList in self.tableau:
            lst = self.tableau[otherCardList]
            lst[-1].show_card()

    def play(self):
        'asks for user input, displays the game, calls check and move functions according to user input'''
        print '\n------------------------------\nNew Game\n'
        self.display()
        userInput = raw_input('\n\nPlease enter r, g, or a move specification.\n\n')
        while userInput != 'r':
            functionType = self.determineFunctionType(userInput)
            if functionType == 1:
                if self.mainDeck.empty():
                    self.flipWaste()
                self.drawFromDeck()
                print ""
                self.display()
            elif functionType == 2:
                moveType = self.determineMoveType(userInput)
                if self.checkMoveInputValid(userInput, moveType):
                    values= self.getValues(userInput, moveType)
                    if moveType == 1:
                        if self.checkLegalTableauMove(values[0],values[1],values[2]):
                            self.executeMove(moveType,values)
                            print ""
                            self.display()
                        else:
                            print  '\nOnly tableau 1-7 are valid, and you can only place a card on a card of a different color with a rank that is one higher.'
                    elif moveType == 2:
                        if self.checkLegalTableauFoundationMove(values[0],values[1]):
                            self.executeMove(moveType,values)
                            if self.checkIfWon():
                                print "You won!"
                                break
                            print ""
                            self.display()
                        else:
                            print '\nOnly tableau 1-7 and foundation 1-4 are valid, and you can only place cards in the foundation one at a time in ascending order, with each suit in its own stack.'
                    elif moveType == 3:
                        if self.checkLegalWasteTableauMove(values[0]):
                            self.executeMove(moveType,values)
                            print ""
                            self.display()
                        else:
                            print '\nOnly tableau 1-7 are valid, and you can only place a card on a card of a different color with a rank that is one higher.'
                    elif moveType == 4:
                        if self.checkLegalWasteFoundationMove(values[0]):
                            self.executeMove(moveType,values)
                            if self.checkIfWon():
                                print "\n\nYou won!"
                                break
                            print ""
                            self.display()
                        else:
                            print '\nOnly foundation 1-4 are valid, and you can only place cards in the foundation one at a time in ascending order, with each suit in its own stack.'
                    else:
                        print '\nA move should be followed by a source and a destination. \nTableau sources must be specified with a card and column number, e.g. \'t1,2\'.'
                else:
                    print '\nPlease enter a move option in the valid format.'
            else:
                print '\nThe input can only be r, g, or a move.'
            print "\n"    
            userInput = raw_input('\nPlease enter r, g, or a move specification.')
        

            
        


    def drawFromDeck(self):
        '''takes the top card from the deck and places it face up in the waste'''
        dealtCard = self.mainDeck.deal()
        dealtCard.show_card()
        self.waste.append(dealtCard)

    

    def flipWaste(self):
        '''takes the cards in the waste list and places them facedown in the deck'''
        for card in self.waste:
            card.set_hidden()
            self.mainDeck.add_card_top(card)
        self.waste = []
        

    


    def tableauPrint(self):
        '''prints the rank and suit of each card in each key of the tableau dictionary in a vertical fashion'''
        lengths = []
        for cardList in self.tableau.values():
            length = len(cardList)
            lengths.append(length)
        longest = max(lengths)
        for i in range(0,longest):
            print "\n"
            for cardList in self.tableau.values():
                length = len(cardList)
                if length < i + 1:
                    print "   ",
                else:
                    card = cardList[i]
                    print str(" ") + card.__str__(),
                    
        
    def foundationString(self):
        '''gets the rank and suit values of the top card in each key of the foundation dictionary and returns them in a string''' 
        foun = ""
        for cardList in self.foundation.values():
            length = len(cardList)
            
            if length < 1:
                x = "  "
            else:
                card = cardList[-1]
                x = card.__str__()
            foun = foun + str('  ') + x
        return foun
        
        
            
            

    def wasteString(self):
        '''takes the rank and suit values of the top card in the waste list and returns a string'''
        if self.waste == []:
            x = "  "
        else:
            card = self.waste[-1]
            x= card.__str__()
        return x

    def deckString(self):
        '''returns an empty string if the deck list is empty, returns 'xx' if it is not''' 
        if self.mainDeck == []:
            x = "  "
        else:
            x= "xx"
        return x

    def display(self):
        '''prints the strings returned by the various string functions in one line and calls the tableauPrint function, creating a display'''
        w = self.wasteString()
        f = self.foundationString()
        d = self.deckString()
        print d + str("  ") +  w + str("   ") + f
        self.tableauPrint()
        
        
        


    def checkIfWon(self):
        '''returns true if all of the cards from the deck are located in the foundation'''
        ls=self.foundation.values()
        count = 0
        for lst in ls:
            if len(lst) == 13:
                count = count + 1
        if count == 4:
            x = True
        else:
            x = False
        return x
                

    

    def determineFunctionType(self, userInput):
        '''returns a value corresponding to the type of input the user entered in response to the move prompt - whether g, r, a move, or none of the three'''
        userInput = self.removeSpaces(userInput)
        if userInput == '':
             x = 0
        else:
            if userInput == 'g':
                x = 1
            elif userInput[0] == 'm':
                x = 2
            elif userInput == 'r':
                x = 3
            else:
                 x = 0
        return x



           

    def determineMoveType(self, string):
        '''returns a value corresponding to the type of move the user has specified'''
        alpha = self.getLetters(string)
        try:
            source = alpha[1]
            destination = alpha[2]
        except IndexError:
            x = 0
            return x
        if source == 't':
            if destination == 't':
                x = 1
            elif destination == 'f':
                x = 2
            else:
                x = 0
        elif source == 'w':
            if destination == 't':
                x = 3
            elif destination == 'f':
                x = 4
            else:
                x = 0
        else:
            x = 0
        return x
    
 

    def checkMoveInputValid(self,string,moveType):
        '''takes an input and calls an appropriate check function based on the move type'''
        string = self.removeSpaces(string)
        num = self.getNumbers(string)
        length = len(num)
        if moveType == 0:
            x = False
        elif moveType == 1:
            x = self.checkTableuMoveValid(string)
        elif moveType == 2:
            x = self.checkFoundationMoveValid(string)
        elif moveType == 3:
            x =  self.checkWasteMoveValid(string)
        elif moveType == 4:
            x = self.checkWasteMoveValid(string)
        return x
     
                
            
    def checkTableuMoveValid(self,string):
        '''checks to see if a move from a tableau has 3 numbers, with first two separated by a comma - card, tableau column source, tableau column destination'''
        string = self.removeSpaces(string)
        num = self.getNumbers(string)
        if num != []:
            length = len(num)
            if "," in num:
                comma = num.index(",")
                if comma == 1:
                    if length == 4:
                        x = True
                    else:
                        x = False
                elif comma == 2:
                    if length == 5:
                        x = True
                    else:
                        x = False
            else:
                x = False
        else:
            x = False
        return x

    def checkWasteMoveValid(self,string):
        '''checks to see if a move from the waste has 1 integer'''
        string = self.removeSpaces(string)
        num = self.getNumbers(string)
        if num != []:
            if "," not in num:
                if len(num) == 1:
                    x = True
                else:
                    x = False
            else:
                x=False
        else:
            x = False
        return x

    def checkFoundationMoveValid(self,string):
        '''checks to see if a move from the tableau to the foundation has 2 numbers - 1 for the tableau source oolumn, 1 for the foundation destination column''' 
        string = self.removeSpaces(string)
        num = self.getNumbers(string)
        if num != []:
            if "," not in num:
                if len(num) == 2:
                    x = True
                else:
                    x = False             
            else:
                x= False
        else:
            x = False
        return x


    def getValues(self,string,moveType):
        '''calls the appropriate getValues function according to move type'''
        string = self.removeSpaces(string)
        num = self.getNumbers(string)
        length = len(num)
        if moveType == 1:
            x = self.getValuesTableauMove(string)
        elif moveType == 2:
            x = self.getValuesFoundationMove(string) 
        elif moveType == 3:
            x = self.getValuesWasteMove(string)
        elif moveType == 4:
            x = self.getValuesWasteMove(string)
        return x
    
    def getValuesTableauMove(self,string):
        '''extracts the three numbers from the tableau move input that has been checked and returns them as a list, dealing appropriately with double digit numbers'''
        string = self.removeSpaces(string)
        num = self.getNumbers(string)
        comma = num.index(",")
        values = []
        if comma == 1:
            values.append(num[0])
            values.append(num[2])
            values.append(num[3])
        elif comma == 2:
            values.append(int(str(num[0]) + str(num[1])))
            values.append(num[3])
            values.append(num[4])
        return values


    def getValuesWasteMove(self,string):
        '''extracts the integer from the waste move input and returns it as a string; Deals with both w-f and w-t'''
        string = self.removeSpaces(string)
        num = self.getNumbers(string)
        return num

    def getValuesFoundationMove(self,string):
        '''extracts two integers from a tableau to foundation move input and returns them as a list'''
        string = self.removeSpaces(string)
        num = self.getNumbers(string)
        lst = []
        lst.append(num[0])
        lst.append(num[1])
        return lst


    def executeMove(self,moveType,values):
        '''calls the appropriate move function based on move type'''
        if moveType == 1:
            self.moveBetweenTableau(values[0],values[1],values[2])
        elif moveType == 2:
            self.moveTableauToFoundation(values[0],values[1])
        elif moveType == 3:
            self.moveWasteToTableau(values[0])
        elif moveType == 4:
            self.moveWasteToFoundation(values[0])

              
    def moveBetweenTableau(self,i,j,k):
        '''takes the ith card from the top of the values of key j of the tableau and all cards above it, removes the list and appends it list to the values of key k'''
        lst = self.tableau[j]
        lst2=self.tableau[k]
        movedList = lst[-i:]
        lst2.extend(movedList)
        lst = lst[:-i]
        if lst != []:
            uncoveredCard = lst[-1]
            uncoveredCard.show_card()           
        self.tableau[j]=lst
        
        
    
    def checkLegalTableauMove(self,i,j,k):
        '''gets the values of the ith card from the top of the values of key j of the tableau, and returns true if it is a different color from the top card of the values of key k, as well as having a rank that is one less'''
        if j not in range (1,8):
            x = False
            return x
        if self.tableau[j] == []:
            x = False
            return x
        elif i > len(self.tableau[j]):
            x = False
            return x
        if k not in range (1,8):
            x = False
            return x
        movedCardList = self.tableau[j]
        movedCard = movedCardList[-i]
        if movedCard.get_hidden():
            x = False
        else:
            rank = movedCard.get_rank()
            if self.tableau[k] == []:
                if rank == 13:
                    x = True
                else:
                    x = False           
            else:
                receivingCardList = self.tableau[k]
                receivingCard = receivingCardList[-1]
                desiredRank  = receivingCard.get_rank() - 1
                if not receivingCard.has_same_color(movedCard):
                    if rank == desiredRank:
                        x= True
                    else:
                        x = False
                else:
                    x= False
        return x
  

    def moveTableauToFoundation(self,n,m):
        '''moves the top card of the values of key n to the top of the values list of key m of the foundation dictionary'''
        lst = self.tableau[n]
        lst2=self.foundation[m]
        movedCard = lst[-1]
        lst2.append(movedCard)
        lst=lst[:-1]
        if lst != []:
            uncoveredCard = lst[-1]
            uncoveredCard.show_card()
        self.tableau[n]=lst

    def checkLegalTableauFoundationMove(self,n,m):
        '''returns true if the top card of key n of the tableau is the same suit as the top card of key m of the foundation and its rank is 1 greater'''
        if n not in range (1,8):
            x = False
            return x
        if m not in range (1,5):
            x = False
            return x
        if self.tableau[n] == []:
            x = False
            return x
        cardList = self.tableau[n]
        card = cardList[-1]
        rank = card.get_rank()
        if self.foundation[m] == []:
            if rank == 1:
                x = True
            else:
                x = False
        else:
            foundationCardList = self.foundation[m]
            foundationCard = foundationCardList[-1]
            if foundationCard.get_suit() == card.get_suit():
                desiredRank = foundationCard.get_rank() +1
                if rank == desiredRank:
                    x = True
                else:
                    x = False
            else:
                x = False
        return x
        
    def moveWasteToTableau(self, n):
        '''removes the top card of the waste and appends it the the values list of the nth key of the tableau'''
        w = self.waste[-1]
        lst = self.tableau[n]
        lst.append(w)
        self.waste = self.waste[0:-1]

    def checkLegalWasteTableauMove(self,n):
        '''returns true if the top card of the waste is a different color from and one rank lower than the top card of the nth key of the tableau, returns false if not or if the waste is empty'''
        if n not in range (1,8):
            x = False
            return x
        try:
            movedCard = self.waste[-1]
        except IndexError:
            x = False
            return x
        rank = movedCard.get_rank()
        if self.tableau[n] == []:
            if rank == 13:
                x = True
            else:
                x = False
        else:
            receivingCardList = self.tableau[n]
            receivingCard = receivingCardList[-1]
            movedCard = self.waste[-1]
            desiredRank  = receivingCard.get_rank() - 1
            if not receivingCard.has_same_color(movedCard):
                if movedCard.get_rank() == desiredRank:
                    x= True
                else:
                    x = False
            else:
                x= False
        return x
        

    def moveWasteToFoundation(self,m):
        '''removes the top card of the waste list and appends it to the mth key of the tableau dictionary'''
        w = self.waste[-1]
        lst = self.foundation[m]
        lst.append(w)
        self.waste = self.waste[0:-1]

    def checkLegalWasteFoundationMove(self, m):
        '''returns true if the top card of the waste is an ace or if its rank is one higher than the top card of the mth key of the foundation dictionary, returns false if not or if the waste is empty'''
        if m not in range (1,5):
            x = False
            return x
        try:
            card = self.waste[-1]
            rank = card.get_rank()
        except:
            ValueError
            x = False
            return x
        if self.foundation[m] == []:
            if rank == 1:
                x = True
            else:
                x = False
        else:
            foundationCardList = self.foundation[m]
            foundationCard = foundationCardList[-1]
            if foundationCard.get_suit() == card.get_suit():
                desiredRank = foundationCard.get_rank() +1
                if rank == desiredRank:
                    x = True
                else:
                    x = False
            else:
                x = False
        return x


    def getNumbers(self,string):
        '''takes a string and removes any characters that are not integers or commas, returns the string'''
        string = self.removeSpaces(string)
        num = []
        for ch in string:
            if self.isInt(ch):
                num.append(int(ch))
            elif ch == ",":
                num.append(ch)
        return num
            
                             
                    
                   
    def getLetters(self,string):
        '''takes a string and removes all characters that are not letters, returns the string'''
        string = self.removeSpaces(string)
        string = string.lower()
        alpha = []
        for ch in string:
            if not self.isInt(ch):
                if ch != ",":
                    alpha.append(ch)
                
        return alpha
       
         
    def removeSpaces(self,string):
        '''takes a string and removes all characters that are not integers, letters, or commas, returns the string'''
        for i in string:
            if not i.isalpha():
                if not self.isInt(i):
                    if i != ',':
                        string = string.replace(i,'')
        string = string.lower()
        return string   
        

    def isInt(self,arg):
        '''returns true if a character is an integer, false if not'''
        try:
            arg = int(arg)
        except ValueError, e:
            return False
        else:
            return True
if __name__ == '__main__':
    main()                   
        
            
                
        



    
        
            
