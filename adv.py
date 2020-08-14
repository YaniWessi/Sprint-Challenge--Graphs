from room import Room
from player import Player
from world import World
from ast import literal_eval
import sys
import queue
import random
sys.setrecursionlimit(5000)
# Load world
world = World()
# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"
# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)
# Print an ASCII map
world.print_rooms()
player = Player(world.starting_room)
# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
s = []
visited = {}
popped = []


def traverse_map(prev_room, current_room):
    # print()
    # print(f"You are here: {player.current_room.id}")
    # print(f"You think you are here: {current_room}")
    # print(f"You think you came from: {prev_room}")
    # print(f"Possible rooms are: {player.current_room.get_exits()}")
    # print(f"traversal path so far: {traversal_path}")
    if current_room not in visited:
        exits = player.current_room.get_exits()
        visited[current_room] = {}
        for direction in exits:
            visited[current_room][direction] = "?"
    if len(traversal_path) > 0:
        from_direction = traversal_path[-1]
    else:
        from_direction = None
    if from_direction == 'n':
        visited[current_room]['s'] = prev_room
        visited[prev_room]["n"] = current_room
    elif from_direction == 'e':
        visited[current_room]['w'] = prev_room
        visited[prev_room]["e"] = current_room
    elif from_direction == 'w':
        visited[current_room]['e'] = prev_room
        visited[prev_room]["w"] = current_room
    elif from_direction == 's':
        visited[current_room]['n'] = prev_room
        visited[prev_room]["s"] = current_room
    # checks what possible exits there are, add to stack if unknown room
    for direction in visited[current_room]:
        if visited[current_room][direction] == "?":
            player.travel(direction)
            next_room = player.current_room.id
            # print(f"you are adding to stack: current_room {current_room}, next_room {next_room}, direction {direction}")
            if (current_room, next_room, direction) not in s:
                s.append((current_room, next_room, direction))
            if direction == "n":
                player.travel("s")
            elif direction == "e":
                player.travel("w")
            elif direction == "s":
                player.travel("n")
            elif direction == "w":
                player.travel("e")
    # print(f"this is the stack: {s}")
    if len(s) > 0:
        info_for_next_room = s.pop()
        popped.append(info_for_next_room)
        current_room_info = info_for_next_room[0]
        next_room_info = info_for_next_room[1]
        direction_info = info_for_next_room[2]
        # print(f"popped off stack. current room: {current_room_info}, next room: {next_room_info}, direction: {direction_info}")
        if direction_info in visited[current_room] and visited[current_room][direction_info] == "?":
            traversal_path.append(direction_info)
            # print(f"You travelled {direction_info} because its available and is unknown")
            player.travel(direction_info)
            traverse_map(current_room_info, next_room_info)
        else:
            # print("unknown not available, from here do a breadth first search")
            def bfs():
                # print(f"from direction is: {from_direction}")
                if from_direction == 'n':
                    goto_direction = 's'
                elif from_direction == 'e':
                    goto_direction = 'w'
                elif from_direction == 's':
                    goto_direction = 'n'
                elif from_direction == 'w':
                    goto_direction = 'e'
                q = queue.Queue()
                # print(f"goto direction is: {goto_direction}")
                q.put([goto_direction])
                while q.qsize() > 0 and len(visited) < len(room_graph):
                    path = q.get()
                    # print(f"path is {path}")
                    current_room = player.current_room.id
                    for direction in path:
                        # print(f"currently here {player.current_room.id}")
                        # print(f"traveling this direction {direction}")
                        player.travel(direction)
                        # print(f"arrived here after moving {player.current_room.id}")
                    if path[-1] == "n":
                        player.travel('s')
                        current_room = player.current_room.id
                        player.travel('n')
                    elif path[-1] == "e":
                        player.travel('w')
                        current_room = player.current_room.id
                        player.travel('e')
                    elif path[-1] == "s":
                        player.travel('n')
                        current_room = player.current_room.id
                        player.travel('s')
                    elif path[-1] == "w":
                        player.travel('e')
                        current_room = player.current_room.id
                        player.travel('w')
                    if player.current_room.id not in visited:
                        # print(f"found unvisited room. recursion here")
                        for direction in path:
                            traversal_path.append(direction)
                        traverse_map(current_room, player.current_room.id)
                    else:
                        # print(f"this room {player.current_room.id} is in visited already")
                        for direction in visited[player.current_room.id]:
                            if direction == "?":
                                # print(f"returning the path {path}")
                                return path
                        for direction in visited[player.current_room.id]:
                            direction_from = ""
                            if path[-1] == "n":
                                direction_from = "s"
                            elif path[-1] == "e":
                                direction_from = "w"
                            elif path[-1] == "w":
                                direction_from = "e"
                            elif path[-1] == "s":
                                direction_from = "n"
                            if direction_from != direction:
                                new_path = list(path)
                                new_path.append(direction)
                                # print(f"putting this path in the queue: {new_path}")
                                q.put(new_path)
                        # print(f"backtravelling this path {path}")
                        # print(f"you are here {player.current_room.id}")
                        reverse_path = list(path)
                        reverse_path.reverse()
                        for direction in reverse_path:
                            if direction == "n":
                                # print(f"travelling s")
                                player.travel('s')
                            elif direction == "e":
                                # print(f"travelling w")
                                player.travel('w')
                            elif direction == "s":
                                # print(f"travelling n")
                                player.travel('n')
                            elif direction == "w":
                                # print(f"travelling e")
                                player.travel('e')
                        # print(f"you are now here {player.current_room.id}")
            bfs()


traverse_map(None, player.current_room.id)
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)
for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)
if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
