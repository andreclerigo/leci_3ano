# Authors:
# André Clérigo, 98485
# Pedro Rocha, 98256

import asyncio
import getpass
import json
import os
import websockets
import copy
import pprint

# dictionary with pieces information for each rotation state
# structure: {'piece_type': {rot_state: [piece coordinates, base_min, base_width, width, overflow_left]}}

piece_coords = {'o': {1: [ [[3, 3], [4, 3], [3, 4], [4, 4]], 3, 2, 2, 0 ]},
                'i': {1: [ [[2, 2], [3, 2], [4, 2], [5, 2]], 2, 4, 4, 0 ], 2: [ [[4, 2], [4, 3], [4, 4], [4, 5]], 4, 1, 1, 0 ]},
                's': {1: [ [[4, 2], [4, 3], [5, 3], [5, 4]], 5, 1, 2, 1 ], 2: [ [[4, 4], [5, 4], [3, 5], [4, 5]], 3, 2, 3, 0 ]},
                'z': {1: [ [[4, 2], [3, 3], [4, 3], [3, 4]], 3, 1, 2, 0 ], 2: [ [[3, 4], [4, 4], [4, 5], [5, 5]], 4, 2, 3, 1 ]},
                'l': {1: [ [[4, 2], [4, 3], [4, 4], [5, 4]], 4, 2, 2, 0 ],
                      2: [ [[3, 3], [4, 3], [5, 3], [3, 4]], 3, 1, 3, 0 ],
                      3: [ [[3, 3], [4, 3], [4, 4], [4, 5]], 4, 1, 2, 1 ],
                      4: [ [[5, 5], [3, 6], [4, 6], [5, 6]], 3, 3, 3, 0 ]},
                't': {1: [ [[4, 2], [4, 3], [5, 3], [4, 4]], 4, 1, 2, 0 ],
                      2: [ [[3, 4], [4, 4], [5, 4], [4, 5]], 4, 1, 3, 1 ],
                      3: [ [[4, 2], [3, 3], [4, 3], [4, 4]], 4, 1, 2, 1 ],
                      4: [ [[4, 3], [3, 4], [4, 4], [5, 4]], 3, 3, 3, 0 ]},
                'j': {1: [ [[4, 2], [5, 2], [4, 3], [4, 4]], 4, 1, 2, 0 ],
                      2: [ [[3, 4], [4, 4], [5, 4], [5, 5]], 5, 1, 3, 2 ], 
                      3: [ [[4, 4], [4, 5], [3, 6], [4, 6]], 3, 2, 2, 0 ],
                      4: [ [[3, 5], [3, 6], [4, 6], [5, 6]], 3, 3, 3, 0 ]},
                }


# returns the piece type (o, j, l , s, z, t, i)
def recon_piece(piece):
    piece_type = None
    
    if piece[0][0] == piece[1][0]-1 == piece[2][0] == piece[3][0]-1 and piece[0][1] == piece[1][1] == piece[2][1]-1 == piece[3][1]-1:
        piece_type = 'o'
    else:
        if piece[0][0] == piece[1][0] == piece[2][0]-1 == piece[3][0]-1 and piece[0][1]+1 == piece[1][1] == piece[2][1] == piece[3][1]-1 \
            or piece[0][0] == piece[1][0]-1 == piece[2][0]+1 == piece[3][0] and piece[0][1] == piece[1][1] == piece[2][1]-1 == piece[3][1]-1:
            piece_type = 's' 
        else:
            if piece[0][0]-1 == piece[1][0] == piece[2][0]-1 == piece[3][0] and piece[0][1] == piece[1][1]-1 == piece[2][1]-1 == piece[3][1]-2 \
                or piece[0][0] == piece[1][0]-1 == piece[2][0]-1 == piece[3][0]-2 and piece[0][1] == piece[1][1] == piece[2][1]-1 == piece[3][1]-1:
                piece_type = 'z'
            else:
                if piece[0][1] == piece[1][1] == piece[2][1] == piece[3][1] \
                    or piece[0][0] == piece[1][0] == piece[2][0] == piece[3][0]:
                    piece_type = 'i'
                else:
                    if piece[0][0] == piece[1][0] == piece[2][0] and piece[0][1] == piece[1][1]-1 == piece[2][1]-2 == piece[3][1]-2 \
                        or piece[0][0] == piece[1][0]-1 == piece[2][0]-2 == piece[3][0] and piece[0][1] == piece[1][1] == piece[2][1] == piece[3][1]-1 \
                        or piece[0][0] == piece[1][0]-1 == piece[2][0]-1 == piece[3][0]-1 and piece[0][1] == piece[1][1] == piece[2][1]-1 == piece[3][1]-2 \
                        or piece[0][0] == piece[1][0]+2 == piece[2][0]+1 == piece[3][0] and piece[0][1] == piece[1][1]-1 == piece[2][1]-1 == piece[3][1]-1:
                        piece_type = 'l'
                    else:
                        if piece[0][0] == piece[1][0] == piece[2][0]-1 == piece[3][0] and piece[0][1]+1 == piece[1][1] == piece[2][1] == piece[3][1]-1 \
                            or piece[0][0] == piece[1][0]-1 == piece[2][0]-2 == piece[3][0]-1 and piece[0][1] == piece[1][1] == piece[2][1] == piece[3][1]-1 \
                            or piece[0][0] == piece[1][0]+1 == piece[2][0] == piece[3][0] and piece[0][1] == piece[1][1]-1 == piece[2][1]-1 == piece[3][1]-2 \
                            or piece[0][0] == piece[1][0]+1 == piece[2][0] == piece[3][0]-1 and piece[0][1] == piece[1][1]-1 == piece[2][1]-1 == piece[3][1]-1:
                            piece_type = 't'
                        else:
                            if piece[0][0] == piece[1][0]-1 == piece[2][0] == piece[3][0] and piece[0][1] == piece[1][1] == piece[2][1]-1 == piece[3][1]-2 \
                                or piece[0][0] == piece[1][0]-1 == piece[2][0]-2 == piece[3][0]-2 and piece[0][1] == piece[1][1] == piece[2][1] == piece[3][1]-1 \
                                or piece[0][0] == piece[1][0] == piece[2][0]+1 == piece[3][0] and piece[0][1] == piece[1][1]-1 == piece[2][1]-2 == piece[3][1]-2 \
                                or piece[0][0] == piece[1][0] == piece[2][0]-1 == piece[3][0]-2 and piece[0][1] == piece[1][1]-1 == piece[2][1]-1 == piece[3][1]-1:
                                piece_type = 'j'
    
    return piece_type

# returns lowest Y value of piece
def get_height(piece):
    return max(row[1] for row in piece)

# check if the column above the free_spot is empty
def col_is_empty(target, free_grid, piece):
    piece_height = get_height(piece)

    # Iterate from bottom to top of piece
    for y in range(target[1], piece_height, -1):
        if [target[0], y] not in free_grid[y]:
            return False
    return True

# returns a list of all neighbors of a given piece
def get_neighbors(free_grid, target, piece):
    row = free_grid[target[1]]
    free_row = copy.deepcopy(row)
    
    # remove all rejected neighbors to the left and the target
    for n in row:
        if n[0] <= target[0]:
            free_row.remove(n)
        else:
            if not col_is_empty(n, free_grid, piece):
                free_row.remove(n)
    
    # check if neighbors are contiguous
    if len(free_row) >= 3 and free_row[0][0] == target[0] + 1 and free_row[1][0] == target[0] + 2 and free_row[2][0] == target[0] + 3:
        return free_row[:3]
    if len(free_row) >= 2 and free_row[0][0] == target[0] + 1 and free_row[1][0] == target[0] + 2:
        return free_row[:2]
    if len(free_row) >= 1 and free_row[0][0] == target[0] + 1:
        return free_row[:1]
        
    return []

# returns true if the piece intersects with the game
def intersects(piece, game):
    for row in piece:
        if row in game:
            return True
    return False

# returns false if any coordinate in the piece hasn't a collumn empty
def piece_col_is_empty(targets, free_grid, piece):
    # iterate from bottom to top of piece
    for target in targets:
        if not col_is_empty(target, free_grid, piece):
            return False
    return True

# returns a dictionary of the free spaces
def get_free_grid(game):
    free_grid = {y: [[x, y] for x in range(1, 9)] for y in range(30)}
    if game != []:
        for lst in game:
            if lst in free_grid[lst[1]]:
                free_grid[lst[1]].remove(lst)
        return free_grid
    return free_grid

# returns a list of tuples of all possible moves for a given piece with cost associated
def generate_maps(sgame, piece, piece_type, rot_state):
    game = sgame
    free_grid = get_free_grid(game)
    height = get_height(piece)
    min_x = piece_coords[piece_type][rot_state][1]
    base_width = piece_coords[piece_type][rot_state][2]
    width = piece_coords[piece_type][rot_state][3]
    ovfl = piece_coords[piece_type][rot_state][4]
    max_targets = 8 - width + ovfl + 1
    maps = []

    cols_free_grid = {x: [[x, y] for y in range(30)] for x in range(1, 9)}
    if game != []:
        for lst in game:
            if lst in cols_free_grid[lst[0]]:
                cols_free_grid[lst[0]].remove(lst)
            break

    x_list = [x for x in range(1 + ovfl, max_targets + 1)] 

    # generate all possible targets
    for x in x_list:
        while True:
            new_piece = copy.deepcopy(piece)
            y = cols_free_grid[x].pop()[1]
            neighbors = get_neighbors(free_grid, [x,y], piece)

            # check if the target has the correct number of neighbors, if not try the next Y
            if (len(neighbors) + 1 < base_width):
                continue

            vector_x = min_x - x
            vector_y = y - height
            # put the piece at the right coordinates
            for row in new_piece:
                row[1] += vector_y
                row[0] -= vector_x
            
            # check if virtual piece location intersets with current map
            if intersects(new_piece, game):
                continue
            
            # check if all piece's coordinates have a column empty, if not try the next Y
            if not piece_col_is_empty(new_piece, free_grid, piece):
                continue
            
            map = copy.deepcopy(game)
            # add the piece to the map
            for row in new_piece:
                map.append(row)

            cost = calculate_cost(map)
            
            # associate a move to the map
            key = ['']
            if min_x > x:
                key = ['a' for _ in range(min_x - x)]
            if min_x < x:
                key = ['d' for _ in range(x - min_x)]
            
            maps.append((key, cost, [x,y], new_piece))
            break
   
    return maps

# calculate the cost of a given map
def calculate_cost(map):
    # create clean free_grid for the played map
    free_grid = get_free_grid(map)

    # populate sorted map
    sorted_map = {}
    # calculate completed lines (more is better)
    completed_lines = 0
    # calculate holes generated (less is better)
    holes = 0

    for y in range(29, 4, -1):
        sorted_map[y] = sorted(row for row in map if row[1] == y)
        if len(sorted_map[y]) == 8:
            completed_lines += 1
        for row in free_grid[y]:
            if not col_is_empty(row, free_grid, [[1, 4]]):            # Virtual piece fixed to the top
                holes += 1

    # calcute the irregularity of the map (less is better)
    irregularity = 0
    sorted_cols = {}
    cols_heights = []
    
    # get the columns max heights and calculate the irregularity level
    for x in range(1, 9):
        sorted_cols[x] = sorted(column for column in map if column[0] == x)
        if sorted_cols[x] != []:
            cols_heights.append(29 - min(column[1] for column in sorted_cols[x]))
        else:
            cols_heights.append(0)

    irregularity = abs(cols_heights[0] - cols_heights[1]) + abs(cols_heights[1] - cols_heights[2]) + abs(cols_heights[2] - cols_heights[3]) + abs(cols_heights[3] - cols_heights[4]) + abs(cols_heights[4] - cols_heights[5]) + abs(cols_heights[5] - cols_heights[6]) + abs(cols_heights[6] - cols_heights[7])

    # calculate max height of the grid achieved (less is better)
    agg_height = 0
    sum(cols_heights)

    # empty pillars (less is better)
    empty_pillars = 0
    for i in range(0,8):
        if i == 0:
            if cols_heights[i+1] - cols_heights[i] >= 3:
                empty_pillars += abs(cols_heights[i+1] - cols_heights[i])
        elif i == 7:
            if cols_heights[i-1] - cols_heights[i] >= 3:
                empty_pillars += abs(cols_heights[i-1] - cols_heights[i])
        elif cols_heights[i+1] - cols_heights[i] >= 3 and cols_heights[i-1] - cols_heights[i] >= 3:
            empty_pillars += min(abs(cols_heights[i+1] - cols_heights[i]), abs(cols_heights[i-1] - cols_heights[i]))
        else:
            continue

    total_cost = -76*completed_lines + 61*holes + 35*agg_height + 18*irregularity + 12*empty_pillars

    return total_cost

def rotate_decision(piece_type, state):
    maps_for_first = []

    # iterate through all possible rotations
    for i in range(len(piece_coords[piece_type])):
        maps = generate_maps(state['game'], piece_coords[piece_type][i + 1][0], piece_type, i+1)
        maps.sort(key=lambda x: x[1])
        best_for_rotation = maps[0]
        maps_for_first.append([best_for_rotation, i+1])
        
    maps_for_first.sort(key=lambda x: x[0][1])
 
    best_map = maps_for_first.pop(0)
   
    list_keys = ['w' for _ in range(best_map[1] - 1)] + best_map[0][0] + ['s', '', '']
    
    return list_keys

def agent(state):
    
    if state['piece'] == None:
        print("No piece")
        return ['']

    piece_type  = recon_piece(state['piece'])
    
    return rotate_decision(piece_type, state)
    
async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        list_of_keys = []
        while True:
            try:
                key = ''
                
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server

                if 'piece' in state and 'game' in state:
                    if len(list_of_keys) != 0:
                        key = list_of_keys.pop(0)
                    else:
                        list_of_keys = agent(state)    
                        
                await websocket.send(
                    json.dumps({"cmd": "key", "key": key})
                )  # send key command to server - you must implement this send in the AI agent
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                # saving scores in a local file
                with open('score.txt', 'a') as f:
                    f.write(str(state['score']) + '\n')
                return


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))