from dataclasses import dataclass
from collections import namedtuple, deque

class GardenMap:
    def __init__(self,plots:str,height:int,width:int):
        self.plots = "".join(plots.split())
        self.height = height
        self.width = width
        
    def __getitem__(self,key) -> str:
        x,y = key
        if x < 0 or x >= self.width:
            return ' '
        if y < 0 or y >= self.height:
            return ' '
        offset = x + (y * self.width)
        return self.plots[offset]

Point = namedtuple("Point","x y")

@dataclass(init=False)
class GardenPlot:
    locations:frozenset[Point]
    symbol:str
    surface:int
    circumference:int
    
    def __init__(self,symbol:str,locations:set[Point],circumference:int):
        self.locations = frozenset(locations)
        self.symbol = symbol[0]
        self.surface = len(locations)
        self.circumference = circumference

IType = GardenMap

def parse_input(input_content:str) -> IType:
    lines = input_content.splitlines()
    w,h = len(lines[0]),len(lines)
    return GardenMap(input_content,h,w)

def parse_plots(data:IType) -> list[GardenPlot]:
    visited:set[Point] = set()
    plots:list[GardenPlot] = list()
        
    for y in range(data.height):
        for x in range(data.width):
            if Point(x,y) in visited:
                continue
            cur_sym:str = data[x,y]
            fields:set[Point] = set()
            circumference:int = 0
            to_check:deque[Point] = deque()
            to_check.append(Point(x,y))
            while to_check:
                here = to_check.popleft()
                
                if here in fields:
                    continue
                if data[here] != cur_sym:
                    circumference += 1
                    continue
                
                to_check.append(Point(here.x-1,here.y))
                to_check.append(Point(here.x+1,here.y))
                to_check.append(Point(here.x,here.y-1))
                to_check.append(Point(here.x,here.y+1))
                
                visited.add(here)
                fields.add(here)
            plots.append(GardenPlot(cur_sym,fields,circumference))
    return plots


def star_one(data:IType) -> str:
    plots = parse_plots(data)
    retval = sum(p.circumference * p.surface for p in plots)
    return f"{retval}"

def star_two(data:IType) -> str:
    plots = parse_plots(data)
    pass

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_12.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_12.txt"
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
