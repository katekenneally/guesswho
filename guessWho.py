# -*- coding: utf-8 -*-
# Kate Kenneally and Stephanie Armstrong
# May 8, 2015
# CS 111 Final Project
# guessWho.py

import Tkinter as tk
import random
import animation # Modified one line in animation so that image id is not required
import photoslide # Taken from Lab 11

class App(tk.Frame): # Creates GUI and contains game
    
    def __init__(self, root):
        
        # Variables, etc. for App
        tk.Frame.__init__(self)
        root.title('Guess Who?') # Title
        self.color = 'SteelBlue2' # background color
        self.configure(bg=self.color)
        self.grid()
        self.totalNumberOfImages = 9
        self.answerIndex = tk.IntVar()
        self.default = 'hogwarts.gif' # Default picture at beginning of game
        self.iLabels = [] # Blank image label list
        self.radios = [] # Blank radio button list
        self.symbols = [] # Blank list for animation
        
        # Code for animation canvas
        self.canvas = animation.AnimationCanvas(self, width=575, height=75, 
            bd=0, highlightthickness=0)
        self.canvas.config(bg=self.color)
        self.canvas.place(x=0,y=615)
        
        # For loops to append image labels and radiobuttons to respective lists
        # This sets up the game's cards in rows of 3 when the app launches
        for card in range(3):
            pic = tk.PhotoImage(file=self.default)
            self.iLabels.append(tk.Label(self,image=pic,bg=self.color))   
            self.iLabels[card].pic = pic
            self.iLabels[card].grid(row=2,column=1+(card),sticky=tk.N+tk.E+tk.W+tk.S)
            self.newButton = tk.Radiobutton(self,bg=self.color,
                variable=self.answerIndex,value=card)
            self.radios.append(self.newButton)
            self.newButton.grid(row=3,column=1+(card))
        for card in range(3):
            pic = tk.PhotoImage(file=self.default)
            self.iLabels.append(tk.Label(self,image=pic,bg=self.color))   
            self.iLabels[card+3].pic = pic
            self.iLabels[card+3].grid(row=4,column=1+(card),sticky=tk.N+tk.E+tk.W+tk.S)
            self.newButton = tk.Radiobutton(self,bg=self.color,
                variable=self.answerIndex,value=card+3)
            self.radios.append(self.newButton)
            self.newButton.grid(row=5,column=1+(card))
        for card in range(3):
            pic = tk.PhotoImage(file=self.default)
            self.iLabels.append(tk.Label(self,image=pic,bg=self.color))   
            self.iLabels[card+6].pic = pic
            self.iLabels[card+6].grid(row=6,column=1+(card),sticky=tk.N+tk.E+tk.W+tk.S)
            self.newButton = tk.Radiobutton(self,bg=self.color,
                variable=self.answerIndex,value=card+6)
            self.radios.append(self.newButton)
            self.newButton.grid(row=7,column=1+(card))
        
        # Image label for computer's card 
        self.questionpic = tk.PhotoImage(file='question.gif')
        self.cpuImage = tk.Label(self,image=self.questionpic,bg=self.color)
        self.cpuImage.pic = self.questionpic
        self.cpuImage.grid(row=6,column=4)
            
        # Hint labels
        self.hint1 = tk.StringVar()
        self.hint1Label = tk.Label(self,textvariable=self.hint1,bg=self.color,width=60)
        self.hint1Label.grid(row=1,column=4)
        self.hint1.set('???')
        self.hint2 = tk.StringVar()
        self.hint2Label = tk.Label(self,textvariable=self.hint2,bg=self.color,width=60)
        self.hint2Label.grid(row=2,column=4)
        self.hint2.set('???')
        self.hint3 = tk.StringVar()
        self.hint3Label = tk.Label(self,textvariable=self.hint3,bg=self.color,width=60)
        self.hint3Label.grid(row=3,column=4)
        self.hint3.set('???')
        self.hint4 = tk.StringVar()
        self.hint4Label = tk.Label(self,textvariable=self.hint4,bg=self.color,width=60)
        self.hint4Label.grid(row=4,column=4)
        self.hint4.set('???')
        self.hint5 = tk.StringVar()
        self.hint5Label = tk.Label(self,textvariable=self.hint5,bg=self.color,width=60)
        self.hint5Label.grid(row=5,column=4)
        self.hint5.set('???')
        
        # Title label that will change to display win/lose message
        self.titleLabel = tk.Label(self,text='Guess Who?',font='System 30 bold',
            fg='white',bg=self.color,width=10)
        self.titleLabel.grid(row=0,column=2,sticky=tk.N+tk.E+tk.W+tk.S)
        
        # Start button calls startGame in order to play game
        self.startButton = tk.Button(self,text='Start',command=self.startGame)
        self.startButton.grid(row=7,column=4)
        
        # Hint button calls onHintButtonClick to reveal up to 5 hints
        self.hintButton = tk.Button(self,text='Hint',state='disabled',
            command=self.onHintButtonClick)
        self.hintButton.grid(row=8,column=4)
        
        # Submit button calls checkAnswer to submit user's response
        self.submitButton = tk.Button(self,text='Submit',command=self.checkAnswer
            ,state='disabled')
        self.submitButton.grid(row=9,column=4)
        
        # Quit button calls onQuitButtonClick to exit game at any time
        self.quitButton = tk.Button(self,text='Quit',command=self.onQuitButtonClick)
        self.quitButton.grid(row=10,column=4)
        
    def startGame(self):
        
        self.end_animation() # Ends any existing animation
        
        self.hintButton.config(state='normal') # Enables hint button
        self.submitButton.config(state='normal') # and submit button
        
        self.imagelist = [] # Creates empty character image file list
        self.charlist = [] # Creates empty character name list
        charcount = 0 # Sets character count to 0
        self.hintcount = 0 # Sets hint count to 0
        
        # Resetting computer's card to question mark    
        self.cpuImage.configure(image=self.questionpic)
        self.cpuImage.image = self.questionpic
        
        # Resetting title label
        self.titleLabel.config(text = 'Guess Who?')
        
        # Resetting hint labels
        self.hint1.set('???')
        self.hint2.set('???')
        self.hint3.set('???')
        self.hint4.set('???')
        self.hint5.set('???')
        
        # Generates list of 9 random characters from Harry Potter class
        while charcount < 9:
            person = peopleHP[random.randint(0,len(peopleHP)-1)]
            link = person.getImage()
            if link not in self.imagelist:
                self.charlist.append(person)
                self.imagelist.append(link)
                charcount = charcount + 1
            else:
                charcount = charcount
                
        # Randomly chooses a card from charlist to be the computer's card
        self.cpuCard = self.charlist[random.randint(0,len(self.charlist)-1)]
         
        # Changes image labels and radio button text to correspond with chosen characters
        for card in range(3):
            pic = tk.PhotoImage(file=self.imagelist[card])   
            self.iLabels[card].configure(image=pic)
            self.iLabels[card].image = pic
            self.radios[card].configure(text=self.charlist[card].getName())
            self.newButton.deselect()
        for card in range(3):
            pic = tk.PhotoImage(file=self.imagelist[card+3])
            self.iLabels[card+3].configure(image=pic)
            self.iLabels[card+3].image = pic
            self.radios[card+3].configure(text=self.charlist[card+3].getName())
            self.newButton.deselect()
        for card in range(3):
            pic = tk.PhotoImage(file=self.imagelist[card+6])
            self.iLabels[card+6].configure(image=pic)
            self.iLabels[card+6].image = pic
            self.radios[card+6].configure(text=self.charlist[card+6].getName())
            self.newButton.deselect()
    # Gets hints from hint list for computer's card (up to 5)   
    def onHintButtonClick(self):
        if self.hintcount == 0:
            self.hint1.set(self.cpuCard.getHint(0))
            self.hintcount = 1
        elif self.hintcount == 1:
            self.hint2.set(self.cpuCard.getHint(1))
            self.hintcount = 2
        elif self.hintcount == 2:
            self.hint3.set(self.cpuCard.getHint(2))
            self.hintcount = 3          
        elif self.hintcount == 3:
            self.hint4.set(self.cpuCard.getHint(3))
            self.hintcount = 4
        elif self.hintcount == 4:
            self.hint5.set(self.cpuCard.getHint(4))
            self.hintcount = 5
            self.hintButton.config(state='disabled')
            
    def start_animation(self,img,r,d):
    # r is the number of images that will appear on the screen
    # d is an extra length down for the losing animation
        # For loop to create multiple images
        for i in range(r):
            oneImage = photoslide.PhotoSlide(self.canvas,img,0+i*10,0+d+i*10)
            self.symbols.append(oneImage) # Append to list for easy removal
            self.canvas.addItem(oneImage)
        self.canvas.start()
        
    def end_animation(self):
        # Removes animated images from canvas
        self.canvas.stop()
        for b in self.symbols:
            self.canvas.removeItem(b)
        self.symbols = [] # Resets list of symbols
            
    def checkAnswer(self):
        try:
            # Gets user's response index
            x = self.answerIndex.get()
            # Gets name of character from index number
            response = self.charlist[x].getName()
            # Compares user's response to cpuCard
            if response == self.cpuCard.getName():
                # Winning animation
                self.start_animation('win.gif',10,0)
                self.titleLabel.config(text = 'Congrats!')
            else:
                # Losing animation
                self.start_animation('lose.gif',1,40)
                self.titleLabel.config(text = 'Game Over!')
            # Reveals computer's card
            pic = tk.PhotoImage(file=self.cpuCard.getImage())
            self.cpuImage.configure(image=pic)
            self.cpuImage.image = pic
            # Disable hint and submit buttons
            self.hintButton.config(state='disabled')
            self.submitButton.config(state='disabled')
        # Error handling
        except ValueError:
            self.titleLabel.config(text = 'Make a guess!')
            
    def onQuitButtonClick(self):
            root.destroy()
    
class HarryPotter():
    
    # Each character gets  a hintlist, image, and name
    def __init__(self,hintlist,image,name):  
        self.hintlist = hintlist
        self.image = image
        self.name = name
         
    def getHint(self,num):
        return self.hintlist[num]
        
    def getImage(self):
        return self.image
        
    def getName(self):
        return self.name

# Variables for HarryPotter characters        
Bellatrix = HarryPotter(['Quote: "I was and am the Dark Lord\'s most loyal servant."','Killed by Molly Weasley','Killed Sirius Black','Narcissa and Andromeda\'s older sister','...Just disgustingly evil.'],'hp/bellatrix.gif','Bellatrix Lestrange')
Cedric = HarryPotter(['Gray eyes','Saved Harry from a giant spider','Killed by Wormtail','Hufflepuff','Edward Cullen'],'hp/cedric.gif','Cedric Diggory')
Cho = HarryPotter(['Member of Dumbledore\'s Army','Ravenclaw Seeker','Besties with Marietta Edgecomb','Harry\'s first crush','Bubble-head charm saved her from the Great Lake'],'hp/cho.gif','Cho Chang')
Dobby = HarryPotter(['Warned Harry about the Chamber of Secrets','Fatally wounded by Bellatrix Lestrange\'s knife','Unintentionally freed by Lucius Malfoy','Brave and loyal','House-elf'],'hp/dobby.gif','Dobby')
Draco = HarryPotter(['Quote: "Longbottom, if brains were gold, you\'d be poorer than Weasley."','Became a Death Eater at 16','Prefect','Tasked with killing Albus Dumbledore','Son of Lucius and Narcissa'],'hp/draco.gif','Draco Malfoy')
Dumbledore = HarryPotter(['Ate an earwax-flavored Bernie Bott\'s Every Flavor Bean','Discovered the twelve uses of dragon\'s blood','Founded the first and second Order of the Phoenix','Quote:"It does not do to dwell on dreams and forget to live."','Headmaster of Hogwarts'],'hp/dumbledore.gif','Albus Dumbledore')
Fleur = HarryPotter(['Wand contains Rosewood','One-quarter Veela blood','Middle name Isabelle','Nicknamed "Phlegm" by Ginny','Marries Bill Weasley'],'hp/fleur.gif','Fleur Delacour')
FredGeorge = HarryPotter(['Left Hogwarts in order to rebel against Umbridge\'s tyranny','Quote: "Give her hell from us, Peeves."','Founded Weasleys\' Wizard Wheezes','Beaters','Twins'],'hp/fredgeorge.gif','Fred & George Weasley')
Ginny = HarryPotter(['First best friend was Tom Riddle','Becomes professional Quidditch player for Holyhead Harpies','Forced to re-open the Chamber of Secrets','Marries Harry Potter','Youngest Weasley'],'hp/ginny.gif','Ginny Weasley')
Hagrid = HarryPotter(['Framed by Tom Riddle for the crime of opening the Chamber of Secrets','Taught Care of Magical Creatures','Gamekeeper of Hogwarts','Tasked with reintroducing Harry to the Wizarding World','Half-Giant Wizard'],'hp/hagrid.gif','Rubeus Hagrid')
Harry = HarryPotter(['Gryffindor','Wand has a phoenix-feather core','Boggart: Dementor','Birthday: July 31','The Boy Who Lived'],'hp/harry.gif','Harry Potter')
Hermione = HarryPotter(['Gifted a Time-Turner by the Ministry of Magic','Formed the association S.P.E.W.','Brewed Polyjuice Potion during second year at Hogwarts','Parents are muggle dentists','Quote: "We could all have been killed - or worse, expelled."'],'hp/hermione.gif','Hermione Granger')
James = HarryPotter(['One of the four Marauders','Prongs','"An arrogant toerag"','Buried in Godric\'s Hollow','Passed on Invisibility Cloak to Harry'],'hp/james.gif','James Potter')
Lily = HarryPotter(['Member of the Slug Club','Born to Muggle parents','Friends with Snape at Hogwarts','Quote: "Not Harry, please no, take me, kill me instead-"','Harry has her eyes'],'hp/lily.gif','Lily Evans')
Lockhart = HarryPotter(['Favorite color is lilac','Invented an Occamy egg yolk shampoo','Quote: "Celebrity is as celebrity does"','Five-time winner of Witch Weekly\'s Most Charming Smile Award','Books include "Gaddling with Ghouls" and "Who Am I?"'],'hp/lockhart.gif','Gilderoy Lockhart')
Luna = HarryPotter(['Member of Dumbledore\'s Army','Noticed Thestrals on first day at Hogwarts','Patronus: Hare','Daughter of Xenophilius and Pandora','Nickname: Loony'],'hp/luna.gif','Luna Lovegood')
Lupin = HarryPotter(['One of the four Marauders','Moony','Half-blood wizard','Married to Nymphadora Tonks','Harry\'s third Defense Against the Dark Arts teacher'],'hp/lupin.gif','Remus Lupin')
McGonagall = HarryPotter(['Quote: "Man the boundaries, protect us, do your duty to our school!"','Fought at the Battle of Hogwarts','Particularly talented at Transfiguration','Head of Gryffindor House','Becomes Headmistress of Hogwarts'],'hp/mcgonagall.gif','Minerva McGonagall')
Moody = HarryPotter(['Quote: "Never got round to much teaching, did I?"','Auror','Kidnapped by Barty Crouch Jr.','Overly cautious and paranoid','Magical eye'],'hp/moody.gif','Mad-Eye Moody')
Neville = HarryPotter(['Quote: "You and whose army?"','Raised by grandmother','Becomes Professor of Herbology','Lost toad named Trevor on the way to Hogwarts','Destroyed the 7th Horcrux'],'hp/neville.gif','Neville Longbottom')
Pettigrew = HarryPotter(['One of the four Marauders','Wormtail','Strangled to death','Played a key role in Voldemort\'s return','Also know as Scabbers'],'hp/pettigrew.gif','Peter Pettigrew')
Quirrell = HarryPotter(['Ravenclaw','Half-blood wizard','Died while trying to kill Harry','Quote: "Troll - in the dungeons - thought you ought to know."','Harry\'s first Defense Against the Dark Arts teacher'],'hp/quirrell.gif','Quirinus Quirrell')
Riddle = HarryPotter(['Raised by muggles','Speaks Parseltongue','Heir of Slytherin','Opened the Chamber of Secrets','Died at the Battle of Hogwarts'],'hp/riddle.gif','Tom Riddle')
Ron = HarryPotter(['Children: Rose and Hugo','Keeper','Pure-blood','Gryffindor','Best friends with Harry Potter'],'hp/ron.gif','Ron Weasley')
Sirius = HarryPotter(['One of the four Marauders','Padfoot','Only known person to escape Azkaban','Harry Potter\'s godfather','Heir to the House of Black'],'hp/sirius.gif','Sirius Black')
Snape = HarryPotter(['"The bravest man" Harry ever knew','Slytherin','The half-blood prince','In love with Lily Evans','Potions professor'],'hp/snape.gif','Severus Snape')
Sprout = HarryPotter(['Brewed Mandrake Restorative Draught','Attended Memorial Feast in Cedric’s memory','Advocated to keep school open after Dumbledore’s death','Head of Hufflepuff House','Herbology professor'],'hp/sprout.gif','Pomona Sprout')
Trelawney = HarryPotter(['Great-great granddaughter of Cassandra','Almost banished by Umbridge','Made a prophecy concerning Voldemort','Seer','Divination professor'],'hp/trelawney.gif','Sybill Trelawney')
Umbridge = HarryPotter(['Slytherin','Ran Muggle-Born Registration Commission','Toad','Harry\'s fifth Defense Against the Dark Arts teacher','Fond of cruel and unusual punishment and the color pink'],'hp/umbridge.gif','Dolores Umbridge')
Viktor = HarryPotter(['Seeker','Boggart: Voldemort','Confronted by the symbol of the Deathly Hallows','Once Ron\'s favorite Quidditch player','Durmstrang Institute'],'hp/viktor.gif','Viktor Krum')
Voldemort = HarryPotter(['Quote: "There is nothing worse than death, Dumbledore!"','Soul is split into eight pieces','Leader of the Death Eaters','Symbol: The Dark Mark','He-Who-Must-Not-Be-Named'],'hp/voldemort.gif','Voldemort')

# List of variables for easy access
peopleHP = [Bellatrix,Cedric,Cho,Dobby,Draco,Dumbledore,Fleur,
    FredGeorge,Ginny,Hagrid,Harry,Hermione,Hermione,James,
    Lily,Lockhart,Lupin,McGonagall,Moody,Neville,Pettigrew,Quirrell,
    Riddle,Ron,Sirius,Snape,Sprout,Trelawney,Umbridge,Viktor,Voldemort]

root = tk.Tk()
app = App(root)
root.mainloop()