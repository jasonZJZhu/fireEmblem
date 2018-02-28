'''
Jason Zhu
sprites
'''
import pygame
pygame.init()
'''creates variables for all the fonts and sizes needed'''
xl_font = pygame.font.Font("Fire_Emblem_Text.ttf", 45)
large_font = pygame.font.Font("Fire_Emblem_Text.ttf", 30)
medium_font = pygame.font.Font("Fire_Emblem_Text.ttf", 25)
small_font = pygame.font.Font("Fire_Emblem_Text.ttf", 20)
dank_font = pygame.font.Font("ReggaeC.ttf",30)

class Grid(pygame.sprite.Sprite):
    '''this class is the most important class in the whole entire game, it makes up the grids they walk on, special effects and many other features'''
    def __init__(self,screen,x,y,item):
        pygame.sprite.Sprite.__init__(self)
        
        '''determine what kind of grid it is'''
        if item == 'f':
            self.__type = 'Forest'
            self.__forest1 = pygame.image.load("Sprites/map/forest1.gif").convert()
            self.__forest2 = pygame.image.load("Sprites/map/forest2.gif").convert()
            self.image = self.__forest1
            self.__def = 5
            self.__avo = 10           
        elif item == 'm':
            self.__type = 'Mountain'
            self.image = pygame.image.load("Sprites/map/mountain.gif").convert()
            self.__def = 10
            self.__avo = 10            
        elif item == 's':
            self.__type = 'Sea'
            self.__sea1 = pygame.image.load("Sprites/map/sea1.gif").convert()
            self.__sea2 = pygame.image.load("Sprites/map/sea2.gif").convert()
            self.image = self.__sea1
            self.__def = 0
            self.__avo = 30            
        else:
            self.__type = 'Plains'
            self.image = pygame.image.load("Sprites/map/plain.gif").convert()
            self.__def = 0
            self.__avo = 0
        self.rect = self.image.get_rect()
        '''attribute used to create a sense of movement'''
        self.__count = 0
        '''attributes used to interact with other sprites'''
        self.__contain = False
        self.__cover = False

        
        self.rect.left = 50*(x-1)
        self.rect.top = 50*(y-1)
        self.__screen = screen
    
    def get_status(self):
        '''return attributes to be used by main module'''
        return ((self.rect.left/50,self.rect.top/50), self.__contain, self.__cover,self.__type)
    
    def receive(self,character):
        '''takes in other sprites'''
        self.__contain = character
    
    def cover(self,turn,side,square):
        '''takes in other sprites'''
        if turn:
            if self.__type == "Plains" or self.__type == "Forest":
                if self.__contain:
                    square.kill()
                    return True
                else:
                    self.__cover = (side,square)
            else:
                square.kill()
                return True
        else:
            self.__cover = side,square
    
    def reset_squares(self):
        '''remove the value of other sprites given to the grid'''
        self.__cover = False
    
    def remove(self):
        '''remove the value of otehr sprites given to the grid'''
        self.__contain = False
    
    def display(self):
        '''attributes given to Display sprites'''
        return (self.__type,self.__def,self.__avo)
    
    def update(self):
        '''creates a sense of movement'''
        if self.__type == "Sea":
            self.__count += 1
        if self.__count == 15:
            if self.image == self.__sea1:
                self.image = self.__sea2
            else:
                self.image = self.__sea1
            self.image.convert()
            self.__count = 0
            
        if self.__type == "Forest":
            self.__count += 1
        if self.__count == 15:
            if self.image == self.__forest1:
                self.image = self.__forest2
            else:
                self.image = self.__forest1
            self.image.convert()
            self.__count = 0        

class Selector(pygame.sprite.Sprite):
    '''this class is all that the player has direct control over, it helps them select characters and options'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((50,50))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image,(129, 238, 255),((0,0),(50,50)), 10)
        
        self.__x_pos = 8
        self.__y_pos = 6
        
    def change_xpos(self, change):
        '''x movement'''
        if change > 0:
            if self.__x_pos < 15:
                self.__x_pos += change
                return True
        elif self.__x_pos > 0:
            self.__x_pos += change
            return True
    
    def change_ypos(self, change):
        '''y movement'''
        if change > 0:
            if self.__y_pos < 11:
                self.__y_pos += change
                return True
        elif self.__y_pos > 0:
            self.__y_pos += change
            return True
            
    def selected(self):
        '''return self position for main module'''
        return self.__x_pos, self.__y_pos
            
    def update(self):
        self.rect.left = self.__x_pos*50
        self.rect.top = self.__y_pos*50

class Character(pygame.sprite.Sprite):
    '''this class is the life of the game, where all the actions happen'''
    def __init__(self,status,char):
        pygame.sprite.Sprite.__init__(self)
        
        self.__type = int(status[2])
        '''the following code determines the value and side of the character'''
        if char:
            if self.__type == 10:
                self.__coloured = pygame.image.load("Sprites/characters/blue_hero.gif") 
                self.__grey = pygame.image.load("Sprites/characters/b_blue_hero.gif")
                self.image = self.__coloured
                
            elif self.__type == 11:
                self.__coloured = pygame.image.load("Sprites/characters/blue_axe.gif")
                self.__grey = pygame.image.load("Sprites/characters/b_blue_axe.gif")
                self.image = self.__coloured
                
            elif self.__type == 12:
                self.__coloured = pygame.image.load("Sprites/characters/blue_spear.gif")
                self.__grey = pygame.image.load("Sprites/characters/b_blue_spear.gif")
                self.image = self.__coloured
                
            elif self.__type == 13:
                self.__coloured = pygame.image.load("Sprites/characters/blue_sword.gif")          
                self.__grey = pygame.image.load("Sprites/characters/b_blue_sword.gif")
                self.image = self.__coloured
        else:
            if self.__type == 20:
                self.__coloured = pygame.image.load("Sprites/characters/red_boss.gif")      
                self.__grey = pygame.image.load("Sprites/characters/b_red_boss.gif")
                self.image = self.__coloured
                
            elif self.__type == 21:
                self.__coloured = pygame.image.load("Sprites/characters/red_axe.gif")   
                self.__grey = pygame.image.load("Sprites/characters/b_red_axe.gif")
                self.image = self.__coloured
                
            elif self.__type == 22:
                self.__coloured = pygame.image.load("Sprites/characters/red_spear.gif")
                self.__grey = pygame.image.load("Sprites/characters/b_red_spear.gif")
                self.image = self.__coloured
                
            elif self.__type == 23:
                self.__coloured = pygame.image.load("Sprites/characters/red_sword.gif")
                self.__grey = pygame.image.load("Sprites/characters/b_red_sword.gif")
                self.image = self.__coloured
        self.rect = self.image.get_rect()
        self.set_status(char)
        '''sets position for character'''
        self.__x_pos = status[0]-1
        self.__y_pos = status[1]-1
        '''attributes used for movement'''
        self.__x_move = 0
        self.__y_move = 0
        '''attributes used to determine the state of the character'''
        self.__moved = False
        self.__over = False
        self.__still = True
        self.__battle = False
        self.__been_hit = False
        
        self.rect.left = (status[0]-1)*50 +5
        self.rect.top = (status[1]-1)*50 +5
    
    def get_pos(self):
        '''returns position for other sprites'''
        return (self.__x_pos, self.__y_pos)
    
    def set_status(self,char):
        '''sets attributes for these characters which affects their future interactions'''
        if char:
            '''move= how far they can move
            max hp= maximum health
            current hp= current health
            off= attack damage
            def= defence
            agi= speed
            crit= critical chance
            hit= hit chance
            avo= miss chance'''
            if self.__type == 10:
                self.__move = 3
                self.__max_hp= 60
                self.__current_hp = 60
                self.__off = 15
                self.__def = 0
                self.__agi = 10
                self.__crit = 5
                self.__hit = 95
                self.__avo = 10
            elif self.__type == 11:
                self.__move = 2
                self.__max_hp= 35
                self.__current_hp = 35
                self.__off = 13
                self.__def = 5
                self.__agi = 5
                self.__crit = 0
                self.__hit = 90
                self.__avo = 0
            elif self.__type == 12:
                self.__move = 2
                self.__max_hp= 25
                self.__current_hp = 25
                self.__off = 18
                self.__def = 3
                self.__agi = 0
                self.__crit = 5
                self.__hit = 100
                self.__avo = 5
            else:
                self.__move = 3
                self.__max_hp= 30
                self.__current_hp = 30
                self.__off = 11
                self.__def = 0
                self.__agi = 10
                self.__crit = 3
                self.__hit = 95
                self.__avo = 10
        else:
            if self.__type == 20:
                self.__move = 3
                self.__max_hp= 60
                self.__current_hp = 60
                self.__off = 15
                self.__def = 0
                self.__agi = 10
                self.__crit = 5
                self.__hit = 95
                self.__avo = 10
            elif self.__type == 21:
                self.__move = 2
                self.__max_hp= 35
                self.__current_hp = 35
                self.__off = 13
                self.__def = 5
                self.__agi = 5
                self.__crit = 0
                self.__hit = 90
                self.__avo = 0
            elif self.__type == 22:
                self.__move = 2
                self.__max_hp= 25
                self.__current_hp = 25
                self.__off = 18
                self.__def = 3
                self.__agi = 0
                self.__crit = 5
                self.__hit = 100
                self.__avo = 5
            else:
                self.__move = 3
                self.__max_hp= 30
                self.__current_hp = 30
                self.__off = 11
                self.__def = 0
                self.__agi = 10
                self.__crit = 3
                self.__hit = 95
                self.__avo = 10
    
    def get_status(self):
        '''return the status of character for display purposes'''
        return (self.__type, self.__move, self,self.__max_hp,self.__current_hp)
    
    def get_value(self):
        '''returns the values of character for interactions with other sprites'''
        return (self.__type,self.__current_hp,self.__max_hp,self.__off,self.__def,self.__agi,self.__crit,self.__hit,self.__avo)

    def change_bonus(self,bonus):
        '''attributes from the grid, boosts the character's stats'''
        self.__def+= bonus[1]
        self.__agi+= bonus[2]

    def move(self,move):
        '''change attributes for animation purposes'''
        self.__x_pos += move[0]
        self.__x_move = move[0]*2      
        self.__y_pos += move[1]
        self.__y_move = move[1]*2
        self.__moved = True
    
    def turnover(self):
        '''mutator method, change if the character can make a move'''
        self.__over = True
        
    def check_moved(self):
        '''returns self status for main module'''
        return (self.__moved, self.__over, self.__still)
    
    def reset(self):
        '''mutator method'''
        self.__moved = False
        self.__over = False
    
    def attack(self,pos):
        '''trigger for attack animation'''
        self.__battle = True
        self.__count = 4
        self.__x_change = pos[0]-self.__x_pos
        self.__y_change = pos[1]-self.__y_pos
    
    def defend(self,damage):
        '''trigger for defend animation'''
        self.__been_hit = True
        self.__current_hp -= damage
        if self.__current_hp <= 0:
            self.kill()
            return self.get_pos()
        else:
            self.__count = 4
        return False
    
    def update(self):
        '''moves the chracter by its status'''
        if self.__x_move != 0:
            self.__still = False
            if self.__x_move > 0:
                self.rect.left += 25
                self.__x_move -= 1
            else:
                self.rect.left -= 25
                self.__x_move += 1
                
        elif self.__y_move != 0:
            self.__still = False            
            if self.__y_move > 0:
                self.rect.top += 25
                self.__y_move -= 1
            else:
                self.rect.top -= 25
                self.__y_move += 1
                
        elif self.__battle:
            self.__count -= 1
            self.__still = False
            if self.__count >= 2:
                self.rect.left += 20*self.__x_change
                self.rect.top += 20*self.__y_change
            else:
                self.rect.left -= 20*self.__x_change
                self.rect.top -= 20*self.__y_change
            if self.__count == 0:
                self.__still = True
                self.__battle = False
                self.__count = 4
                
        elif self.__been_hit:
            self.__still = False
            if self.__count != 0:
                if self.__count%2 == 0:
                    self.rect.left += 5
                else:
                    self.rect.left -= 5
                self.__count -=1
            else:
                self.__still = True
                self.__been_hit = False
                self.__count = 4
                        
        elif self.__over:
            self.__still = True            
            self.image = self.__grey
        elif self.__over == False:
            self.__still = True
            self.image = self.__coloured
                

class Square(pygame.sprite.Sprite):
    '''this display related sprite is used in interaction with character sprites'''
    def __init__(self,x,y,side):
        pygame.sprite.Sprite.__init__(self)
        '''determine the color'''
        if side:
            self.image = pygame.image.load("Sprites/map/red_square.gif")
        else:
            self.image = pygame.image.load("Sprites/map/blue_square.gif")
        self.rect = self.image.get_rect()
        self.__side = side        
        
        self.rect.left = 50*x+5
        self.rect.top = 50*y+5

class Clear(pygame.sprite.Sprite):
    '''this sprite is used to clear off certain sprites by using collision detection'''
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface(screen.get_size())
        self.rect = self.image.get_rect()
        
        self.rect.left = 0
        self.rect.top = 0

class Display(pygame.sprite.Sprite):
    '''this class is used for most of the displays'''
    def __init__(self,screen,usage,variable):
        pygame.sprite.Sprite.__init__(self)
        
        if usage:
            if usage == 1:
                '''the first usage of the display is to display the bonuses which a grid gives'''
                self.__type = 1
                self.__image1 = pygame.image.load("Sprites/system/grid.gif")
                self.set_status(("Plains",0,0))            
                self.__image1.blit(self.__label1,(10,15))
                self.__image1.blit(self.__label2,(5,50))
                self.__image1.blit(self.__label3,(5,75))
            
                self.__image2 = pygame.image.load("Sprites/system/grid.gif")
                self.set_status(("Forest",5,10))            
                self.__image2.blit(self.__label1,(10,15))
                self.__image2.blit(self.__label2,(5,50))
                self.__image2.blit(self.__label3,(5,75))
                
                self.__image3 = pygame.image.load("Sprites/system/grid.gif")
                self.set_status(("Mountain",10,10))            
                self.__image3.blit(self.__label1,(10,15))
                self.__image3.blit(self.__label2,(5,50))
                self.__image3.blit(self.__label3,(5,75))
            
                self.__image4 = pygame.image.load("Sprites/system/grid.gif")
                self.set_status(("Sea",0,30))            
                self.__image4.blit(self.__label1,(10,15))
                self.__image4.blit(self.__label2,(5,50))
                self.__image4.blit(self.__label3,(5,75))            
            
                self.image = self.__image1
                self.rect = self.image.get_rect()            
                self.rect.bottom = screen.get_height()-20
                self.rect.left = 20
            else:
                self.__type = 2
                '''the second usage of the display is to display the character status'''
                if variable:
                    self.image = pygame.image.load("Sprites/system/stats.gif")
                else:
                    self.image = pygame.image.load("Sprites/system/stats_red.gif")
                self.rect = self.image.get_rect()
                self.rect.bottom = screen.get_height()-140
                self.rect.left = 20
                  
        else:
            '''the third usage is to display whose turn it is'''
            self.__type = 0
            self.__side = variable
            self.__image1 = pygame.image.load("Sprites/system/goal.gif")
            self.__label1 = xl_font.render("Blue's Turn",1,(0,0,0))
            self.__image2 = pygame.image.load("Sprites/system/goal_red.gif")
            self.__label2 = xl_font.render("Red's Turn",1,(0,0,0))
            
            self.__image1.blit(self.__label1,(25,25))
            self.__image2.blit(self.__label2,(25,25))
            
            if self.__side:
                self.image = self.__image2
                
            else:
                self.image = self.__image1
            self.rect = self.image.get_rect()
            
            self.rect.top = 20
            self.rect.right = screen.get_width()-20

            
    def set_status(self,grid_status):
        '''display grid bonus'''
        self.__label1 = medium_font.render(grid_status[0],1,(0,0,0))
        self.__label2 = small_font.render("DEF.    "+str(grid_status[1]),1,(0,0,0))
        self.__label3 = small_font.render("AVO.    "+str(grid_status[2]),1,(0,0,0))
    
    def change(self,var):
        '''change grid bonus'''
        if self.__type:
            if var == "Plains":
                self.image = self.__image1
            elif var == "Sea":
                self.image = self.__image4
            elif var == "Forest":
                self.image = self.__image2
            else:
                self.image = self.__image3
    
    def switch_sides(self,player_side):
        '''change turn'''
        if player_side:
            self.image = self.__image2
        else:
            self.image = self.__image1

class Text(pygame.sprite.Sprite):
    '''this is used along with Display class for text'''
    def __init__(self,usage,screen,side,char,hp,max_hp):
        pygame.sprite.Sprite.__init__(self)
        if usage:
            self.set_title(char,side)
            self.rect = self.image.get_rect()
            self.rect.centerx = 85
            self.rect.top = screen.get_height()-225
        else:
            self.__max_hp = max_hp
            self.__hp = hp            
            self.change_hp()
            self.rect = self.image.get_rect()
            self.rect.left = 25
            self.rect.top = screen.get_height()-185
    
    def set_title(self,char,side):
        if char:
            if char==1:
                self.__title = "Axe"
            if char==2:
                self.__title = "Lancer"
            if char==3:
                self.__title = "Swordsman"
        elif side:
            self.__title = "Hero"
        else:
            self.__title = "Boss"
            
        self.image = large_font.render(self.__title,1,(0,0,0))
    
    def change_hp(self):
        self.image = large_font.render("HP: "+str(self.__hp)+"/"+str(self.__max_hp),1,(0,0,0))

class Menu(pygame.sprite.Sprite):
    '''this class is used for option selection during battle phases'''
    def __init__(self,screen,coordinates):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Sprites/system/options.gif").convert()
        self.rect = self.image.get_rect()
        
        self.rect.left = (coordinates[0]+1)*50+5
        if self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()
            
        self.rect.top = coordinates[1]*50+5
        if self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()
            
    def give_pos(self):
        return (self.rect.left, self.rect.top)

class Arrow(pygame.sprite.Sprite):
    '''this class is used along with Menu class for option selections'''
    def __init__(self,position,option):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Sprites/system/arrow.gif")
        self.rect = self.image.get_rect()
        
        self.rect.left = position[0]+80
        self.rect.top = position[1]+22+option*40

class Battle(pygame.sprite.Sprite):
    '''this text class is used to display the status of the battle'''
    def __init__(self,screen,hit,damage,crit,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100,40))
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        
        if crit:
            self.__color = (250, 150, 0)
        else:
            self.__color = (0,0,0)
        
        if hit:
            self.__label = dank_font.render("-"+str(damage),0,self.__color)
        else:
            self.__label = dank_font.render("MISS",0,self.__color)
        
        self.image.blit(self.__label,(0,0))
        
        self.rect.left = pos[0]*50+5
        self.rect.top = pos[1]*50
        
        if self.rect.right > screen.get_width():
            self.rect.right = screen.get_width
            self.rect.top += 50
            if self.rect.bottom > screen.get_height():
                self.rect.top -= 50
        if self.rect.bottom > screen.get_height():
            self.rect.top -= 50
        self.__count = 15
        
    def update(self):
        self.__count -=1
        if self.__count <= 0:
            self.kill()