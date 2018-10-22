import random
    
suits = {'Hearts', 'Diamonds', 'Spades' , 'Clubs'}
ranks ={'Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace'}
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,'King':10, 'Queen':10, 'Ace':11}
class Chips():
    def __init__(self):
        self.chips_value = 0;

    def won_bet(self, amount):
        self.chips_value += amount

    def lost_bet(self, amount):
        if self.chips_value >= amount:
            self.chips_value -= amount
            return True
        else:
            return False
    def __str__(self):
        return 'You have '+ str(self.chips_value)

class Card():
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return self.rank +' of '+self.suit

    def value(self):
        return values[self.rank]
    
class Deck():
    def __init__(self):
        self.cards = []
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))
    def print_deck(self):
        for card in self.cards:
            print(card)
    def shuffle_deck(self):
        random.shuffle(self.cards)

    def __len__(self):
        return len(self.cards)

    def deal(self):
        poped_card = self.cards.pop()
        return poped_card

class Player():
    def __init__(self, name):
        self.cards = []
        self.name = name

    def sum(self):
        ace_cards = list(card for card in self.cards if card.rank == 'Ace')
        other_cards = list(card for card in self.cards if card.rank != 'Ace')
        sum_of_cards = 0
        sum_of_cards = sum(list(card.value() for card in other_cards))
        for ace in ace_cards:
            card_value = 1
            if ace.value() + sum_of_cards <= 21:
                card_value = ace.value()
            sum_of_cards += card_value
        return sum_of_cards

    def hit(self, card):
        self.cards.append(card)

def who_is_next(current_player):
    if current_player == 0:
        return 1
    elif  current_player == 1:
        return 0

def calculate_credit(won, current_player, chips_available, bet_amount):
    if (won == True and current_player == 0) or (won == False and current_player == 1):
        chips_available.won_bet(bet_amount)
    elif (won == False and current_player == 0) or (won == True and current_player == 1):
        chips_available.lost_bet(bet_amount)
    print(f"You have {chips_available.chips_value}")
                

def hit_deal(player, current_player, chips_available, bet_amount, card_face_down=False):
    #Hit
    card_from_deck = deck.deal()
    player.hit(card_from_deck)
    result = player.sum()
    for (index, card_from_player_hand) in enumerate(player.cards):
        if card_face_down and current_player == 1 and index == 1:
            print(f'\t face down')
        else:
            print(f'\t {card_from_player_hand}')
    print("\n")
    game_end = False
    if result > 21:
        next_player = players[who_is_next(current_player)]
        print(f'{player.name} BUST!!!')
        won = False
        game_end = True
    elif result == 21:
        print(f'{player.name} WON. BLACK JACK!!!     ')
        won = True
        game_end = True
    else:
        next_player = players[who_is_next(current_player)]
        if card_face_down == False and player.sum() > next_player.sum():
            print(f'{player.name} WON!!!')
            won = True
            game_end = True
    if game_end == True:
        calculate_credit(won, current_player, chips_available, bet_amount)
        return True
        
def get_bet_amount(chips_value):
    while True:
        try:
               bet_amount = int(input('Bet chips: '))
               if bet_amount <= chips_value:
                   return bet_amount
               else:
                   print(f'Amount exceeded the chips_value. Enter {chips_available.chips_value} or below ')
                   return 0
        except:
            print('Amount was not valid. Enter again')
chips_available = Chips()
chips_available.chips_value = 1000
while True:
    print("WELCOME TO BLACK JACK")
    if chips_available.chips_value <= 0:
        print("Ooops!!! Out of chips_value")
        break    
    bet_amount = get_bet_amount(chips_available.chips_value)

    if bet_amount > 0:
        print("\n")
        print("***************************************************************************")
        print("                                                                           ")
        print("                                 DEAL                                      ")
        print("                                                                           ")
        print("***************************************************************************")
        print("\n")
        
        deck = Deck()
        deck.shuffle_deck()
        human_player = Player('Human Player')
        computer_player = Player('Computer Dealer')
        players = (human_player, computer_player)
        game_on = True
        current_player = 0
        card_face_down = True
        for init_card_count in range(0,4):
            player = players[current_player]
            print(f"{player.name}'s TURN: ")
            print("-----------------------")
            game_on = not hit_deal(player, current_player, chips_available, bet_amount, card_face_down)
            if game_on == True:
                current_player = who_is_next(current_player)
                next_player = players[current_player]
            else:
                break
            
        if game_on == True:        
            while True:
                player = players[current_player]
                print(f"{player.name}'s TURN: ")
                print("-----------------------")
                if current_player == 1:
                    face_down = False
                    game_on = not hit_deal(player, current_player, chips_available, bet_amount,card_face_down)
                else:
                    decide = input("Choose 'H' or 'S': ")
                    if decide.upper() == 'H':
                        game_on = not hit_deal(player, current_player, chips_available, bet_amount,card_face_down)
                    else:
                        card_face_down = False
                        current_player = who_is_next(current_player)
                if game_on != True:
                    break
        if game_on == False:
            if chips_available.chips_value <= 0:
                print("Ooops!!! Out of chips_value")
                break
            else:
                decide = input("Do you want to play again? 'Y' or 'N'")
                if decide.upper() == 'N':
                    break
                
