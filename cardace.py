from random import shuffle

class acecard():
    def __init__(self,cards):
        self.cards = cards

    def player(self):
        numberofplayer = int(input("number of players "))
        players = []
        print("enter your players name")
        for x in range(numberofplayer):
            pname = input()
            players.append(pname)
        return players
    def shufflecard(self, players):
        x = int(len(self.cards)/len(players))
        shuffle(self.cards)
        list_oflist = [self.cards[i:i+x] for i in range(0, len(self.cards), x)]
        balancecard = 52 - ((len(players)) * len(list_oflist[0]))
        if balancecard != 0:
            a = self.cards[- balancecard:]
            for i in range(len(a)):
                list_oflist[i].append(a[i])
        return list_oflist

def mainmenu():
    print("welcom to ace game....")
    print("1. Ace")
    print("2. Exit")
    nchoose = int(input("choose you'r number"))

    if nchoose == 1:
        print(nchoose)
    elif nchoose == 2:
        exit()
    else:
        print("choose the wrong number")

def  cardlist():
    cardslist = []
    cnamelist = ["ACE","SPIDE","HEART","DIMOND"]
    for i in cnamelist:
        for x in range(2,15):
            if x <= 10:
                cardslist.append(i + " " + str(x))
            elif x == 11:
                cardslist.append(i + " J")
            elif x == 12:
                cardslist.append(i + " Q")
            elif x == 13:
                cardslist.append(i + " K")
            else:
                cardslist.append(i + " A")

    return cardslist

def cardselect(card, d):
    for i in range(len(card)):
        if card[i].find(d) == False:
            print(i, card[i])
        elif d == ' ':
            print(i, card[i])
    indexselect = input("select your card index ")
    return indexselect

def gameplay(players, list_card):
    #while(len(players) == 1):
    rollcard = []
    d = ' '
    for i in range(5):
        print(players[0] + " chance")
        selectedcard = int(cardselect(list_card[0], d))
        rollcard.append(list_card[0][selectedcard])
        a = list_card[0].pop(selectedcard)
        d = str(rollcard[0].split(' ')[0])
        print(a)
        print(d)
    print(rollcard)

def main():
    # mainmenu()
    cards = cardlist()
    game = acecard(cards)
    # players = game.player()
    players = ["sha", "bir", "ali"]
    list_ofcard = game.shufflecard(players)
    gameplay(players,list_ofcard)

if __name__ == "__main__":
    main()