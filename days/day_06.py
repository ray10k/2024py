from collections.abc import Callable
from dataclasses import dataclass
from itertools import cycle

@dataclass(frozen=True,unsafe_hash=True)
class Coordinate:
    """A single location in the map."""
    x:int
    y:int
    
    def step(self,direction:tuple[int,int]) -> "Coordinate":
        return Coordinate(self.x + direction[0], self.y + direction[1])

# Locations of obstacles, guard's initial position, map height/width
IType = tuple[set[Coordinate],Coordinate,tuple[int,int]]

def reach_check(height:int,width:int) -> Callable[[int,int],bool]:
    return lambda x,y: x >=0 and x < width and y >= 0 and y < height

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
    reach = reach_check(width,height)
    print(f"Field size {width} x {height}")
    direction = cycle(((0,-1),(1,0),(0,1),(-1,0)))
    
    while True:
        facing = next(direction)
        guard_n = guard
        while guard_n not in obstacles and reach(guard_n.x,guard_n.y):
            visited.add(guard_n)
            guard = guard_n
            guard_n = Coordinate(guard_n.x + facing[0],guard_n.y + facing[1])
        if not reach(guard_n.x,guard_n.y):
            break
    
    #print_map(obstacles,visited,(width,height))
            
    return f"{len(visited)}"

def star_two(data:IType) -> str:
    obstacles,guard,(width,height) = data
    
    directions = ((0,-1,0),(1,0,1),(0,1,2),(-1,0,3))
    main_direction = cycle(directions)
    heading = next(main_direction)
    
    check = reach_check(width,height)
    
    insert_positions:set[Coordinate] = set()
    
    while check(guard.x, guard.y):
        step = guard.step(heading[0:2])
        if step in obstacles:
            heading = next(main_direction)
        else:
            #Treat the step as a ghost obstacle, and see if there is a collision that happens twice.
            
            inner_direction = cycle(directions)
            inner_heading = next(inner_direction)
            inner_guard = guard
            for _ in range(heading[2]):
                inner_heading = next(inner_direction)
            
            colisions:set[tuple[int,Coordinate]] = set()
            while True:
                inner_step = inner_guard.step(inner_heading[0:2])
                if not check(inner_step.x, inner_step.y):
                    break #The guard left the area; this is definitely not an infinite loop.
                if inner_step in obstacles or inner_step == step:
                    #The guard ran into something. Check if she did so before (same position, same heading.)
                    event = (inner_heading[2],inner_guard)
                    if event in colisions:
                        insert_positions.add(step)
                        print(colisions)
                        print(event)
                        break
                    else:
                        colisions.add(event)
                        inner_heading = next(inner_direction)
                else:
                    inner_guard = inner_step
            colisions.clear()
            guard = step
    return f"{len(insert_positions)}"

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
