import random as rd
import colorama 

wall = (2, colorama.Fore.BLUE) 
ground = (1, colorama.Fore.YELLOW, colorama.Back.LIGHTGREEN_EX)
void = (0, colorama.Fore.LIGHTMAGENTA_EX, colorama.Back.RED)
start = ("S", colorama.Fore.GREEN, colorama.Back.BLACK)
end = ("E", colorama.Fore.GREEN, colorama.Back.BLACK)

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

    return map

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

    walkable = {ground, start, end}

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
maps = create_empty_map(15, 15)
add_ground_tiles(maps, 40)
add_wall_tiles(maps)
add_start_and_end(maps)

# print the map and add colors
for row in maps:
    for tile in row:
        print(tile[1] + str(tile[0]), end=' ')
    print()


