# Warner & Caetano behaviors.py
# 3 February 2020

import logging
import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
from checks import closest_friendly, closest_enemy, reaction_time, effective_size
from  math import ceil, sqrt


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 5:
        return False

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
    # (1) If we currently have 5 fleets in flight, just do nothing.
    if len(state.my_fleets()) >= 5:
        return False

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


#def balance_our_planets(state): # warner
    # check if one planet has less than the average.
    # find the difference, average that dif value and average it by total num of our planets
    #       send that average ship number from every our_planet to the weak_planet while
    #       the planet_ship_count is < average for the weak_planet
    #return


def combined_attack(state): # warner

    # find a best_enemy_planet, find out its ship value
    # target_planet will be attacked by (target_planet.shipcount + reacting_time(?) )
    return


#thresh
def threshold(state, target):
    average = sum(planet.num_ships for planet in state.my_planets()) / len(state.my_planets) # how to write?
    upper = average + (average * 0.2) # upper bound of threshold
    lower = average - (average * 0.2) # lower ^^^^^^^^^^^^^^^^^^
    ret_val = 0 # return value

    if target > upper: # if target is greater than upper threshold --> means it is sufficiently large
        ret_val = 1
    elif target < lower: # if target is fewer than lower threshold --> means too weak
        ret_val = -1
    elif target <= upper and target >= lower: # sweet spot, planets in this range are average size
        ret_val = 0
    else:
        return ret_val
    return ret_val


def defend_boi(state): # warner
    ships_to_send = 0

    counter = 0
    average = 0
    diff    = 0

    weak_list   = []
    strong_list = []
    weakest     = 10000
    strongest   = 0 #(?)


    for planet in state.my_planets(): # stores small ship count in small, big ship count in big

        if threshold(state, planet) < 0:
            weak_list.append(planet)

            if weak_list[planet] < weakest: # finds weakest planet
                weakest = planet.num_ships

        elif threshold(state, planet) > 0:

            strong_list.append(planet)


    # find closest big planet to weakest
    for find_support in state.my_planets(): # find weakest to support
        if find_support.num_ships == weakest:
            for supporter in closest_planets(state, find_support): # from perspective of weakest, find the closest planet that meets threshold

                if supporter in strong_list: # this is one of the strong planets
                    do_thing=1
                if threshold(state, supporter) <= 0: # less than sufficiently large
                    continue

''' # commented out for testing other parts
                elif threshold(state, supporter) > 0: # sufficiently large
                    # need a needed ship_num value
                    needed = 
                    issue_order(state, supporter, find_support, needed)
                else:
                    return
                '''




''' average = sum(planet.num_ships for planet in state.my_planets()) / len(state.my_planets) #planets:ship ratio

    for planet in my_planets():
        if planet.num_ships <= (average - 30):  #weak threshold
            target = planet
            diff = average - target.num_ships
            ships_to_send = diff + reaction_time
            return                              #

        elif planet.num_ships > (average + 30): # strong threshold
            target = None
            return
        counter += 1 
    '''

'''
    spread to an our_planet that is being attacked and is saveable



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
    #return


def snipe_boi(state): #caetano
    # make empty dict for storing, index is a neutral planet targeted by an enemy fleet, stores tuples.
    # [0] is the number of enemy units that will be there when all enemy fleets arrive,
    # [1] is the number of turns until the first enemy fleet arrives
    logging.info('sniping')
    snipes = {}
    for fleet in state.enemy_fleets():
        target = state.planets[fleet.destination_planet]
        if target.owner == 0 and -3 < reaction_time(state, target):
            if target not in snipes:
                snipes[target] = (fleet.num_ships - target.num_ships, fleet.turns_remaining - fleet.turns_remaining * target.growth_rate)
            else:
                snipes[target][0] += fleet.num_ships - fleet.turns_remaining * target.growth_rate
                if snipes[target][1] > fleet.turns_remaining:
                    snipes[target][1] = fleet.turns_remaining

    for snipe in snipes:
        if reaction_time(state, snipe) > 0 and 0 < snipes[snipe][0] < 21:
            closest = closest_planets(state, snipe)
            div = len(closest)
            for boi in closest:
                issue_order(state, boi.ID, snipe.ID, ceil(snipes[snipe][0] + 1 / div))

    return True


def spread_to_best_neutral(state):
    if not state.neutral_planets:
        return False

    bestTarget = state.neutral_planets[0]
    bestTime = reaction_time(state, bestTarget)
    for nPlanet in state.neutral_planets():
        nReaction = reaction_time(state, nPlanet)
        if nReaction > bestTime:
            bestTarget = nPlanet
            bestTime = nReaction

    closest = closest_planets(state, bestTarget)

    lastFleetTime = 0
    armada = []
    for myPlanet in closest:
        #if threshold(myPlanet, bestTarget): #implement threshold
            armada.append(myPlanet)
    combined_move(state, bestTarget, armada)


### Helper Functions ###

# puts all friendly planets in a list sorted by distance to target
def closest_planets(state, target):
    closest = []
    for planet in state.my_planets():
        closest.insert(state.distance(planet.ID, target.ID), planet)

    return closest


# Issues orders to put target's effective size over 1
def combined_move(state, target, armada): # warner
    friendly = False
    if target.owner == 1:
        friendly = True

    lastFleetTime = state.distance(armada[len(armada)-1], target)
    targetSize = target.num_ships
    # send ships from each planet in armada
    #for planet in armada:

    return


