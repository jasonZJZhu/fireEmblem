'''
Jason Zhu
Fire Emblem!(16x12)
'''
# I - import and initialize
import pygame, mySprites, attack
pygame.init()
pygame.mixer.init(48000,16,2,4096)

# D - display configuration
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Fire Emblem! ")

# E - entities
background = pygame.Surface(screen.get_size())
background.fill((255,255,255))
background = background.convert()
screen.blit(background,(0,0))

# A - action
# A - Assign
clock = pygame.time.Clock()

def main():
    '''Mailine logic of the game, it first initializes the map, then calls the main game loop, when the game loop ends, it calls the end game page before exiting'''
    # more assign
    pygame.mouse.set_visible(False)
    
    # more entities
    hit = pygame.mixer.Sound("Sounds/Attack_Hit_1.wav")
    hit.set_volume(0.7)
    miss = pygame.mixer.Sound("Sounds/Attack_Miss_2.wav")
    miss.set_volume(0.7)
    death = pygame.mixer.Sound("Sounds/Death.wav")
    death.set_volume(0.7)
    win = pygame.mixer.Sound("Sounds/Level_Up.wav")
    win.set_volume(0.7)    
    crit = pygame.mixer.Sound("Sounds/Final_Hit.wav")
    crit.set_volume(0.7)
    switch= pygame.mixer.Sound("Sounds/Next_Turn.wav")
    switch.set_volume(0.7)
    
    # CALLS intro game loop and allows the players to choose a map
    gameMap = intro()
    if gameMap:
        pygame.mixer.music.load("Sounds/The_Dawn.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)        
        gridGroup, grids, heroGroup, enemyGroup = open_map(gameMap)        
        keepGoing = True        
    
        # calls all the initially required sprites
        clear = mySprites.Clear(screen)
        enemy_count = len(enemyGroup)
        displays = []
        displayGroup,char_stats = display_text(displays,1,screen,grids[6][8].get_status(),0)
        selector = mySprites.Selector()
    
        allSprites = pygame.sprite.OrderedUpdates(clear,gridGroup, heroGroup,\
                                              enemyGroup, selector,displayGroup)
    
    
        # CALLS our game loop 
        winner = game(clear,allSprites,gridGroup,selector,heroGroup,enemyGroup,grids,keepGoing,displayGroup,enemy_count,displays,hit,miss,death,win,crit,switch)
    
        # when the game loop ends, calls the end game page
        pygame.mixer.music.load("Sounds/Happy_End_Of_The_World.mp3")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)
        victory(winner,screen)
    
    # closes the game
    pygame.mouse.set_visible(True)
    pygame.time.delay(1000)
    pygame.quit()

def intro():
    '''this function is the intro loop of the game, giving the players instructions and explanations'''
    pygame.mixer.music.load("Sounds/Happy_End_Of_The_World.mp3")
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)
    selection_page = pygame.image.load("Sprites/system/intro.gif").convert()
    keepGoing = True
    gameMap = False
    while keepGoing:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                elif event.key == pygame.K_c:
                    '''when the players are done with the instructions, they will be moving onto the map selections'''
                    gameMap = selection(keepGoing)
                    keepGoing = False
        
        screen.blit(selection_page,(0,0))
        pygame.display.flip()
    pygame.mixer.music.fadeout(1000)
    return gameMap

def selection(keepGoing):
    '''this function is the map selection loops, where the player can choose where the battle will be take place. In addition, the players can actually create their own maps OUTSIDE of Python in the maps folder'''
    background = pygame.image.load("Sprites/system/selection.gif").convert()
    while keepGoing:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                elif event.key == pygame.K_1:
                    return "maps/cliffs.txt"
                elif event.key == pygame.K_2:
                    return "maps/arena.txt"
                elif event.key == pygame.K_3:
                    return "maps/blue_test.txt"
                elif event.key == pygame.K_4:
                    return "maps/red_test.txt"
                
        screen.blit(background,(0,0))
        pygame.display.flip()
    '''returns False if no map is chosen by the player'''
    return False
                
def open_map(gameMap):
    '''this function is used to initialize the map, creating grids and pieces for both sides'''
    map_used = open(gameMap,"r")
    if gameMap == "maps/arena.txt":
        pygame.mixer.music.load("Sounds/Trifecta.mp3")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)        
    
    friendly = []
    enemy = []
    
    heros = []
    enemies = []
    grids = []
    x = 0
    y = 0
    
    '''reads from the .txt files and prints out a 16x12 grid, wow!'''
    for line in map_used:
        y += 1
        grids.append([])
        for item in line.split():
            if x == 16:
                x = 0
            x += 1
            grids[y-1].append(mySprites.Grid(screen,x,y, item))
            try:
                if int(item)-20 >= 0:
                    enemy.append((x,y,item))
                
                elif int(item)-10 >= 0:
                    friendly.append((x,y,item))
            except:
                pass
            
    for status in friendly:
        character = mySprites.Character(status,1)
        heros.append(character)
        grids[status[1]-1][status[0]-1].receive(character)
        
    for status in enemy:
        character = mySprites.Character(status,0)
        enemies.append(character)
        grids[status[1]-1][status[0]-1].receive(character)
    
    gridGroup = pygame.sprite.Group(grids)
    heroGroup = pygame.sprite.Group(heros)
    enemyGroup = pygame.sprite.Group(enemies)
    return gridGroup, grids, heroGroup, enemyGroup
    
def game(clear,allSprites,gridGroup,selector,heroGroup,enemyGroup,grids,keepGoing,displayGroup,enemy_count,displays,hit,miss,death,win,crit,switch):
    '''This function is where the majority of the game takes place, it creates many variables that are required for the game later on'''
    squareGroup = None
    turn_display = 0
    squares = []
    covered = []
    available = []
    selected = False
    character = False
    initial = False
    final = False
    grid_status = False
    option = 0
    reset_count = 30
    player_side = 0
    side = 0
    animation_phase = 0
    battle_phase=[]
    message = False
    # this variable is used to delay the events
    counter = 15
    winner = False
    # this variable is used to delay the events
    end = 90
    
    # L - Loop
    while keepGoing:
        # T - Time
        clock.tick(30)
        
        # E - calls the player function for event handling
        keepGoing,squareGroup,turn_display,squares,covered,selected,character,initial,final,available,option,player_side,side,battle_phase,animation_phase= player(selector,grids,keepGoing,squareGroup,clear,turn_display,squares,covered,selected,character,initial,final,available,option,player_side,side,battle_phase,animation_phase)
        if keepGoing==False:
            pygame.mixer.music.fadeout(1000)
        
        '''checks if a battle has taken place, if true then calls the animation function'''
        if animation_phase != 0:
            animation_phase,message,counter = battle(screen,battle_phase,animation_phase,message,grids,counter,clear,hit,miss,death,crit)           
        
        '''checks if one side has been defeated/ran out of pieces, if true then calls the end game page with the winner'''
        if len(heroGroup) ==0:
            winner = 2
            end = pause(end,1,win)
            if end == 0:
                keepGoing = False
        elif len(enemyGroup) ==0:
            winner = 1
            end = pause(end,1,win)
            if end ==0:
                keepGoing = False           
        
        '''checks if all characters on one side has made its move'''
        if player_side:
            moves = len(enemyGroup)
            for hero in enemyGroup:
                if hero.check_moved()[1]:
                    moves -= 1
        else:
            moves = len(heroGroup)
            for hero in heroGroup:
                if hero.check_moved()[1]:
                    moves -=1
        '''resets the characters and switches turns when one side has mvoed all of its pieces'''
        if moves == 0:
            reset_count -= 1
            if reset_count == 20:
                # plays sound effect
                switch.play()                
            if reset_count == 0:
                reset_count = 30
                if player_side:                
                    player_side = 0
                else:            
                    player_side = 1                 
                for hero in heroGroup:
                    hero.reset()        
                for hero in enemyGroup:
                    hero.reset()              
              
        
        '''calls the information displays if a character isn't moving'''
        if turn_display == 0 or turn_display==3:
            temp_grid = pygame.sprite.spritecollide(selector,gridGroup,False)
            grid_status = temp_grid[0].get_status()
            displayGroup.clear(screen,background)
            displayGroup,statsGroup = display_text(displays,0,screen, grid_status,player_side)
            
        '''The codes below determines what are displayed onto the screen'''
        if turn_display:
            # show grids for movement
            if turn_display==1:
                displayGroup.clear(screen,background)
                allSprites = pygame.sprite.OrderedUpdates(clear,gridGroup,heroGroup,enemyGroup, squareGroup, selector)
            # show menu for action selection
            elif turn_display==2:
                if character:
                    if character.check_moved()[2]:
                        menuGroup,menu = show_menu(screen,character.get_pos(),option)
                        allSprites = pygame.sprite.OrderedUpdates(clear,gridGroup,heroGroup,enemyGroup,displayGroup,statsGroup,menuGroup)
            # show grids for attacking
            elif turn_display==3:
                allSprites= pygame.sprite.OrderedUpdates(clear,gridGroup,heroGroup,enemyGroup,squareGroup,selector,displayGroup,statsGroup)
        # show character information if selector is on top of the character
        elif statsGroup:
            allSprites = pygame.sprite.OrderedUpdates(clear,gridGroup,heroGroup,enemyGroup, selector, displayGroup, statsGroup)
        # show normal map with displays
        else:
            allSprites = pygame.sprite.OrderedUpdates(clear,gridGroup,heroGroup,enemyGroup, selector, displayGroup)
        # show battle info if there are any
        if message:
            allSprites.add(message)
        
        # R - refresh dislplay
        allSprites.clear(screen,background)
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
        
    #returns 1 or 2 representing which side has won, false if there's no winner
    return winner

def player(selector,grids,keepGoing,squareGroup,clear,turn_display,squares,covered,selected,character,initial,final,available,option,player_side,side,battle_phase,animation_phase):
    '''This function is used to handle all the events given from the player during the main game phase'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepGoing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                keepGoing = False
            elif event.key == pygame.K_LEFT:
                selector.change_xpos(-1)
                    
            elif event.key == pygame.K_RIGHT:
                selector.change_xpos(1)
                    
            elif event.key == pygame.K_UP:
                if turn_display!=2:
                    selector.change_ypos(-1)
                elif option:
                    option = 0
                else:
                    option = 1                    
                    
            elif event.key == pygame.K_DOWN:
                if turn_display!=2:
                    selector.change_ypos(1)
                elif option:
                    option = 0
                else:   
                    option = 1                       
                
            elif event.key == pygame.K_c:
                '''majority of the events are revolved around the key C, so there are many variables decleared here'''
                # gets location of the grid that is selected
                x, y = selector.selected()
                selected = grids[y][x].get_status()
                '''turn_display is the variable used to determine what phase of the game is and what it is displaying at the moment.'''
                if turn_display == 0:
                    '''0 means nothing is happening, player can still choose pieces'''
                    initial = (x,y)
                    if selected[1]:
                        character = selected[1]
                        if character.get_status()[0] - 20 >= 0:
                            side = 1
                        else:
                            side = 0
                        turn_display = 1                            
                        squareGroup,squares,covered,available = display_squares(character.get_pos(),grids,character.get_status()[1],side,covered,available,player_side)
                elif turn_display ==1:
                    '''1 means a piece is chosen, the play can now select a movement grid. Many codes here are used for limitation of the piece's movements'''  
                    final = (x,y)
                    turn_display=0
                    if final in available:
                        if character.check_moved()[0] == False: 
                            if side == player_side:
                                turn_display =2    
                                '''moves the character'''
                                character.move((final[0]-initial[0],final[1]-initial[1]))
                                '''updates character onto the grid and give it with the power boost'''
                                grids[y][x].receive(character)
                                character.change_bonus(grids[y][x].display())
                                
                                if final != initial:
                                    grids[initial[1]][initial[0]].remove()
                                    available.remove(final)
                    elif final == initial:
                        turn_display = 0
                        if side == player_side:
                            if character.check_moved()[0] == False:
                                turn_display = 2
                                
                    if squareGroup:
                        for square in squares:
                            square.kill()
                        for grid in covered:
                            grid.reset_squares()
                        selected = False
                    available = []
                    
                elif turn_display ==2:
                    '''2 means the piece has moved, and now is able to attack or wait'''
                    if character.check_moved()[1]==False:
                        if option:
                            character.turnover()
                            option = 0
                            turn_display = 0
                        else:
                            squareGroup,squares,covered,available=show_range(character,grids)
                            turn_display = 3
                        
                elif turn_display ==3:
                    '''3 means the piece has decided to attack, display attackable grids'''
                    final = (x,y)
                    if final in available:
                        if selected[1]:               
                            if selected[1].get_status()[0] - 20 >= 0:
                                side = 1
                            else:   
                                side = 0
                            if side != player_side:
                                '''calls the attack module to do the calculations of the battle and putting it all into one list'''
                                battle_phase=attack.pre_attack(character,selected[1])
                                battle_phase.append(character)
                                battle_phase.append(selected[1])
                                # changes the value to trigger battle animations
                                animation_phase = 1
                                # resets the turn display
                                turn_display = 0                            
                
            elif event.key == pygame.K_x:
                '''the key X is used to clear all displays on the screen and start all over again'''
                if turn_display == 1:
                    turn_display = 0
                elif turn_display == 2 or turn_display ==3:
                    character.turnover()
                    option = 0
                    turn_display = 0
                
                if squareGroup:
                    for square in squares:
                        square.kill()
                    for grid in covered:
                        grid.reset_squares()
                    selected = False
                    character = False
                available = []

    return keepGoing, squareGroup, turn_display,squares,covered,selected,character,initial,final,available,option,player_side,side,battle_phase,animation_phase

def show_range(character,grids):
    '''this function is used to show the attackable range of characters'''
    available = []
    covered =  []
    squares = []
    (x,y) = character.get_pos()
    '''first it checks whether the piece is a big guy, if so they are allowed to attack in diagonals'''
    if character.get_status()[0] == 10 or character.get_status()[0] == 20:
        if x-1 >= 0 and y-1 >=0:
            square = mySprites.Square(x-1,y-1,1)
            squares.append(square)
            covered.append(grids[y-1][x-1])
            grids[y-1][x-1].cover(0,1,square)
            if (x-1,y-1) not in available:
                available.append((x-1,y-1))
                
        if x-1 >= 0 and x+1 <= 11:
            square = mySprites.Square(x-1,y+1,1)
            squares.append(square)
            covered.append(grids[y+1][x-1])
            grids[y+1][x-1].cover(0,1,square)        
            if (x-1,y+1) not in available:
                available.append((x-1,y+1))        
        
        if x+1 <= 15 and y-1 >= 0:
            square = mySprites.Square(x+1,y-1,1)
            squares.append(square)
            covered.append(grids[y-1][x+1])       
            grids[y-1][x+1].cover(0,1,square)        
            if (x+1,y-1) not in available:
                available.append((x+1,y-1))
        
        if x+1 <=15 and y+1 <=11:
            square = mySprites.Square(x+1,y+1,1)
            squares.append(square)
            covered.append(grids[y+1][x+1])
            grids[y+1][x+1].cover(0,1,square)
            if (x+1,y+1) not in available:
                available.append((x+1,y+1))
                
    '''no matter if the piece selected is big, they all get to attack straight'''
    if y-1 >=0:        
        square = mySprites.Square(x,y-1,1)
        squares.append(square)
        covered.append(grids[y-1][x])
        grids[y-1][x].cover(0,1,square)
        if (x,y-1) not in available:
            available.append((x,y-1))
    
    if x-1 >=0:
        square = mySprites.Square(x-1,y,1)
        squares.append(square)
        covered.append(grids[y][x-1])
        grids[y][x-1].cover(0,1,square)
        if (x-1,y) not in available:
            available.append((x-1,y))  
     
    if y+1 <= 11:        
        square = mySprites.Square(x,y+1,1)
        squares.append(square)
        covered.append(grids[y+1][x])
        grids[y+1][x].cover(0,1,square)
        if (x,y+1) not in available:
            available.append((x,y+1))
    
    if x+1 <= 15:
        square = mySprites.Square(x+1,y,1)
        squares.append(square)
        covered.append(grids[y][x+1])
        grids[y][x+1].cover(0,1,square)
        if (x+1,y) not in available:
            available.append((x+1,y))           
    
    
    squareGroup = pygame.sprite.Group(squares)
    return squareGroup,squares,covered,available
                
def display_squares(origin,grids,move,side,covered,available,player_side):
    '''this function is used to display the moveable squares for a piece'''
    squares = []
    origin_x = origin[0]
    origin_y = origin[1]
    '''lots of math involved, 4 for loops handling all 4 directions, if the gird is sea or mountain, then the unit cannot move onto it'''
    for dx in xrange(1,move+1):
        x = origin_x - dx
        if x >= 0 and x <= 15:
            square = mySprites.Square(x,origin_y,side)
            if grids[origin_y][x].cover(1,side,square):
                pass
            else:
                squares.append(square)                 
                covered.append(grids[origin_y][x])
                if side == player_side:
                    if (x,origin_y) not in available:
                        available.append((x,origin_y))
        
    for dx in xrange(1,move+1):
        x = origin_x + dx
        if x >= 0 and x <= 15:
            square = mySprites.Square(x,origin_y,side)
            if grids[origin_y][x].cover(1,side,square):
                pass
            else:
                squares.append(square)                 
                covered.append(grids[origin_y][x])
                if side == player_side:
                    if (x,origin_y) not in available:
                        available.append((x,origin_y))
                
    for dy in xrange(1,move+1):
        y = origin_y - dy
        for x in xrange(origin_x-(move-dy),origin_x+(move-dy)+1):
            if (x >= 0 and x <= 15) and (y >= 0 and y <= 11):
                square = mySprites.Square(x,y,side)
                if grids[y][x].cover(1,side,square):
                    pass
                else:
                    squares.append(square)                    
                    covered.append(grids[y][x])
                    if side == player_side:
                        if (x,y) not in available:
                            available.append((x,y))
                    
            
    for dy in xrange(1,move+1):
        y = origin_y + dy
        for x in xrange(origin_x-(move-dy),origin_x+(move-dy)+1):
            if (x >= 0 and x <= 15) and (y >= 0 and y <= 11):
                square = mySprites.Square(x,y,side)
                if grids[y][x].cover(1,side,square):
                    pass
                else:
                    squares.append(square)                    
                    covered.append(grids[y][x])
                    if side == player_side:
                        if (x,y) not in available:
                            available.append((x,y))
                    
    squareGroup = pygame.sprite.Group(squares)
    return squareGroup,squares,covered,available

def display_text(displays,first_time,screen,grid_status,player_side):
    '''this function is used to display all the information about a landscape, a character, and whose turn it currently is'''
    char_stats = []
    for display in displays:
        '''resets the screen of displays before creating new ones'''
        display.kill()
    if first_time:
        '''some displays only need to be created once'''
        grid = mySprites.Display(screen,1,grid_status[3])
        displays.append(grid)
        goal = mySprites.Display(screen,0,player_side)
        displays.append(goal)        
    else:
        '''after the first time being called, all sprites can change accordingly'''
        displays[0].change(grid_status[3])
        displays[1].switch_sides(player_side)
        if grid_status[1]:
            char_status =  grid_status[1].get_status()
            char = char_status[0] - 20
            if char >= 0:
                side = 0
                max_hp = char_status[3]
                hp = char_status[4]
            else:
                side = 1
                char+= 10
                max_hp = char_status[3]
                hp = char_status[4]
            stats_box = mySprites.Display(screen,2,side)
            char_stats.append(stats_box)
            
            title = mySprites.Text(1,screen,side,char,0,0)
            stats_text = mySprites.Text(0,screen,0,0,hp,max_hp)
            
            char_stats.append(title)
            char_stats.append(stats_text)
    
    displayGroup = pygame.sprite.Group(displays)
    statsGroup = pygame.sprite.OrderedUpdates(char_stats)
    return displayGroup, statsGroup

def show_menu(screen,coordinates,option):
    '''this function is used to show and select the options a piece has during phase 2 of turn display'''
    menu_objects = []
    menu = mySprites.Menu(screen,coordinates)
    menu_objects.append(menu)
    
    arrow = mySprites.Arrow(menu.give_pos(),option)
    menu_objects.append(arrow)
    
    menuGroup = pygame.sprite.OrderedUpdates(menu_objects,arrow)    
    return menuGroup,menu_objects

def pause(counter,end,win):
    '''this function is used to delay events, also transitions into the endgame loop if keepGoing is False'''
    counter -=1
    if end:
        pygame.mixer.music.fadeout(1000)
        if counter == 59:
            win.play()
    return counter
    
def battle(screen,info,phase,message,grids,counter,clear,hit,miss,death,crit):
    '''this function is used to handle the battle animations when called with all the information about the outcome of the battle'''
    
    '''INFO: attack hit, damage, crit, reflect hit, damage, crit, multihit, attack hit, damage, crit, attacker, enemy'''
    
    if phase ==1:
        '''phase 1 of battle is when the attacker attacks the defender, check for miss and critical strikes'''
        message = mySprites.Battle(screen,info[0],info[1],info[2],info[11].get_pos())
        phase = 2
        if info[0]:
            if info[2]:
                crit.play()
            else:
                hit.play()
            info[10].attack(info[11].get_pos())
            if info[10].check_moved()[2]:
                dead = info[11].defend(info[1])
                if dead:
                    grids[dead[1]][dead[0]].remove()
                    death.play()
                    info[10].turnover()
                    phase = 0
        else:
            miss.play()
    
    elif phase ==2:
        '''phase 2 of battle is when the defender returns a hit, check for miss and critical strikes'''
        counter = pause(counter,0,0)
        if counter == 0:
            if info[6]:
                phase = 3
            else:
                phase = 0
                info[10].turnover()
            
            message = mySprites.Battle(screen,info[3],info[4],info[5],info[10].get_pos())
            if info[3]:
                if info[5]:
                    crit.play()
                else:
                    hit.play()
                info[11].attack(info[10].get_pos())
                if info[11].check_moved()[2]:
                    dead = info[10].defend(info[4])
                    if dead:
                        grids[dead[1]][dead[0]].remove()
                        death.play()
                        phase = 0
                    else:
                        info[10].turnover()
            else:
                miss.play()
            counter = 15
   
    elif phase ==3:
        '''phase 3 of battle is when the attacker attacks the defender again due to its overwhelming speed, check for miss and critical strikes'''
        counter = pause(counter,0,0)
        if counter ==0:
            message = mySprites.Battle(screen,info[7],info[8],info[9],info[11].get_pos())
            if info[7]:
                if info[9]:
                    crit.play()
                else:
                    hit.play()
                info[10].attack(info[11].get_pos())
                if info[10].check_moved()[2]:
                    dead = info[11].defend(info[1])
                    if dead:
                        grids[dead[1]][dead[0]].remove()
                        death.play()
                    info[10].turnover()
            else:
                miss.play()
            phase = 0
            counter = 15
    return phase,message,counter

def victory(winner,screen):
    '''this is the endgame loop, displays the victor and waits for the final quit command from the player'''
    keepGoing = True
    if winner==2:
        end = pygame.image.load("Sprites/system/end_red.gif")
        end = end.convert()
    elif winner ==1:
        end = pygame.image.load("Sprites/system/end_blue.gif")
        end = end.convert()
    else:
        end = pygame.image.load("Sprites/system/end.gif")
        end = end.convert()
    while keepGoing:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_c:
                    keepGoing = False
                
        screen.blit(end,(0,0))
        pygame.display.flip()
main()