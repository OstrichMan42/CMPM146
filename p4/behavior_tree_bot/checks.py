def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())


def making_more_ships(state):
    return sum(planet.growth_rate for planet in state.my_planets()) > sum(planet.growth_rate for planet in state.enemy_planets())


def have_advantage(state):
    return making_more_ships(state) and have_largest_fleet(state)


# returns whether or not any of our planets would be taken
def planet_will_lose(state):
    for fleet in state.enemy_fleets():
        if fleet.turns_remaining * fleet.target_planet.growth_rate + fleet.target_planet.num_ships < fleet.num_ships:
            return True
    return False


# determines if we could send a fleet to arrive at a neutral planet to take it just after the enemy
def snipe_available(state):
    # make empty dict for storing, stores amount of enemy ships that will be in the planet once all fleets arrive
    snipes = {}
    for fleet in state.enemy_fleets:
        target = fleet.target_planet
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
    enemyPlanet = closest_enemy(state, target_planet)
    myPlanet = closest_friendly(state, target_planet)

    enemyReaction = state.distance(enemyPlanet.ID, target_planet.ID)
    myReaction = state.distance(myPlanet.ID, target_planet.ID)

    return enemyReaction - myReaction


# returns target_planet's closest relevant friendly neighbor
def closest_friendly(state, target_planet):
    bestPlanet = target_planet
    myReaction = 200
    for myPlanet in state.my_planets:
        if state.distance(myPlanet.ID, target_planet.ID) < myReaction and myPlanet.num_ships > target_planet.num_ships * 0.1:
            bestPlanet = myPlanet
            myReaction = state.distance(myPlanet.ID, target_planet.ID)
    return bestPlanet


# returns target_planet's closest relevant hostile neighbor
def closest_enemy(state, target_planet):
    bestPlanet = target_planet
    enemyReaction = 200
    for enemyPlanet in state.enemy_planets:
        if state.distance(enemyPlanet.ID, target_planet.ID) < enemyReaction and enemyPlanet.num_ships > target_planet.num_ships * 0.1:
            bestPlanet = enemyPlanet
            enemyReaction = state.distance(enemyPlanet.ID, target_planet.ID)
    return bestPlanet
