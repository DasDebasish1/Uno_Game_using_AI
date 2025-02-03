import pygame
from random import shuffle,randint,choice
import math
from helper import *

colors = ["Red", "Blue", "Green", "Yellow"]
specialCards = ["Skip", "Reverse", "Draw"]
wildCards    = ["Wild_Draw", "Wild"]
menu = {
  1: 'start',
  2: 'quit'
}


pygame.init()
screen=pygame.display.set_mode()
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 40)
pygame.mixer.music.load("Assets/Sound/Uno.wav")

class Card:
    """
    A class to represent a card.

    Attributes
    ----------
    position : int, float or tuple of (x,y) coordinates
        A 2-Dimensional Vector
    color : str
        Colour assigned to the card.
    number : int
        Number assigned to the card.
    special: str
        Represents the special action that a card can perform.
    hidden: bool
        Dictates whether a card's face is hidden or not.
    angle: int
        Represents the angle at which the card is rotated.
    moving: bool
        Determines whether a card is moving or not.
    moving_timer:
        A timer for an animation procedure.
    moving_duration:
        The duration for which the card moves (animation).

    Methods
    -------
    move:
        Moves the card.
    load_images:
        Loads the assets (card pngs) onto the cards.
    calculate_rect:
        Calculates the size of the cards with the loaded images.
    canPlayedOn:
        Returns a conditional checking whether a card can be played on a given card.
    draw:
        Draws a card on the given screen.
    set_hidden:
        Hides the card from view.
    rotate:
        Rotates card and updates its image to reflect the rotation.
    update:
        Checks if the card is moving, and returns True or False, otherwise checks if player has clicked a card.
    """
    def __init__(self,position,color="",number="",special="",hidden=False,angle=0):
        self.position=pygame.Vector2(*position)
        self.color=color
        self.number=number
        self.special=special
        self.hidden=hidden
        self.angle=angle
        self.load_image()
        self.moving=False
        self.moving_timer=0
        self.moving_duration=1
    
    def move(self,position):
        self.moving=True
        self.moveTo=pygame.Vector2(*position)
        
        
    
    def load_image(self):
        if not self.hidden:
            path=f"Assets/UoN_Cards/{self.color}_{self.number}.png"
            if self.special:
                if self.special in specialCards:
                    path=f"Assets/UoN_Cards/{self.color}_{self.special}.png"
                else:
                    path=f"Assets/UoN_Cards/{self.special}.png"
        else:
            path="Assets/UoN_Cards/Deck.png"
        image=pygame.image.load(path).convert_alpha()
        if self.angle!=0:
            image = pygame.transform.rotate(image, self.angle)
            
        
        self.image=pygame.transform.smoothscale(image,(image.get_width()/3,image.get_height()/3))
        
        self.calculate_rect()
    
    def calculate_rect(self):
        self.rect=pygame.Rect(self.position,self.image.get_size())
    
    def canPlayedOn(self,card):
        return (self.color==card.color and self.color!="")  or (self.number == card.number and self.number!="") or (self.special== card.special and self.special !="") or self.special in wildCards
    
    def draw(self,screen):
        screen.blit(self.image,self.position)
    
    def set_hidden(self,state):
        self.hidden=state
        self.load_image()
    
    def rotate(self,angle):
        self.angle=angle
        self.load_image()
    
    def update(self,events,dt):
        if self.moving:
            self.position=self.position.lerp(self.moveTo,self.moving_timer)
            self.moving_timer+=dt
            if self.moving_timer>=self.moving_duration:
                self.moving=False
                self.position=self.moveTo
                self.moving_timer=0
                return True
            return False
        else:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(pygame.mouse.get_pos()):
                        print(self.color,self.number,self.special)
                        return True
            return False
        

class Table:
    """
    A class to represent the game Table.

    Attributes
    ----------
    table_bg: pygame.Surface
        Render object of the game background (fit to full_screen).
    players: list
        The players at the table.
    deck: list
        The deck of cards for the game.
    discard_deck: list 
        Stores the discard deck where the played cards are placed.
    discard_deck_position: pygame.Vector2 
        Render object of the position of the discard deck on the screen.
    direction: int
        Determines the direction of play (either 1 or -1).
    turn_index: int
        The index of the player whose turn it is.
    color_state: str
        The current color state of the game.
    state: str
        The current state of the game (e.g. "normal", "transition").
    player_won: Obj 
        The player who won the game, if any.
    won: bool
        Indicates whether the game has been won.
    n: int
        The number of players in the game.
    player_names: list
        A list of computer player names.
    cards: list
        Stores the cards for each player.
    rotation: float
        The rotation of the players around the table.
    points: list
        Determines the points on the screen where the players are positioned.
    number_of_players: int 
        The number of players in the game (excluding yourself).
    
    

    Methods
    -------
    next_turn:
        Advances the game to the next players turn, whilst checking if their hand is empty or not.
    calculate_score:
        Calculates the points present in the players hand.
    add_player:
        Adds a computer player to the table
    initialize_cards:
        Initializes the deck of cards (108 cards).
    draw:
        Draws the cards, deck and discard pile to the screen.
    update:
        Checks the state of the round, and updates according to player action/round status.
    """
    def __init__(self,n) -> None:
        self.table_bg = pygame.transform.smoothscale(pygame.image.load("Assets/Tables/Table_0.png"),screen.get_size())
        self.players=[]
        self.deck=[]
        self.discard_deck=[]
        self.discard_deck_position=pygame.Vector2(screen.get_width()/2.5,screen.get_height()/2.4)
        self.direction=-1
        self.turn_index=0
        self.color_state=""
        self.state="normal"
        self.player_won=None
        self.won=None
        self.initialize_cards()
        self.n=n
        cards=[]
        self.player_names=["Max","John","Steve","Paul","Bruce","Ron"]
        shuffle(self.player_names)
        for i in range(7):
            cards.append(self.deck.pop(0))
        self.players.append(Human(0,"You",(screen.get_width()/2,screen.get_height()-screen.get_height()/4),cards,self))
        number_of_players=n-1
        rotation=math.radians(360/(number_of_players+1))
        points=polygon(number_of_players+1,(screen.get_height()/6)*2,rotation,(screen.get_width()/2,(screen.get_height()/5)*2))
        print(points)
        
        if len(self.deck)>0:
            self.discard_deck.append(self.deck.pop(0))
        
        for i in range(number_of_players):
            angle=(i+1)*(360/(number_of_players+1))
            point=points[i]
            position=point
            if angle>180:
                position=point[0]-screen.get_width()/8,point[1]
            elif angle<180:
                position=point[0]+screen.get_width()/8,point[1]
            self.add_player(i,angle,position)
    
    def next_turn(self):
        if self.players[self.turn_index].cards==[]:
            self.won=True
            return
        self.turn_index= (self.turn_index + self.direction) % self.n
        
        
    def calculate_score(self):
        score=0
        for player in self.players:
            for card in player.cards:
                if card.number!="":
                    score+=int(card.number)
                elif card.special in specialCards:
                    score+=20
                elif card.special in wildCards:
                    score+=50
                else:
                    1
        return score
            
    
    def add_player(self,index,angle,position):
        cards=[]
        name=self.player_names.pop(0)
        for i in range(7):
            card=self.deck.pop(0)
            card.set_hidden(True)
            cards.append(card)
        
        self.players.append(Computer(index+1,name,position,cards,self,angle))
        
    
    
    
    def initialize_cards(self):
        for color in colors:
            self.deck.append(Card((0,0),color=color,number="0"))
            for i in range(2):
                for number in range(1,10):
                    self.deck.append(Card((0,0),color=color,number=number))
                
                for special in specialCards:
                    self.deck.append(Card((0,0),color=color,special=special))
                    
        for i in range(4):
            for wild in wildCards:
                self.deck.append(Card((0,0),special=wild))
                
            

        shuffle(self.deck)
    
    def draw(self,screen:pygame.Surface):
        screen.blit(self.table_bg,(0,0))
        
        for i,card in enumerate(self.deck):
            if i>9:
                break
            card.position=pygame.Vector2(i*2+screen.get_width()/1.8,i*2+screen.get_height()/2.4)
            card.set_hidden(True)
            card.draw(screen)
        if self.state=="transition":
            self.discard_deck[0].draw(screen)
        if len(self.discard_deck)>1:
            card=self.discard_deck[-2]
            if not card.moving:
                card.position=pygame.Vector2(screen.get_width()/2.5,screen.get_height()/2.4 )
            card.draw(screen)
        card=self.discard_deck[-1]
        if not card.moving:
            card.position=pygame.Vector2(screen.get_width()/2.5,screen.get_height()/2.4 )
        card.draw(screen)
        
        if self.color_state!="":
            text=font.render(self.color_state,True,"black")
            screen.blit(text,(screen.get_width()/2,screen.get_height()/3))
        

        for player in self.players:
            player.draw(screen)
        if self.state=="Won":
            text=font.render(f"Player {self.won+1} Wins",True,"black")
            screen.blit(text,(screen.get_width()/2,screen.get_height()/2))
    def update(self,events,dt):
        if self.state=="normal":
            player=self.players[self.turn_index]
            self.movingcard=player.update(events,dt)
            
            if self.movingcard:
                self.state="transition"
            if self.won!=None and not self.state=="transition":
                self.state="Won"
                
                
        elif self.state=="transition":
            if self.movingcard.update(events,dt):
                self.state="normal"
        else:
            return self.player_won,self.calculate_score()
            

class player:
    """
    A class to represent a player.

    Attributes
    ----------
    id: int
        Represents a unique identifier for the player.
    name: str
        The player's name.
    position: int, float or tuple of (x,y) coordinates 
        The player's position on the screen (a tuple of x and y coordinates).
    cards: list(Obj)
        A list of Card objects representing the player's hand.
    table: Obj
        The Table object which the game is played on.
    angle: int
        The angle at which the player's cards are rotated. Default is 0.
    diff: int
        Calculates the position of each card the player holds. Used as a
        horizontal offset which determines the spacing between the cards.
    type: str
        Represents the type of player, in this case, Human.
    state: str
        Represents the current state of the player.
    shouted: bool
        Determines whether the player has shouted "UNO".
    player_name_text: Obj
        A rendered version of the player's name.
    name_position: tuple of (x,y) coordinates
        The position at which the player's name is displayed. It is based on
        their position, size of card and an offset.
    

    Methods
    -------
    shout_uno:
        Set shouted variable to True, and plays a sound.
    getValidCards:
        Returns a list of indices of the cards in a hand that can be played on current discard pile
    draw_card:
        Draws a card from the deck and adds it to the player's hand. If deck is empty, reshuffle discard pile and set new deck.
    draw:
        Draws player's cards and name onto the game screen.
    """
    def __init__(self,id,name,position,cards,table,angle=0) -> None:
        self.id=id
        self.name=name
        self.cards=cards
        self.position=position
        self.angle=angle
        self.diff=40
        self.table=table
        self.type=""
        self.state="normal"
        self.shouted=False
        self.player_name_text=font.render(self.name,True,"black")
        self.name_position=self.position[0]-self.player_name_text.get_width()/2-self.cards[0].rect.width/2,self.position[1]+self.cards[0].rect.height+40
        
    
    def shout_uno(self):
        self.shouted=True
        pygame.mixer.music.play()
    
    def getValidCards(self):
        validcards=[]
        for i,card in enumerate(self.cards):
            if card.canPlayedOn(self.table.discard_deck[len(self.table.discard_deck)-1]):
                validcards.append(i)
        return validcards
    
    def draw_card(self):
        if self.table.deck!=[]:
            card=self.table.deck.pop(0)
            self.cards.append(card)
            if self.table.deck==[]:
                self.table.deck=self.table.discard_deck[:-1]
                self.table.discard_deck=[self.table.discard_deck[-1]]
                shuffle(self.table.deck)
            card.rotate(self.angle)
            card.move(self.position)
            if self.type=="Human":
                card.set_hidden(False)
            return card
        
        
    
    def draw(self,screen):
        for i,card in enumerate(self.cards):
            y_diff=0
            if self.table.turn_index==self.id:
                if self.type=="Human" and i in self.getValidCards() :
                    if self.disposed and self.picked and self.table.state=="normal":
                        y_diff=50
            if not card.moving:
                card.position=pygame.Vector2(self.position[0]-(len(self.cards)/2*self.diff)+i*self.diff-100,self.position[1]-y_diff)
                card.calculate_rect()
            card.angle=self.angle
            card.draw(screen)
        screen.blit(self.player_name_text,(self.name_position))
           

class Human(player):
    """
    A subclass to represent a human player.

    Attributes
    ----------
    id: int 
        Represents a unique identifier for the player.
    name: str
        The player's name.
    position: int, float or tuple of (x,y) coordinates.
        Represents players position on the table.
    cards: list(Obj)
        Represents the cards in the player's hand.
    table: Obj
        Represents the game table.
    type: str
        Represents the type of player, in this case, Human.
    disposed: bool
        Determines whether the player has already disposed of a card during their turn.
    picked: bool
        Determines whether the player has already picked up a card during their turn.
    to_pick: integer
        The number of cards the player is required to pick up.
    waspicking: bool
        Determines whether the player was picking up cards in the previous turn.
    new_picked: bool
        Determines whether the player has just picked up a card.
    uno_button: Obj
        The "UNO" button.
    color_buttons: list(Obj)
        Represents the list of buttons for selecting a color.
    pickingcolor: bool
        Determines whether the player is currently picking a color.
    canshoutUno: bool
        Determines whether the player can shout "UNO" (i.e. if they only have one card remaining in their hand).

    Methods
    -------
    select_color:
        Sets the card on top of the discard pile's colour, 
        pickingcolor is set to False, updates color_state and advances
        to next turn.
    draw:
        Draws all inherited from player class, and also checks if player is
        picking colour, in which case draws the buttons for colours.
    update:
        Updates the game state. Checks a variety of conditions: if a player
        is picking up a card, disposing a card, picking a colour, has won. If
        True, updates game state accordingly.

    """
    def __init__(self,id,name,position,cards,table) -> None:
        super().__init__(id,name,position,cards,table)
        self.type="Human"
        self.disposed=False
        self.picked=False
        self.to_pick=0
        self.waspicking=False
        self.new_picked=False
        self.uno_button=Button(((screen.get_width()/8)*7,self.position[1]+100),"UNO",self.shout_uno)
        self.color_buttons=[]
        self.pickingcolor=False
        self.canshoutUno=False
        
        
        for i,color in enumerate(colors):
            self.color_buttons.append(Button((screen.get_width()/2-300+(150*i),self.position[1]-55),color,lambda c=color:self.select_color(c)))
    
    def select_color(self,color):
        if color:
            self.table.discard_deck[-1].color=color
            self.pickingcolor=False
            self.table.color_state=color
            self.table.next_turn()
            self.disposed=False
            self.picked=False
            self.new_picked=False
    
    def draw(self, screen):
        super().draw(screen)
        
        if self.pickingcolor:
            for b in self.color_buttons:
                b.draw(screen)
       
    def update(self,events,dt):        
        if self.to_pick!=0:
            self.to_pick-=1
            self.waspicking=True
            return self.draw_card()
        elif self.waspicking:
            self.table.next_turn()
            self.waspicking=False
        elif self.table.turn_index==self.id:
            
            if not self.disposed:
                for i in range(len(self.cards)-1,-1,-1):
                    if self.cards[i].update(events,dt):
                        card=self.cards.pop(i)
                        
                        self.table.discard_deck.insert(0,card)
                        
                        card.move(self.table.discard_deck_position)
                        self.disposed=True
                        return card
                
            elif self.disposed and not self.picked:
                self.picked=True
                return self.draw_card()
                
            elif self.picked and not self.pickingcolor:
                if self.cards==[]:
                    self.table.won=self.id
                    return
                validcards=self.getValidCards()
                if validcards==[] and not self.new_picked:
                    self.new_picked=True
                    return self.draw_card()
                validcards=self.getValidCards()
                if len(validcards)==1 and not self.shouted and len(self.cards)==1:
                    self.uno_button.draw(screen)
                    self.uno_button.update(events)
                for i in reversed(validcards):
                    if self.cards[i].update(events,dt):
                        if len(self.cards)==1 and not self.shouted:
                            self.to_pick=4
                            break
                        elif len(self.cards)==1:
                            self.table.player_won=self.name
                            
                        card=self.cards.pop(i)
                        self.table.color_state=""
                        if card.special=="Reverse":
                            self.table.direction*=-1
                            if len(self.table.players)==2:
                                self.table.next_turn()
                        elif card.special=="Skip":
                            self.table.next_turn()
                        elif card.special=="Draw":
                            self.table.players[(self.table.turn_index + self.table.direction) % self.table.n].to_pick=2
                        elif card.special=="Wild_Draw":
                            self.table.players[(self.table.turn_index + self.table.direction) % self.table.n].to_pick=4
                            self.pickingcolor=True
                        elif card.special=="Wild":
                            self.pickingcolor=True
                            
                        self.table.discard_deck.append(card)
                        
                        if not self.pickingcolor:
                            self.table.next_turn()
                            self.disposed=False
                            self.picked=False
                            self.new_picked=False
                        card.move(self.table.discard_deck_position)
                        
                        return card
                validcards=self.getValidCards()
                if validcards==[]:
                    self.table.next_turn()
                    self.disposed=False
                    self.new_picked=False
                    self.picked=False
            elif self.pickingcolor:
                for b in self.color_buttons:
                    b.update(events)
                

class Computer(player):
    """
    A subclass to represent a computer player.

    Attributes
    ----------
    id: int 
        Representing a unique identifier for the player.
    name: str
        Representing the player's name.
    position: int, float or tuple of (x,y) coordinates.
        Represents players position on the table.
    cards: list(Obj)
        Represents the cards in the player's hand.
    table: Obj
        Represents the game table.
    angle: int 
        The angle at which the player's cards are rotated.
    type: str
        Represents the type of player, in this case, Computer.
    diff: int
        Calculates the position of each card the player holds. Used as a
        horizontal offset which determines the spacing between the cards.
    disposed: bool
        Indicates whether the player has already disposed of a card during their turn.
    picked: bool
        Indicates whether the player has already picked up a card during their turn.
    to_pick: int
        The number of cards the player is required to pick up.
    waspicking: bool
        Indicates whether the player was picking up cards in the previous turn.
    new_picked: bool
        Indicates whether the player has just picked up a card.

    Methods
    -------
    update:
        Updates the game state. Runs through a number of conditionals based on
        game rules to check CPU's hand, play and update the game state accordingly.

    """
    def __init__(self,id,name,position,cards,table,angle) -> None:
        super().__init__(id,name,position,cards,table,angle)
        for card in self.cards:
            #card.hidden=True
            card.rotate(self.angle)
        self.type="Computer"
        self.diff=10
        self.disposed=False
        self.picked=False
        self.to_pick=0
        self.waspicking=False
        self.new_picked=False

        
    def update(self,events,dt):
        if self.to_pick!=0:
            self.to_pick-=1
            self.waspicking=True
            return self.draw_card()
        elif self.waspicking:
            self.table.next_turn()
            self.waspicking=False
        elif self.table.turn_index==self.id:
            if not self.disposed:
                if len(self.cards)>0:
                    card=self.cards.pop(randint(0,len(self.cards)-1))
                    self.table.discard_deck.insert(0,card)
                    card.rotate(0)
                    card.move(self.table.discard_deck_position)
                    self.disposed=True
                    return card
            elif self.disposed and not self.picked:
                self.picked=True
                return self.draw_card()
            
            elif self.picked:
                validcards=self.getValidCards()
                if validcards==[] and not self.new_picked:
                    self.new_picked=True
                    return self.draw_card()
                
                validcards=self.getValidCards()
                if len(validcards)==1 and not self.shouted and len(self.cards)==1:
                    self.shout_uno()
                    
                    self.table.player_won=self.name
                if len(validcards)>0:
                    
                    self.table.color_state=""
                    card=self.cards.pop(validcards[randint(0,len(validcards)-1)])
                    if card.special=="Reverse":
                        self.table.direction*=-1
                        if len(self.table.players)==2:
                            self.table.next_turn()
                        
                    card.set_hidden(False)
                    if card.special=="Wild":
                        card.color=choice(colors)
                        self.table.color_state=card.color
                    if card.special=="Skip":
                        self.table.next_turn()
                    if card.special=="Draw":
                        
                        self.table.players[(self.table.turn_index + self.table.direction) % self.table.n].to_pick=2
                        
                    if card.special=="Wild_Draw":
                        card.color=choice(colors)
                        self.table.color_state=card.color
                        
                        self.table.players[(self.table.turn_index + self.table.direction) % self.table.n].to_pick=4
                    card.rotate(0)
                    self.table.discard_deck.append(card)
                    
                    self.table.next_turn()
                    card.move(self.table.discard_deck_position)
                    self.disposed=False
                    self.picked=False
                    self.new_picked=False
                    return card
                validcards=self.getValidCards()
                if validcards==[]:
                    self.table.next_turn()
                    self.disposed=False
                    self.picked=False
                    self.new_picked=False
                    
                    
class Button:
    """
    A class representing a button.

    Attributes
    ----------
    position: int, float or tuple of (x,y) coordinates.
        Represents players position on the table.
    text: str
        The text to be displayed on the button.
    callback: func
        The function to be called when the button is clicked.
    image:
        (Optional) Represents an image to be displayed on the button.
    rect: pygame.Rect
        Rectangle object representing the area of the button.
    text_surface: pygame.Obj
        Render object of the text attribute.
    text_rect: pygame.Obj
        Rectangle object representing the area of the text on the button.
    hover_text_surface: pygame.Obj
        Render object of a hover action on the button.
    hover: bool
        Determines whether the cursor is hovering over the button.
    color: str
        The colour of the button.
    clicked: bool
        Determines whether the button has been clicked.


    Methods
    -------
    draw:
        Draws the button object to the screen, and updates the color attribute
        depending on the hover action.
    update:
        Checks for mouse events and updates the 'hover' and 'clicked' attributes
        accordingly. If a button is clicked, the 'callback' function fires.
    """
    def __init__(self,position,text="",callback=None,image=None):
        self.position=position
        self.text=text
        self.image=image
        self.callback=callback
        if self.image:
            self.rect=self.image.get_rect()
            self.rect.topleft=self.position
        else:
            self.rect=pygame.Rect(self.position,(150,100))
            self.rect.center=self.position
        self.text_surface=font.render(text,True,"black")
        self.text_rect=self.text_surface.get_rect(center=self.position)
        self.hover_text_surface=font.render(text,True,"white")
        self.hover=False
        self.color="black"
        self.clicked=False
        
    def draw(self,screen):
        if self.image:
            screen.blit(self.image,self.position)
        else:
            if self.hover:
                self.color="white"
                screen.blit(self.hover_text_surface,self.text_rect)
            else:
                self.color="black"
                screen.blit(self.text_surface,self.text_rect)
            pygame.draw.rect(screen,self.color,self.rect,width=5)

        
    
    def update(self,events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.hover=True
                else:
                    self.hover=False
            elif event.type ==pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.clicked=True
            elif event.type ==pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(pygame.mouse.get_pos()) and self.clicked:
                    self.callback()
                else:
                    self.clicked=False
class Toggle:
    """
    A class representing a toggle feature for switching colours in buttons.

    Attributes
    ----------
    position: int, float or tuple of (x,y) coordinates.
        Represents players position on the table.
    text: str
        The text to be displayed on the button.
    callback: func
        The function to be called when the button is clicked.
    toggable: bool
    state: bool
        The state of the toggle.
    rect: pygame.Rect
        Rectangle object representing the area of the button.
    text_surface: pygame.Obj
        Render object of the text attribute.
    text_rect: pygame.Obj
        Rectangle object representing the area of the text on the button.
    hover_text_surface: pygame.Obj
        Render object of a hover action on the button.
    hover: bool
        Determines whether the cursor is hovering over the button.
    color: str
        The colour of the button.
    clicked: bool
        Determines whether the button has been clicked.


    Methods
    -------
    toggle:
        Sets the state of the toggle based on a state argument.
    draw:
        Checks value of 'hover' and 'state'. If True, turns button white, else leaves black.
    update:
        Checks for mouse events and updates the 'hover' and 'clicked' attributes
        accordingly. If a button is clicked, the 'callback' function fires.
    """
    def __init__(self,position,text="",callback=None,toggable=False):
        self.position=position
        self.text=text
        
        self.callback=callback
        self.state=False
        
        self.rect=pygame.Rect(self.position,(150,100))
        self.rect.center=self.position
        self.text_surface=font.render(text,True,"black")
        self.text_rect=self.text_surface.get_rect(center=self.position)
        self.hover_text_surface=font.render(text,True,"white")
        self.hover=False
        self.color="black"
        self.clicked=False
    
    def toggle(self,state):
        self.state=state    
    
    def draw(self,screen):
        if self.hover or self.state:
            self.color="white"
            screen.blit(self.hover_text_surface,self.text_rect)
        else:
            self.color="black"
            screen.blit(self.text_surface,self.text_rect)
        pygame.draw.rect(screen,self.color,self.rect,width=5)

        
    
    def update(self,events):
        
        for event in events:
            
            if event.type ==pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.clicked=True
            elif event.type ==pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(pygame.mouse.get_pos()) and self.clicked:
                    
                    self.callback()
                    self.toggle(True)
                else:
                    self.clicked=False
            if self.rect.collidepoint(pygame.mouse.get_pos()) :
                    self.hover=True
            elif not self.state:
                self.hover=False

class Start_Screen:
    """
    A class representing the start screen (Main Menu).

    Attributes
    ----------
    table_bg: pygame.Surface
        Render object of the game background (fit to full_screen).
    logo: pygame.image
        Image object of the UNO logo.
    title: pygame.Obj
        Render object of the title given (in this case: "Welcome To Uno")
    title_rect: pygame.Obj
        Rectangle object representing the area of the title.
    selected: int
        Keeps track of what has been selected.
    play: bool
        Determines the state of play.
    buttons: list
        Represents the buttons available on the screen.


    Methods
    -------
    onplay:
        Sets the play attribute to True, sending the user to the next screen/into a game.
    pressed:
        Determines if a button has been selected, and stores which button has been clicked on via numeric identifier.
    draw:
       Draws the logo, title, table_bg and buttons to the screen.
    update:
        Calls the update method from the Buttons class for the button in the list of buttons.
    """
    def __init__(self):
      self.table_bg = pygame.transform.smoothscale(pygame.image.load("Assets/Tables/Table_0.png"),screen.get_size())
      self.logo = pygame.image.load("Assets/UNO_Logo.png")
      self.title=font.render("Welcome To Uno","True","black")
      self.title_rect=self.title.get_rect(center=(screen.get_width()/2,screen.get_height()/2.1))
      self.selected=0
      self.play=False
      self.buttons=[]
      x=1
      y=0
      
      for i in range(1,3,1):
        pos=(screen.get_width()/2)*(x)
        
        self.buttons.append(Button((pos,y*200+screen.get_height()/1.5),str(menu[i]),lambda i=i: self.pressed(i)))
        y+=1
        if x>3:
          x=1
          y+=1

    def onplay(self):
        self.play=True
                
    def pressed(self,i):
        self.selected=i
        print(self.selected)
    
    def draw(self,screen):
        screen.blit(self.table_bg,(0,0))
        screen.blit(self.logo,(screen.get_width()/2-self.logo.get_width()/2,screen.get_height()/6))
        screen.blit(self.title,self.title_rect)
        for button in self.buttons:
            button.draw(screen)
            
    
    def update(self,events):
        for button in self.buttons:
            button.update(events)
        return self.selected

class Select_Screen:
    """
    A class representing the player selection screen.

    Attributes
    ----------
    table_bg: pygame.Surface
        Render object of the game background (fit to full_screen).
    logo: pygame.image
        Image object of the UNO logo.
    title: pygame.Obj
        Render object of the title given (in this case: "Welcome To Uno")
    title_rect: pygame.Obj
        Rectangle object representing the area of the title.
    play_button: Obj
        Button Object with an attached onplay method.
    selected: int
        Keeps track of what has been selected.
    play: bool
        Determines the state of play.
    buttons: list
        Represents the buttons available on the screen.


    Methods
    -------
    onplay:
        Sets the play attribute to True, sending the user to the next screen/into a game.
    onselect:
        Sets state of the buttons using Toggle.toggle method and identifies the selected button.
    draw:
       Draws the logo, title, table_bg and buttons to the screen. Once button clicked, play button is drawn to screen too. 
    update:
        Calls the update method from the Buttons class for the button in the list of buttons. Also returns 'selected' variable
        depending on whether the 'play' variable is True.
    """
    def __init__(self):
        self.table_bg = pygame.transform.smoothscale(pygame.image.load("Assets/Tables/Table_0.png"),screen.get_size())
        self.logo = pygame.image.load("Assets/UNO_Logo.png")
        self.title=font.render("Select Number of Players: ","True","black")
        self.title_rect=self.title.get_rect(center=(screen.get_width()/2,screen.get_height()/2.1))
        self.play_button=Button((screen.get_width()-75,screen.get_height()-50),"Play",lambda : self.onplay())
        self.selected=0
        self.play=False
        self.buttons=[]
        x=1
        y=0
        
        for i in range(2,8):
            pos=(screen.get_width()/4)*(x)
            
            self.buttons.append(Toggle((pos,y*200+screen.get_height()/1.5),str(i),lambda i=i: self.onselect(i)))
            x+=1
            if x>3:
                x=1
                y+=1
                
    def onplay(self):
        self.play=True
    
    def onselect(self,i):
        for but in self.buttons:
            but.toggle(False)
        self.selected=i
    
    def draw(self,screen):
        screen.blit(self.table_bg,(0,0))
        screen.blit(self.logo,(screen.get_width()/2-self.logo.get_width()/2,screen.get_height()/6))
        screen.blit(self.title,self.title_rect)
        
        for button in self.buttons:
            button.draw(screen)
        if self.selected:
            self.play_button.draw(screen)
            
    
    def update(self,events):
        
        for button in self.buttons:
            button.update(events)
        if self.selected:
            self.play_button.update(events)
        if self.play:
            return self.selected
        return 0
        

class Win_Screen:
    """
    A class representing the endgame screen.

    Attributes
    ----------
    player: str
        Represents a player name.
    score: int
        Represents a player's score.
    table_bg: pygame.Surface
        Render object of the game background (fit to full_screen).
    con_text: pygame.Obj
        Render object of a congratulatory message.
    player_text: pygame.Obj
        Render object of the player's name.
    score_text: pygame.Obj
        Render object of the score.
    playagain_button: Obj
        A Button object representing 'play again'.
    play: bool
        Determines the state of play.

    Methods
    -------
    play_again:
        Sets the state of play to True.
    draw:
       Draws the background, congratulations, player name, player score and play again 
       button to the screen.
    update:
        Calls itself on the 'play again' button based on the list of events passed as arguments.
        Then updates the play attribute to be True.
    """
    def __init__(self,player,score) -> None:
        self.table_bg = pygame.transform.smoothscale(pygame.image.load("Assets/Tables/Table_0.png"),screen.get_size())
        self.con_text=font.render("Congratulation",True,"black")
        
        self.player_text=font.render(f"{player} Win",True,"black")
        self.score_text=font.render(f"Score: {score}",True,"black")
        self.playagain_button=Button((-125+screen.get_width()/2,screen.get_height()/2+250),"Play Again",self.play_again)
        self.playagain_button.rect.width=250
        self.playagain_button.rect.center=(screen.get_width()/2,screen.get_height()/2+250)
        self.playagain_button.text_rect=self.playagain_button.text_surface.get_rect(center=self.playagain_button.rect.center)
        self.play=False

    def play_again(self):
        self.play=True
    def draw(self,screen):
        screen.blit(self.table_bg,(0,0))
        screen.blit(self.con_text,(-self.con_text.get_width()/2+screen.get_width()/2,screen.get_height()/3))
        screen.blit(self.player_text,(-self.player_text.get_width()/2+screen.get_width()/2,screen.get_height()/2))
        screen.blit(self.score_text,(-self.score_text.get_width()/2+screen.get_width()/2,screen.get_height()/2+100))
        self.playagain_button.draw(screen)
    
    def update(self,events):
        self.playagain_button.update(events)
        if self.play:
            return True
        

class Game:
    """
    A class representing the Game's states (scenes).

    Attributes
    ----------
    state: str
        Keeps track of the current state of the game.
    selector: Obj
        Displays the given object to the screen (as a scene).
    close_button: Obj
        Button object that can be clicked to close the game.
    isquit: bool
        Determines whether the game has been quit or not. 

    Methods
    -------
    exit:
        Sets 'isquit' to True, therefore closing the game.
    update:
        Determines which scene should be displayed to the screen,
        as well as checking if any buttons have been pressed which
        would result in the game closing.
    """
    def __init__(self):
        self.state="start_screen"
        self.selector=Start_Screen()
        
        close_icon=pygame.image.load("Assets/UI/close.png")
        
        self.close_button=Button((screen.get_width()-130,0),callback=self.exit,image=close_icon)
        self.isquit=False
    
    def exit(self):
        print("quit")
        self.isquit=True
    
    def update(self,events,dt):
        self.close_button.update(events)

        if self.state=="start_screen":
            self.selector.draw(screen)
            selected=self.selector.update(events)
            if selected==1:
                self.state="select_screen"
                self.selector = Select_Screen()
            elif selected==2:
                exit()
        
        if self.state=="select_screen":
            self.selector.draw(screen)
            selected=self.selector.update(events)
            if selected>1:
                self.state="game"
                self.table=Table(selected)
                
            
        elif self.state=="game":
            self.table.draw(screen)
            result=self.table.update(events,dt)
            if result:
                self.winscreen=Win_Screen(result[0],result[1])
                self.state="won"
        
        elif self.state=="won":
            self.winscreen.draw(screen)
            if self.winscreen.update(events):
                self.selector.play=False
                self.state="select_screen"
        
            
        self.close_button.draw(screen)
        if self.isquit:
            return True

# the main game loop
def main():
    
    gameover=False
    game=Game()
    while not gameover:
        events=pygame.event.get()
        clock.tick(60)
        delta=clock.get_time()/1000
        for event in events:
            if event.type == pygame.QUIT:
                gameover=True
        if game.update(events,delta):
            gameover= not gameover
        
        pygame.display.update()
    

if __name__ == "__main__":
    main()