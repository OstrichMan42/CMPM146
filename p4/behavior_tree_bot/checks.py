

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


def planet_will_lose(state):
    for fleet in state.enemy_fleets():
        if fleet.turns_remaining * fleet.target_planet.growth_rate + fleet.target_planet.num_ships < fleet.num_ships:
            return True
    return False
