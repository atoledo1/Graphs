from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# dictionary for backtrack
reversed_directions = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

#reverse path for backtracking
reversal_path = []



#set for roooms that we've visited
visited = set()

# While the amount of room we've visited is less than the total 
while len(visited) < 500:

    # variable to dictate where we want to go next
    next_move = None

    # go through exits in the current room
    for exit in player.current_room.get_exits():
        # If we haven't visited one of the rooms connected yet
        if player.current_room.get_room_in_direction(exit) not in visited:
            # Set that as the destination 
            next_move = exit
            break

    # If we have a direction that we can go to (not dead end)
    if next_move is not None:
        # Add move to path
        traversal_path.append(next_move)
        # add opposite direction of where we're going for backtracking later
        reversal_path.append(reversed_directions[next_move])
        # move player to room
        player.travel(next_move)
        # Add new room to visited
        visited.add(player.current_room)

    # If there's no more exits that we have not visited (dead end)
    else:
        #set the destination for the next move to be the previous path 
        next_move = reversal_path.pop()
        # Add backtracking step to traversal path
        traversal_path.append(next_move)
        # move player to previous room
        player.travel(next_move)




# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
