import logging

def if_neutral_planet_available(state):
    logging.info('neutral available ')
    return any(state.neutral_planets())


def have_largest_fleet(state):
    logging.info('have largest ')
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())


#
def making_more_ships(state):
    logging.info('makin more')
    return sum(planet.growth_rate for planet in state.my_planets()) > sum(planet.growth_rate for planet in state.enemy_planets())


def have_advantage(state):
    logging.info('have advantage')
    return making_more_ships(state) and have_largest_fleet(state)


# returns whether or not any of our planets would be taken
def planet_will_lose(state):
    logging.info('will lose ')
    for fleet in state.enemy_fleets():
        if fleet.turns_remaining * fleet.target_planet.growth_rate + fleet.target_planet.num_ships < fleet.num_ships:
            return True
    return False

<<<<<<< HEAD
def defend_boi_available(state):
    logging.info('defend available ')
    #wouldDie = []
    for planet in state.my_planets():
        #turn = 0
        for size in effective_size(state, planet):
            if size < 1 and reaction_time(state, planet) > -1:
                return True  # wouldDie.append((planet, turn))
    return False
            #turn += 1
=======

def defend_boi_available(state):
    logging.info('defend check ')
    for planet in state.my_planets():
        for size in effective_size(state, planet):
            if size < 1: #  and reaction_time(state, planet) > -5
                logging.info('defend available ')
                return True
    return False
>>>>>>> master



#questions for dan: vector?, debug?, neutral planet growth rate
# determines if we could send a fleet to arrive at a neutral planet to take it just after the enemy
def snipe_available(state):
    logging.info('checking snipe available')
    # make empty dict for storing, stores amount of enemy ships that will be in the planet once all fleets arrive
    snipes = {}
    for fleet in state.enemy_fleets():
        target = state.planets[fleet.destination_planet]
        if target.owner == 0 and -3 < reaction_time(state, target):
            if target not in snipes:
                snipes[target] = fleet.num_ships - target.num_ships
            else:
                snipes[target] += fleet.num_ships

    for snipe in snipes:
        if reaction_time(state, snipe) > 0 and snipes[snipe] < 21:
            return True

    return False


# returns enemy_reaction_time - our_reaction_time
def reaction_time(state, target_planet):
    #logging.info('reaction time ')
    enemyPlanet = closest_enemy(state, target_planet)
    myPlanet = closest_friendly(state, target_planet)

    enemyReaction = state.distance(enemyPlanet.ID, target_planet.ID)
    myReaction = state.distance(myPlanet.ID, target_planet.ID)

    return enemyReaction - myReaction


# returns target_planet's closest relevant friendly neighbor
def closest_friendly(state, target_planet):
    #logging.info('closest friendly ')
    bestPlanet = target_planet
    myReaction = 200
    for myPlanet in state.my_planets():
        if myPlanet == target_planet:  # don't count itself
            continue
        if state.distance(myPlanet.ID, target_planet.ID) < myReaction and myPlanet.num_ships > target_planet.num_ships * 0.1:
            bestPlanet = myPlanet
            myReaction = state.distance(myPlanet.ID, target_planet.ID)
    return bestPlanet


# returns target_planet's closest relevant hostile neighbor
def closest_enemy(state, target_planet):
    #logging.info('closest_enemy ')
    bestPlanet = target_planet
    enemyReaction = 200
    for enemyPlanet in state.enemy_planets():
        if enemyPlanet == target_planet:  # don't count itself
            continue
        if state.distance(enemyPlanet.ID, target_planet.ID) < enemyReaction and enemyPlanet.num_ships > target_planet.num_ships / 10:
            bestPlanet = enemyPlanet
            enemyReaction = state.distance(enemyPlanet.ID, target_planet.ID)
    return bestPlanet


# return size of planet after all fleets arrive
def effective_size(state, planet):
    #logging.info('effective size ')
    sizeAtTurn = []
    if planet.owner == 1: #friendly planet
        sizeAtTurn = [planet.num_ships, planet.num_ships + planet.growth_rate, planet.num_ships + planet.growth_rate * 2,
                      planet.num_ships + planet.growth_rate * 3, planet.num_ships + planet.growth_rate * 4,
                      planet.num_ships + planet.growth_rate * 5, planet.num_ships + planet.growth_rate * 6,
                      planet.num_ships + planet.growth_rate * 7, planet.num_ships + planet.growth_rate * 8,
                      planet.num_ships + planet.growth_rate * 9]
    elif planet.owner == 2: #enemy planet
        sizeAtTurn = [-planet.num_ships, -(planet.num_ships + planet.growth_rate),
                      -(planet.num_ships + planet.growth_rate * 2), -(planet.num_ships + planet.growth_rate * 3),
                      -(planet.num_ships + planet.growth_rate * 4), -(planet.num_ships + planet.growth_rate * 5),
                      -(planet.num_ships + planet.growth_rate * 6), -(planet.num_ships + planet.growth_rate * 7),
                      -(planet.num_ships + planet.growth_rate * 8), -(planet.num_ships + planet.growth_rate * 9)]
    else: #neutral planet
        sizeAtTurn[0:9] = planet.num_ships

    for fleet in state.fleets:
        if fleet.destination_planet == planet and fleet.turns_remaining < 10:
            if planet.owner == 0:
                sizeAtTurn[fleet.turns_remaining] -= fleet.num_ships
            elif fleet.owner == 1:
                sizeAtTurn[fleet.turns_remaining] += fleet.num_ships
            else:
                sizeAtTurn[fleet.turns_remaining] -= fleet.num_ships

    return sizeAtTurn
