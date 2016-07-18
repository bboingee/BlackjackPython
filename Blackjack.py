# Blackjack Game
import random
ranks = ['2','3','4','5','6','7','8','9','Ten','Jack','Queen','King','Ace']
suits = ['Clubs','Spades','Diamonds','Hearts']
deck = []
playerhand = []
dealerhand = []
playermoney = 1000

def debtinput(promptText):
    global playermoney
    while True:
        try:
            inputText = int(input(promptText))
            if inputText > playermoney:
                raise FileNotFoundError
            return inputText
        except FileNotFoundError:
            print("You don't have that much money!")
        except ValueError:
            print("Enter a number.")

def refreshdeck():
    global deck
    deck = []
    global ranks
    global suits
    for a in ranks:
        for b in suits:
            deck.append(a + ' of ' + b)
    random.shuffle(deck)
    return None

def deal(hand, number = 1):
    for i in range(number):
        hand.append(deck.pop())
    return None

def ifblackjack(hand):
    if ("Ace" in hand[0] or "Ace" in hand[1]) and (hand[1][0] in "JQKT" or hand[0][0] in "JQKT"):
        return True
    else:
        return False

def handvalue(hand):
    pointvalue = 0
    for card in hand:
        if card[0] in "JQKT":
            pointvalue += 10
        elif card[0] in "23456789":
            pointvalue += int(card[0])
    for card in hand:
        if card[0] == "A":
            if (pointvalue + 11) > 21:
                pointvalue += 1
            else:
                pointvalue += 11
    return pointvalue

def turnloop():
    global playerhand
    global dealerhand
    victory = [""] # will be formatted [player who won],[type of win] / P = player, D = dealer, U = push / P = payout, B = blackjack, S = split, I = insurance, ...
    #
    playerhand = []
    dealerhand = []
    deal(playerhand,2)
    deal(dealerhand,2)
    print(dealerhand[0])
    print(playerhand)    
    # insurance check
    if "Ace" in dealerhand[0]:
        ins = input("Insure? Y/N ")
        if ins == "Y" or ins == "y":
            victory.append("Insurance")
    # blackjack check
    if ifblackjack(dealerhand) or ifblackjack(playerhand):
        victory.append("Blackjack")
        if handvalue(dealerhand) > handvalue(playerhand):
            victory[0] = "D"
            return victory
        elif handvalue(dealerhand) == handvalue(playerhand):
            victory[0] = "U"
            return victory
        else:
            victory[0] = "P"
            return victory
    # splitting check
    # double down
    dbl = "N"
    if 11 >= handvalue(playerhand) >= 9:
        dbl = input("Double down? Y/N ")
    if (dbl == "Y" or dbl == "y"):
        victory.append("Double")
    # player turn
    plchoice = input("Hit (H) or Stay (S)? ")
    while plchoice[0] == "H" or plchoice[0] == "h":
        deal(playerhand)
        print(playerhand)
        if handvalue(playerhand) > 21:
            print("Bust!")
            victory.append("Bust")
            victory[0] = "D"
            return victory
        else:
            plchoice = input("Hit (H) or Stay (S)? ")
    # dealer turn
    while handvalue(dealerhand) < 17:
            deal(dealerhand)
            if handvalue(dealerhand) > 21:
                print("Dealer busts!")
                victory[0] = "P"
                victory.append("Bust")
                return victory
    # No bust, no blackjack, so just compare
    if handvalue(dealerhand) > handvalue(playerhand):
        victory[0] = "D"
        return victory
    elif handvalue(dealerhand) == handvalue(playerhand):
        victory[0] = "U"
        return victory
    else:
        victory[0] = "P"
        return victory
    return ["What the hell happened?"]

def bethandler(victory, bet):
    payout = 0
    if "Double" in victory:
        bet = bet*2
    if "Surrender" in victory:
        return -bet/2
    if "Insurance" in victory:
        payout -= bet
    if victory[0] == "D":
        payout -= bet
        if "Blackjack" and "Insurance" in victory:
            return 0
    elif victory[0] == "P":
        payout += bet
        if "Blackjack" in victory:
            payout += bet/2
    else:
        payout += 0
    return payout

def main():
    global playermoney
    global playerhand
    global dealerhand
    while playermoney > 0 and playermoney < 10000:
        refreshdeck()
        bet = debtinput("How much will you bet? ")
        turnvic = turnloop()
        print(turnvic)
        print(dealerhand)
        print(playerhand)
        playermoney += bethandler(turnvic,bet)
        print(playermoney)
    if playermoney <= 0:
        print("You lose!")
    else:
        print("You won!")
    return None

main ()