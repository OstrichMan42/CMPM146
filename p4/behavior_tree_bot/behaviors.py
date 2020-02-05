# Warner & Caetano behaviors.py
# 3 February 2020

import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
from  math import ceil, sqrt

def helper_best(player_planet, target_planet, reaction_time)


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    #if len(state.my_fleets()) >= 1:
        #return False                  # commented out because we want to be able to attack/defend regardless


    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    #if len(state.my_fleets()) >= 1:
    #    return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, weakest_planet.num_ships + 1)

def spread_best_neutral(state):
    # closest & weakest neutral is target
    chosen_one = None
    #for chosen_one in state.neutral_planets():

    return
def attack_best_enemy(state):
    # closest & weakest enemy is the target
    return
def balance_our_planets(state): # warner
    # check if one planet has less than the average.
    # find the difference, average that dif value and average it by total num of our planets
    #       send that average ship number from every our_planet to the weak_planet while
    #       the planet_ship_count is < average for the weak_planet
    return
def combined_attack(state): # warner

    # find a best_enemy_planet, find out its ship value
    # target_planet will be attacked by (target_planet.shipcount + reacting_time(?) )
    return
def defend_boi(state): # warner
    '''
    spread to an our_ship that is being attacked and is saveable



    if our_target.reaction_time <= 0:          #(<=)? idk the affect of reactiontime == 0
        not saveable, ignore the boi (sadface)
    else if reaction_time > 0:
        #SAVE THE BOI!


    ?(saveable():
    if our_ship is within saveable distance
        return true
    else:
    false)?
    '''
    return

def snipe_boi(state): #caetano
    return