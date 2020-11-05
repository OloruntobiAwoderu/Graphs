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
roomGraph=literal_eval(open(map_file, "r").read())
world.load_graph(roomGraph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

def roomsSeen(roomID):
    for room in roomGraph[roomID][1].values():
        if room not in seenRooms:
            return False
    return True

def unseenRoom(roomID):
    for direction, room in roomGraph[roomID][1].items():
        if room not in seenRooms:
            traversal_Path.append(direction)
            seenRooms.add(room)
            return room

def backTrackSteps():
    visited = []
    paths = {}
    s = Stack()
    s.push(currentRoom)
    paths[currentRoom] = [currentRoom]
    while s.size() > 0:
        room = s.pop()
        visited.append(room)
        for searchedRoom in roomGraph[room][1].values():
            if searchedRoom in visited:
                continue

            newPath = paths[room][:]

            newPath.append(searchedRoom)
            paths[searchedRoom] = newPath
            if not roomsSeen(searchedRoom):
                correctPath = paths[searchedRoom]
                directions = []
                for i in range(len(correctPath) - 1):
                    for direction, value in roomGraph[correctPath[i]][1].items():
                        if value == correctPath[i + 1]:
                            directions.append(direction)
                    seenRooms.add(correctPath[i + 1])
                return (directions, correctPath[len(correctPath) - 1])
            s.push(searchedRoom)
    return None

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_Path = ['n', 's', 'e', 'w']

seenRooms = set()

currentRoom = 0
while True:
    while not roomsSeen(currentRoom): 
        
        currentRoom = unseenRoom(currentRoom) 

    tracedValues = backTrackSteps() 
    if tracedValues:
        newPath = tracedValues[0]
        traversal_Path.extend(newPath)
        currentRoom = tracedValues[1]
    else:
        break



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_Path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(roomGraph):
    print(f"TESTS PASSED: {len(traversal_Path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(roomGraph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
