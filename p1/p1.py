from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    dist = {initial_position: 0}
    prev = {}
    queue = []
    heappush(queue, (0, initial_position))
    while queue:
        curr = heappop(queue) # curr = (fastestCostSoFar, (location))
        #print(curr)
        adjacent = adj(graph, curr[1])
        for neighbor in adjacent: # neighbor = ((location), cost)
            if neighbor[0] == destination:
                path = [destination]
                trail = curr[1]
                while trail in prev:
                    path.append(trail)
                    trail = prev[trail]
                path.append(initial_position)
                return reversed(path)
            altDist = dist[curr[1]] + neighbor[1]
            if neighbor[0] not in dist or altDist < dist[neighbor[0]]:
                dist[neighbor[0]] = altDist
                prev[neighbor[0]] = curr[1]
                heappush(queue, (altDist, neighbor[0]))
    #print(adjacent)
    #print(dist)
    #print(prev)
    pass


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    allCosts = {initial_position: 0}
    queue = []
    heappush(queue, (0, initial_position))
    while queue:
        curr = heappop(queue)  # curr = (fastestCostSoFar, (location))
        adjacent = adj(graph, curr[1])
        for neighbor in adjacent:  # neighbor = ((location), cost)
            altDist = allCosts[curr[1]] + neighbor[1]
            if neighbor[0] not in allCosts or altDist < allCosts[neighbor[0]]:
                allCosts[neighbor[0]] = altDist
                heappush(queue, (altDist, neighbor[0]))

    return allCosts


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    list = []
    i = -1
    while i < 2:
        j = -1
        while j < 2:
            if i == 0 and j == 0:
                j += 1
            neighbor = cell[0] + i, cell[1] + j
            #if neighbor in level["walls"]:
            #    list.append((neighbor, float("inf")))
            if neighbor in level["spaces"]:
                b = 0.5
                if i != 0 & j != 0:
                    b *= sqrt(2)
                list.append((neighbor, b * level["spaces"][cell] + b * level["spaces"][neighbor]))
            j += 1
        i += 1
    return list


def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'test_maze.txt', 'a','d'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    filename = "my_maze.txt"
    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
