from random import randint ## importing randint function from random package/library
from os import system, name
from functools import reduce

WhichPlayer = 1 ## variable

class Players(): ## class

    def __init__(self, name): ## constructor to initialize Player object. Based on the number of players, that many times this will be called 
        self.name = name ## name property of player object
        self.balance = 100 ## balance property of player object
        self.vowels = 0 ## vowel property of player object
        
    def UpdateBalance(self, num): ## function to update player balance during play
        self.balance += num

    def __str__(self): ## function to display balance
        return self.name + ' with balance of Rs.' + str(self.balance)

def ResetVowelCount(): ## To reset the vowels guessed by all the players
    for i in range(noOfPlayers):
        PlayerList[i].vowels = 0

def DisplayPlayers(): ## To display all the players
    
    for i in range(noOfPlayers):
        print(PlayerList[i])

def NextPlayer(): ## To set which player is playing currently in global variables
    global WhichPlayer
    global noOfPlayers
    if WhichPlayer == noOfPlayers: ## To check if the current player is the last player.
        WhichPlayer = 1 ## if all players played in one cycle then change the current player to th first player
    else:
        WhichPlayer += 1 ## otherwise keep increasing the current player number

def GenerateNextItem(): ## randomly find next phrase. If already asked it will be there in myRandNums then find another
    global myRandNums
    global myNum
    global mySentencesList
    while True:
        myNum = randint(1,len(mySentencesList))
        if not myNum in myRandNums:
            myRandNums.append(myNum)
            break

def WriteAskedFile(): ##Code to write in Asked file
    global myRandNums
    with open('Asked.txt','w') as myfile:
        myfile.write (reduce(lambda x,y: str(x) + ',' + str(y), myRandNums)) ## Need to study reduce function
##Main code starts here --
with open('WheelOfFortune.txt') as myfile: ## opening the text file and and reading all the contents splitting by new line character (\n)
    mySentencesList = (myfile.read()).split('\n')

noOfPlayers = int(input('Enter number of players: ')) ## asking user how many players are playing

PlayerList = [x for x in range(noOfPlayers)] ## List of players. For ex (1,2,3). This code is called as List Comprehension

for i in range(noOfPlayers): ## based on number of players ask the name that many times
    PlayerName = (input(f'Enter name of Player {i+1}: ')).upper()
    PlayerList[i] = Players(PlayerName) ## Creating and initializing the Player object by calling the Player class 

DisplayPlayers() ## Calling the function 

myVowels = ['A','E','I','O','U'] ## Vowel List
with open('Asked.txt') as myfile: ## Opening the Asked file and checking
    myRandNums = myfile.read() ## reading file into a variable
    if len(myRandNums) == 0: ## if contents are zero then creating the list with the same name
        myRandNums = []
    else:
        myRandNums = myRandNums.split(',') ##otherwise creating list splitting using comma as delimiter
        myRandNums = [int(a) for a in myRandNums] ## converting the numbers from text file to integer and creating the list using List Compre
    
GenerateNextItem() ## function call

mySentenceList = [x for x in mySentencesList[myNum-1]] ## making list character by character for the identified phrase

myBlankList = ['_' if x != ' ' else '   ' for x in mySentencesList[myNum-1]] ##creating actual question which is on screen

myGuessList = []

print(' '.join(myBlankList)) ##printing actual question with dashes

countAffected = 0

while True: ## Infinite while loop
    print('\n')
    userInput = (input(f'{PlayerList[WhichPlayer-1].name}, please enter an alphabet OR "$" to guess the whole sentence: ')).upper()
    if userInput == '!': ## If user inputs !
        _ = system('cls')
        print(f'{mySentencesList[myNum-1]}')
        if input('Play again ? (y/n): ') == 'n':
            WriteAskedFile()
            DisplayPlayers()
            break
        
        else:
            myGuessList = []
            GenerateNextItem()
            mySentenceList = [x for x in mySentencesList[myNum-1]]
            myBlankList = ['_' if x != ' ' else '          ' for x in mySentencesList[myNum-1]]
            ResetVowelCount()
            WhichPlayer = 1
            DisplayPlayers()
            print('\n')
            print(' '.join(myBlankList))
            continue
    
    elif userInput == '$': ## If user inputs $
        mySentence = (input('Please guess the sentence: ')).upper()
        if mySentence == mySentencesList[myNum-1]: ## Whether sentenced guessed is the correct sentence
            print(f'{PlayerList[WhichPlayer-1].name}, you guessed correctly. {mySentencesList[myNum-1]}. You won Rs.100')
            PlayerList[WhichPlayer-1].UpdateBalance(100) ## Winning for guessing correct phrase
            if input('Play again ? (y/n): ') == 'n':
                DisplayPlayers()
                WriteAskedFile()
                break
            
            else:
                myGuessList = [] ## If yes
                GenerateNextItem() ## Identify Next Sentence randomly
                mySentenceList = [x for x in mySentencesList[myNum-1]]
                myBlankList = ['_' if x != ' ' else '          ' for x in mySentencesList[myNum-1]]
                ResetVowelCount()
                DisplayPlayers()
                print('\n')
                print(' '.join(myBlankList))
                continue
            
        else:
            PlayerList[WhichPlayer-1].UpdateBalance(-50) ## Panelty for guessing wrong phrase
            print(f'{PlayerList[WhichPlayer-1].name}, wrong guess !! Panelty = Rs.50 (balance = Rs.{PlayerList[WhichPlayer-1].balance})')
            NextPlayer()
            continue
    
    elif userInput in myVowels: ## If user has choosen vowel
        _ = system('cls')
        PlayerList[WhichPlayer-1].UpdateBalance(-20 * (PlayerList[WhichPlayer-1].vowels + 1)) 
        print(f'{PlayerList[WhichPlayer-1].name}, choosing a vowels costed you Rs.{20 * (PlayerList[WhichPlayer-1].vowels + 1)} (balance = Rs.{PlayerList[WhichPlayer-1].balance})')
        PlayerList[WhichPlayer-1].vowels += 1
        
    if userInput in mySentenceList:
        if userInput not in myGuessList:
            myGuessList.append(userInput)
            myGuessList.sort()
        else:
            print(f'{PlayerList[WhichPlayer-1].name}, "{userInput}" has already been guessed.')
            print('\n')
            print(' '.join(myBlankList))
            continue
            
        for index, x in enumerate(mySentenceList):
            if x == userInput:
                myBlankList[index] = userInput
                countAffected += 1
        print(f'{PlayerList[WhichPlayer-1].name}, {countAffected} occurance(s) of "{userInput}"')
        if userInput not in myVowels:
            PlayerList[WhichPlayer-1].UpdateBalance(10*countAffected)
            print(f'{PlayerList[WhichPlayer-1].name}, you have been awarded Rs.{10*countAffected}(balance = Rs.{PlayerList[WhichPlayer-1].balance})')
        countAffected=0
        print(f'Alphabets already guessed: {", ".join(myGuessList)}')
        print('\n')
        print(' '.join(myBlankList))

    else:
        _ = system('cls')
        if userInput not in myGuessList:
            myGuessList.append(userInput)
            myGuessList.sort()
        else:
            print(f'{PlayerList[WhichPlayer-1].name}, "{userInput}" has already been guessed.')
            print('\n')
            print(' '.join(myBlankList))
            continue
            
        PlayerList[WhichPlayer-1].UpdateBalance(-20)
        print(f'{PlayerList[WhichPlayer-1].name}, "{userInput}" is not in the sentence. Panelty = Rs.20(balance = Rs.{PlayerList[WhichPlayer-1].balance})')
        print(f'Alphabets already guessed: {", ".join(myGuessList)}')
        print('\n')
        print(' '.join(myBlankList))
        NextPlayer()

    if '_' not in myBlankList:
        print(f'You guessed it correctly: {mySentencesList[myNum-1]}')
        PlayerList[WhichPlayer-1].UpdateBalance(100)
        if input('Play again ? (y/n): ') == 'n':
            DisplayPlayers()
            WriteAskedFile()
            break
        else:
            myGuessList = []
            GenerateNextItem()
            mySentenceList = [x for x in mySentencesList[myNum-1]]
            myBlankList = ['_' if x != ' ' else '          ' for x in mySentencesList[myNum-1]]
            ResetVowelCount()
            DisplayPlayers()
            print('\n')
            print(' '.join(myBlankList))
exitGame = input('Exit ? (y/n): ')
