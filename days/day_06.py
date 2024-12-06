from dataclasses import dataclass
from itertools import cycle

@dataclass(frozen=True,unsafe_hash=True)
class Coordinate:
    """A single location in the map."""
    x:int
    y:int

# Locations of obstacles, guard's initial position, map height/width
IType = tuple[set[Coordinate],Coordinate,tuple[int,int]]

def print_map(obstacles:set[Coordinate],tiles:set[Coordinate],size:tuple[int,int]):
    for y in range(size[1]):
        for x in range(size[0]):
            here = Coordinate(x,y)
            if here in obstacles and here in tiles:
                print("&",end="")
            elif here in obstacles:
                print("#",end="")
            elif here in tiles:
                print(".",end="")
            else:
                print(" ",end="")
        print()

def parse_input(input_content:str) -> IType:
    obstacles = set()
    guard = None
    lines = input_content.splitlines()
    for y,line in enumerate(lines):
        for x,char in enumerate(line):
            if char == "#":
                obstacles.add(Coordinate(x,y))
            elif char == '^':
                guard = Coordinate(x,y)
    return obstacles, guard, (len(lines[0]),len(lines))

def star_one(data:IType) -> str:
    visited:set[Coordinate] = set()
    obstacles, guard, (width,height) = data
    print(f"Field size {width} x {height}")
    def in_field(x:int,y:int) -> bool:
        return x >= 0 and x < width and y >= 0 and y < height
    direction = cycle(((0,-1),(1,0),(0,1),(-1,0)))
    
    while True:
        facing = next(direction)
        guard_n = guard
        while guard_n not in obstacles and in_field(guard_n.x,guard_n.y):
            visited.add(guard_n)
            guard = guard_n
            guard_n = Coordinate(guard_n.x + facing[0],guard_n.y + facing[1])
        if not in_field(guard_n.x,guard_n.y):
            break
    
    #print_map(obstacles,visited,(width,height))
            
    return f"{len(visited)}"

def star_two(data:IType) -> str:
    pass

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_06.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_06.txt"
    else:
        source = Path(source).absolute()
    
    raw_data:str = ""
    with open(source) as ifile:
        raw_data = ifile.read()
    
    parsed_data = parse_input(raw_data)
    result_one = star_one(parsed_data)
    
    print(f"Result 1: {result_one}")
    
    parsed_data = parse_input(raw_data)
    result_two = star_two(parsed_data)
    
    print(f"Result 2: {result_two}")
