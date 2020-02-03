

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())


# def have_required_ships(state):
#     if target_planet.owner == 0:
#         required_ships = target_planet.num_ships + 1
#     else:
#         required_ships = target_planet.num_ships + \
#                          state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1