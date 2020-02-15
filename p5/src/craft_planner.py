# structure of A* from https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode

import json
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time
from heapq import heappop, heappush
from math import inf

Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])


class State(OrderedDict):
    """ This class is a thin wrapper around an OrderedDict, which is simply a dictionary which keeps the order in
        which elements are added (for consistent key-value pair comparisons). Here, we have provided functionality
        for hashing, should you need to use a state as a key in another dictionary, e.g. distance[state] = 5. By
        default, dictionaries are not hashable. Additionally, when the state is converted to a string, it removes
        all items with quantity 0.

        Use of this state representation is optional, should you prefer another.
    """

    def __key(self):
        return tuple(self.items())

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.__key() < other.__key()

    def copy(self):
        new_state = State()
        new_state.update(self)
        return new_state

    def __str__(self):
        return str(dict(item for item in self.items() if item[1] > 0))


def make_checker(rule):
    # Implement a function that returns a function to determine whether a state meets a
    # rule's requirements. This code runs once, when the rules are constructed before
    # the search is attempted.

    def check(state):
        # This code is called by graph(state) and runs millions of times.
        # Tip: Do something with rule['Consumes'] and rule['Requires'].
        if "Consumes" in rule:
            for need in rule["Consumes"]:
                if rule["Consumes"][need] > state[need]:
                    return False
        if "Requires" in rule:
            for need in rule["Requires"]:
                if rule["Requires"][need] > state[need]:
                    return False
        return True

    return check


def make_effector(rule):
    # Implement a function that returns a function which transitions from state to
    # new_state given the rule. This code runs once, when the rules are constructed
    # before the search is attempted.

    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].
        next_state = State.copy(state)
        #print(next_state, "here")

        if "Consumes" in rule:
            # iterate through all resources consumed and subtract them from the current state
            for used in rule["Consumes"]:
                next_state[used] -= rule["Consumes"][used]

        # iterate through all resources produced and add them to the current state
        for used in rule["Produces"]:
            next_state[used] += rule["Produces"][used]

        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.

    def is_goal(state):
        # This code is used in the search process and may be called millions of times.
        for need in goal:
            #print("I need ", need)
            if goal[need] > state[need]:
                return False
        return True

    return is_goal


def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


def heuristic(new_state, is_goal):
    est = 1


    if is_goal(new_state):
        return 0

    # Check if the new state would have more of a material than is really necessary
    if new_state["bench"] > 1 or \
            new_state["cart"] > 1 or \
            new_state["coal"] > 1 or \
            new_state["cobble"] > 8 or \
            new_state["furnace"] > 1 or \
            new_state["iron_axe"] > 1 or \
            new_state["iron_pickaxe"] > 1 or \
            new_state["ingot"] > 5 or \
            new_state["ore"] > 1 or \
            new_state["plank"] > 7 or \
            new_state["rail"] > 32 or \
            new_state["stick"] > 4 or \
            new_state["stone_axe"] > 1 or \
            new_state["stone_pickaxe"] > 1 or \
            new_state["wood"] > 1 or \
            new_state["wooden_axe"] > 1 or \
            new_state["wooden_pickaxe"] > 1:
        return inf

    return est

def search(graph, state, is_goal, limit, heuristic):

    start_time = time()

    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state
    queue = []
    estCost = {}
    myCost = {}
    previous = {}
    myCost[state] = 0
    estCost[state] = 0

    heappush(queue, (0, state))
    while time() - start_time < limit:
        dist, current = heappop(queue)

        if is_goal(current):
            print("search took", time() - start_time, 'seconds. Cost is', myCost[current], "and visited", len(myCost))
            return reconstruct_path(previous, current)


        for action, new_state, cost in graph(current):

            tentativeCost = myCost[current] + cost

            if new_state not in myCost or tentativeCost < myCost[new_state]:
                previous[new_state] = (current, action)
                myCost[new_state] = tentativeCost
                estCost[new_state] = tentativeCost + heuristic(new_state, is_goal)
                if new_state not in queue:
                    heappush(queue, (estCost[new_state], new_state))

        pass

    # Failed to find a path
    print(time() - start_time, 'seconds.')
    print("Failed to find a path from", state, 'within time limit.')
    return None


# key is a state and the values are the previous state and the action taken to the key
def reconstruct_path(previous, current):
    total_path = []
    while current in previous:
        # print(current)
        total_path.insert(0, previous[current])
        current, action = previous[current]

    return total_path


if __name__ == '__main__':
    with open('Crafting.json') as f:
        Crafting = json.load(f)

    # List of items that can be in your inventory:
    print('All items:', Crafting['Items'])

    # List of items in your initial inventory with amounts:
    print('Initial inventory:', Crafting['Initial'])

    # List of items needed to be in your inventory at the end of the plan:
    print('Goal:',Crafting['Goal'])

    # Dict of crafting recipes (each is a dict):
    # print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

    # Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)

    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])

    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])

    # Search for a solution
    resulting_plan = search(graph, state, is_goal, 30, heuristic)

    if resulting_plan:
        # Print resulting plan
        for state, action in resulting_plan:
            print('\t',state)
            print(action)
