'''
Fire Emblem Attack Module
This module is the calculations module for every battle
'''
import random
def pre_attack(hero,enemy):
    '''VALUES: type,current health, max health, attack, defence, speed, crit chance, hit rate, dodge rate'''
    
    '''this function is the MAIN logic for the whole module, checks for misses, crits, and calculations, then returning all of the values back to our main module'''
    attacker = hero.get_value()
    defender = enemy.get_value()
    multihit = followup(attacker[5],defender[5])
    battle_phase = []
    
    for hits in range(multihit):
        if dodge(attacker[7],defender[8]):
            if hits:
                hit3 = False
                damage2 = 0
                multihit = False
                crit3 = False
            else:
                hit1 = False
                damage1 = 0
                crit1 = 0
                multihit = False
                hit3 = False
                damage2 = 0
                crit3 = False
        else:       
            crit,damage= attack(attacker[3],defender[4],attacker[6])
            if hits:
                hit3 = True
                multihit = True
                damage2 = damage
                crit3 = crit
            else:
                hit3 = False
                crit3 = False
                hit1 = True
                damage1 = damage
                crit1= crit
                damage2 = 0
                multihit = False
    
    if dodge(defender[7],attacker[8]):
        hit2 = False
    else:
        hit2 = True
        
    crit2,reflect = attack(defender[3],attacker[4],defender[6])
    if damage1 < 0:
        reflect = 0
    if reflect < 0:
        reflect = 0
    if damage2 < 0:
        reflect = 0
    '''Here I had to append all values because if not then it will become a tuple and will not be any use by our main module'''
    battle_phase.append(hit1)
    battle_phase.append(damage1)
    battle_phase.append(crit1)
    battle_phase.append(hit2)
    battle_phase.append(reflect)
    battle_phase.append(crit2)
    battle_phase.append(multihit)
    battle_phase.append(hit3)
    battle_phase.append(damage2)
    battle_phase.append(crit3)
    return battle_phase

def dodge(hit,miss):    
    '''this functions checks whether a hit missed or not based on the dodge %'''
    if random.randrange(100) > (hit-miss):
        return True
    else:
        return False

def followup(speed1,speed2):
    '''this function checks whether the attacker is able to land two hits based on speed %'''
    if random.randrange(100) > (speed1-speed2):
        return 1
    else:
        return 2

def attack(attack,defence,crit_chance):
    '''this functions returns the damage that's been done by an attack'''
    crit = check_crit(attack,crit_chance)
    return crit[0],crit[1]-defence

def check_crit(attack,crit_chance):
    '''this function checks for critical strikes based on crit %'''
    if random.randrange(100) > crit_chance:
        return False,attack
    else:
        return True,attack*2