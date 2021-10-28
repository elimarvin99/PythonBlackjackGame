#in order to run a python file from the command line you have to go to the 
#file location and type "pyhton filename.py" for it to run

#A command-line based blackjack game

import random
#why as tuples and not as lists?
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        #calls the key value for the integer value of any rank
        self.value = values[rank]
    
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    #we don't take in a parameter from the user for a deck because a deck is a standardized object that should be the same every time/instance
    def __init__(self):
        # start with an empty list
        self.full_deck = []  
        for suit in suits:
            for rank in ranks:
                #classify each card to be a Card class object containing a suit and rank
                self.full_deck.append(Card(suit,rank))
    
    def shuffle(self):
        #this happens in place without returning anything
        random.shuffle(self.full_deck)
        
    def deal(self):
        #assign a variable that stores a card taken off the deck
        single_card = self.full_deck.pop()
        return single_card
    
    def __str__(self):
        #set placeholder as string in order to append from our list to the string
        deck_comp = ''
        for card in self.full_deck :
            #add string as new line card with string method from card class which prints us the full card(suit and rank)
            deck_comp += '\n' + card.__str__()
        return "The deck has: " + deck_comp

#essentialy the class of each player
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value. value will change as more cards are added to the deck (self.cards)
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        #the card passed into the hand will be taken from the deal method of the Deck class. Deck.deal
        self.cards.append(card)
        #get value of card passed in (by looking up the rank key in the values dictionary) and add it to value of the hand
        self.value += values[card.rank]
        
        #track aces by adding them to the ace counter 
        if card.rank == 'Ace':
            self.aces += 1
    #when in our code do we call this method (to apply it)? when we use the hit method we will run this method to adjust for aces so we don't bust
    def adjust_for_ace(self):
        #aces are considered as 11 unless the hand is over 21, than we lower its value to a 1
        #if value over 21 and i still have an ace(to convert to a 1, otherwise its a bust)
        #here we are treating an integer (self.aces) as a boolean (if true (there is an ace (1) in self.ace) the while loop will run)
        while self.value > 21 and self.aces:
            #if hand is higher than 21 we will automatically consider the ace to be 1 and update the ace counter that we have removed an ace(because it is no longer worth 11)
            self.value -= 10
            self.aces -= 1

class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

#provide an argument of an instance of a Chip class for the function
def take_bet(chips): #get users bet
       while True:
            try:
                chips.bet = int(input("How many chips would you like to bet on this hand: "))
            except: #if player doesn't add in an int
                print("Sorry, please provide an integer")
            else:
                if chips. bet > chips.total:
                    print("Sorry, you don't have enough chips. Current Balance {}".format(chips.total))
                    #loop will run again because we still haven't met the condition to break out of it
                else:
                    break #end the take_bet function

#takes in the deck and players hand and updates a card to the players hand (hand passed here is player or dealer)
#later on we will have to make a function that asks if player wants to hit and only then run this function
def hit(deck,hand):
    #get card from the deck
    single_card = deck.deal()
    #add card to our hand(and adjust our counter of total hand's value)
    hand.add_card(single_card)
    #check if new card is an ace and adjust value of hand accordingly
    hand.adjust_for_ace()

#this function takes into account the deck (to hit off it) and the player (to ask him if he wants to hit off it)
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        #only look at first letter in lowercase of input (in case user typed 'Hit' or 'stand')
        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")
        
        if x[0].lower() == 'h':
            hit(deck,hand)  # hit() function defined above

        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again.")
            #continue in the while loop to ask for input again
            continue
            #if one of the conditions was met than we will exit the while loop
        break

#this function is shown in the begining
def show_some(player,dealer):
    #show only one of the dealers cards
    print("\n Dealers Hand: ")
    print("First card hidden")
    #don't show the dealers first card at index place 0
    print(dealer.cards[1])
    #show all (2) of the players cards
    print("\n Player's hand: ")
    for card in player.cards:
        print(card)
    
    
    
def show_all(player,dealer):
    #show all the dealers cards
    print("\n Dealers Hand: ")
    for card in dealer.cards:
        print(card)
    #because this function is coming at the end we actually want to calculate and display value of the hand
    print("Value of dealer's hand: {}".format(dealer.value))
    #show all (2) of the players cards
    #another way to print all the cards without a for loop is with * plus an argument of how you want each item seperated
    print("\n Player's hand: ",*player.cards,sep='\n')
    print("Value of player's hand: {}".format(player.value))


#for all these functions we will print out what is happening and adjust the attributes accordingly
def player_busts(player,dealer,chips):
    print("BUST PLAYER")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("PLAYER WINS")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Player wins, Dealer busted")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print("Dealer wins")
    chips.lose_bet()
    
    
def push(player,dealer):
    #chips aren't passed in because in this scenario nothing happens to them
    print("Dealer and player tie! PUSH")


while True:
    # Print an opening statement
    print("Welcome to Blackjack")
    print("You have 100 chips in your wallet")

    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    #create player and dealer
    #each instance of a hand class object automatically creates a value and ace counter
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
        
    # Set up the Player's chips
    player_chips = Chips()
    
    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)

    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        #we will be accesing the deck here to the player_hand
        hit_or_stand(deck,player_hand)
        
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)
        
 
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
        

            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        #create loop that will cause dealer to hit until his hand reaches 17 (soft 17)
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
    
    
        # Show all cards
        show_all(player_hand,dealer_hand)
    
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
            #this scenario is only possible when we play with a soft 17 rule where the dealer stops and we can compare. otherwise the dealer will go until he busts
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
            #they have equal amounts
        else: 
            push(player_hand,dealer_hand)
    
    # Inform Player of their chips total 
    print("Player's total chips are at: {}".format(player_chips.total))
    
    # Ask to play again
    new_game = input("Do you want to play another game? y/n: ")
    
    if new_game[0] == 'y':
        playing = True
        continue
    else:
        print("thank you for playing")
        break 
    
    #NOTE: if you start to play a new game the total of chips will reset to 100 because we are generating a new chip class instant and our default total is 100