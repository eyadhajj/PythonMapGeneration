import random as rd
import colorama 

wall = (2, colorama.Fore.BLUE) 
ground = (1, colorama.Fore.YELLOW, colorama.Back.LIGHTGREEN_EX)
void = (0, colorama.Fore.LIGHTMAGENTA_EX, colorama.Back.RED)

colorama.init()

def create_empty_map(width, height):
    return [[void] * width for _ in range(height)]

def add_ground_tiles(map, num_tiles):
    width = len(map[0])
    height = len(map)
    
    for y in range(height):
        for x in range(width):
            map[y][x] = void
    
    chosen_tiles = set()
    while len(chosen_tiles) < num_tiles:
        x = rd.randint(0, width - 1)
        y = rd.randint(0, height - 1)
        if (x, y) not in chosen_tiles:
            chosen_tiles.add((x, y))
            map[y][x] = ground  
    
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

maps = create_empty_map(10, 10)
add_ground_tiles(maps, 40)
add_wall_tiles(maps)

# print the map and add colors
for row in maps:
    for tile in row:
        print(tile[1] + str(tile[0]), end=' ')
    print()
