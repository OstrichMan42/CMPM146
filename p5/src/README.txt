I tried implementing A* for this assignment, but the heuristic is quite simple.
It first checks if the state would satisfy the goal, if so, it has a h_cost of zero.
Second it checks if the state would have more of any item than is necessary to craft anything, if so it has a h_cost of infinity.
The third case catches everything not in the first two, it has a h_cost of one.

Done by Caetano Hyams, no partner.