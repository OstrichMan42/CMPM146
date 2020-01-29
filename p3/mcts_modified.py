"""
Structure from
https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
"""
import random
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

ROLLOUTS = 10
MAX_DEPTH = 5


# Define a helper function to calculate the difference between the bot's score and the opponent's.
def outcome(owned_boxes, game_points, me):
    if game_points is not None:
        # Try to normalize it up?  Not so sure about this code anyhow.
        red_score = game_points[1]*9
        blue_score = game_points[2]*9
    else:
        red_score = len([v for v in owned_boxes.values() if v == 1])
        blue_score = len([v for v in owned_boxes.values() if v == 2])
    return red_score - blue_score if me == 1 else blue_score - red_score



def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.
    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.
    Returns:        A node from which the next stage of the search can proceed.
    """
    if node.untried_actions:
        return node
    bestChild = node
    bestValue = 0

    while not bestChild.untried_actions:  # while the current node has tried all of its actions
        for n in node.child_nodes:  # pick the best one
            value = n.wins + explore_faction * sqrt(log(node.visits) / n.visits)
            if identity is "red" and bestValue <= value:
                bestChild = n
                bestValue = value
            if identity is "blue" and bestValue >= value:
                bestChild = n
                bestValue = value

    bestChild.visits += 1
    return bestChild


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.
    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.
    Returns:    The added child node.
    """
    #print("untried actions: ", node.untried_actions)
    action = choice(node.untried_actions)
    #print("new node from action: ", action, type(action))
    newChild = MCTSNode(node, action, board.next_state(state, action))
    node.child_nodes[action] = newChild
    return newChild
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.
    Args:
        board:  The game setup.
        state:  The state of the game.
    """

    
    simState = state

    moves = board.legal_actions(simState)

    best_move = moves[0]
    best_expectation = float('-inf')

    me = board.current_player(simState)


    for move in moves:
        total_score = 0.0

        # Sample a set number of games where the target move is immediately applied.
        for r in range(ROLLOUTS):
            rollout_state = board.next_state(simState, move)

            # Only play to the specified depth.
            for i in range(MAX_DEPTH):
                if board.is_ended(rollout_state):
                    break
                rollout_move = random.choice(board.legal_actions(rollout_state))
                rollout_state = board.next_state(rollout_state, rollout_move)

            total_score += outcome(board.owned_boxes(rollout_state),
                                    board.points_values(rollout_state), me)

        expectation = float(total_score) / ROLLOUTS

        # If the current move has a better average score, replace best_move and best_expectation
        if expectation > best_expectation:
            best_expectation = expectation
            best_move = move
            
        #move = choice(board.legal_actions(simState))  # random choice
        simState = board.next_state(simState, best_move)

    return board.points_values(simState)


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.
    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.
    """
    if node.parent is None:
        return
    node.wins += won
    backpropagate(node.parent, won)


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.
    Args:
        board:  The game setup.
        state:  The state of the game.
    Returns:    The action to be taken.
    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        leaf = traverse_nodes(node, board, sampled_game, identity_of_bot)
        expand_leaf(leaf, board, sampled_game)
        won = rollout(board, state)
        if won:
            backpropagate(leaf, won[identity_of_bot])

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    action = None
    bestChance = -1
    for move in root_node.child_nodes.keys():
        child = root_node.child_nodes[move]
        if child.wins > bestChance:
            action = child.parent_action
            bestChance = child.wins
    return action
