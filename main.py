import random as rd
import colorama 

import time
import os

wall = (2, colorama.Fore.BLUE) 
ground = (1, colorama.Fore.YELLOW, colorama.Back.LIGHTGREEN_EX)
void = (0, colorama.Fore.LIGHTMAGENTA_EX, colorama.Back.RED)
start = ("S", colorama.Fore.GREEN, colorama.Back.BLACK)
end = ("E", colorama.Fore.GREEN, colorama.Back.BLACK)
explored = ("*", colorama.Fore.WHITE, colorama.Back.BLUE)
path  = (5, colorama.Fore.GREEN, colorama.Back.CYAN)

colorama.init()



def create_empty_map(width, height):
    return [[void] * width for _ in range(height)]

def add_ground_tiles(map, num_tiles):
    width = len(map[0])
    height = len(map)
    
    center_x = width // 2
    center_y = height // 2

    directions = [
        (0, 1), 
        (1, 0), 
        (0, -1), 
        (-1, 0)
        ]  # down, right, up, left

    chosen_tiles = set()

    while len(chosen_tiles) < num_tiles:
        
        map[center_y][center_x] = ground
        chosen_tiles.add((center_x, center_y))

        dir_x, dir_y = rd.choice(directions)
        center_x += dir_x
        center_y += dir_y
        
        center_x = max(0, min(center_x, width - 1))
        center_y = max(0, min(center_y, height - 1))
        
    
    return map

def add_start_and_end(map):
    width = len(map[0])
    height = len(map)
    
    all_ground = [(x, y) for y in range(height) for x in range(width) if map[y][x] == ground]
    start_x, start_y = rd.choice(all_ground)
    map[start_y][start_x] = start

    possible_end_positions = []
    min_distance = (width + height) // 2

    for y in range(height):
        for x in range(width):
            if map[y][x] == ground:
                distance = abs(x - start_x) + abs(y - start_y)
                if distance >= min_distance:
                    possible_end_positions.append((x, y))

    if possible_end_positions:
        end_x, end_y = rd.choice(possible_end_positions)
        map[end_y][end_x] = end
    else:
        all_ground = [(x, y) for y in range(height) for x in range(width) if map[y][x] == ground]
        end_x, end_y = max(
            all_ground, 
            key=lambda pos: abs(pos[0] - start_x) + abs(pos[1] - start_y)
        )
        map[end_y][end_x] = end

    return map, (start_x, start_y), (end_x, end_y)

def add_wall_tiles(map):
    width = len(map[0])
    height = len(map)
    
    for y in range(height):
        for x in range(width):
            if map[y][x] == ground:
                # check right
                if x + 1 < width and map[y][x + 1] == void:
                    map[y][x + 1] = wall
                # check left
                if x - 1 >= 0 and map[y][x - 1] == void:
                    map[y][x - 1] = wall
                # check down
                if y + 1 < height and map[y + 1][x] == void:
                    map[y + 1][x] = wall
                # check up
                if y - 1 >= 0 and map[y - 1][x] == void:
                    map[y - 1][x] = wall        
    
    return map

def get_neighbours(map, x, y):
    neighbours = []

    walkable = {ground, start, end, explored}

    width = len(map[0])
    height = len(map)

    directions = [
        (0, 1), 
        (1, 0), 
        (0, -1), 
        (-1, 0)
    ]  # down, right, up, left
    
    for dir_x, dir_y in directions:
        new_x = x + dir_x
        new_y = y + dir_y

        if 0 <= new_x < width and 0 <= new_y < height:
            if map[new_y][new_x] in walkable:
                neighbours.append((new_x, new_y))

    return neighbours

def breadth_first_search(map, start_pos, end_pos):
    queue = [start_pos]
    visited = {start_pos}

    while queue:
        current_pos = queue.pop(0)
        x, y = current_pos

        if map[y][x] != start and map[y][x] != end:
            map[y][x] = explored

        os.system("cls" if os.name == "nt" else "clear")
        print_map(map)
        time.sleep(0.1)

        if current_pos == end_pos:
            return True

        neighbours = get_neighbours(map, x, y)

        for neighbour in neighbours:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    return False

maps = create_empty_map(10, 10)
add_ground_tiles(maps, 40)
add_wall_tiles(maps)
maps, start_pos, end_pos = add_start_and_end(maps)

print("Start:", start_pos)
print("End:", end_pos)
print("Start neighbours:", get_neighbours(maps, start_pos[0], start_pos[1]))

# print the map and add colors
# for row in maps:
#     for tile in row:
#         print(tile[1] + str(tile[0]), end=' ')
#     print()

def print_map(map):
    for row in map:
        for tile in row:
            print(tile[1] + str(tile[0]), end=' ')
        print()

print_map(maps)

print("Start:", start_pos)
print("End:", end_pos)
print("Can reach end using BFS?: ", breadth_first_search(maps, start_pos, end_pos))
