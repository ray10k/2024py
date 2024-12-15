from collections import deque

Coord = tuple[int,int]
IType = tuple[dict[Coord,int],int,int]

def parse_input(input_content:str) -> IType:
    retval = dict()
    h,w = 0,0
    for y,line in enumerate(input_content.splitlines()):
        h = max(h,y)
        for x,char in enumerate(line):
            w = max(w,x)
            height = int(char)
            retval[(x,y)] = height
    return retval, h, w

def star_one(data:IType) -> str:
    path_map, h, w = data
    starting_points:list[Coord] = list()
    for position,height in path_map.items():
        if height == 0:
            starting_points.append(position)
    hr = range(h+1)
    wr = range(w+1)
    
    def r_check(x,y):
        return x in wr and y in hr
    
    retval = 0
    
    for trialhead in starting_points:
        ends:set[Coord] = set()
        to_check:deque[Coord] = deque()
        to_check.append(trialhead)
        while to_check:
            x,y = to_check.popleft()
            z = path_map[(x,y)]
            if z == 9:
                ends.add((x,y))
                continue
            if r_check(x-1,y) and path_map[(x-1,y)] == z + 1:
                to_check.append((x-1,y))
            if r_check(x+1,y) and path_map[(x+1,y)] == z + 1:
                to_check.append((x+1,y))
            if r_check(x,y-1) and path_map[(x,y-1)] == z + 1:
                to_check.append((x,y-1))
            if r_check(x,y+1) and path_map[(x,y+1)] == z + 1:
                to_check.append((x,y+1))
        retval += len(ends)
    return f"{retval}"

def star_two(data:IType) -> str:
    pass

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_10.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_10.txt"
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
