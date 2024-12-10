from dataclasses import dataclass;
from itertools import permutations;

@dataclass(frozen=True,slots=True)
class Coordinate:
    """Representation of one 'unit' of input-data. May represent as little
    as a single character from input, as much as the entire file, or anywhere
    inbetween."""
    x:int
    y:int
    
    def in_range(self, w:int, h:int) -> bool:
        return self.x >= 0 and self.x < w and self.y >= 0 and self.y < h

IType = list[Coordinate]

def parse_input(input_content:str) -> tuple[dict[str,IType],tuple[int,int]]:
    width, height = 0,0
    retval:dict[str,list[Coordinate]] = dict()
    for y,line in enumerate(input_content.splitlines()):
        width = len(line)
        height += 1
        for x,char in enumerate(line):
            if char != '.':
                if char not in retval:
                    retval[char] = list()
                retval[char].append(Coordinate(x,y))
    
    return retval, (width,height)

def star_one(data:tuple[dict[str,IType],tuple[int,int]]) -> str:
    antinodes:set[Coordinate] = set()
    antennas, (width,height) = data
    for value in antennas.values():
        for a,b in permutations(value,2):
            d_x = a.x - b.x
            d_y = a.y - b.y
            antinode = Coordinate(a.x+d_x,a.y+d_y)
            if antinode.in_range(width,height):
                antinodes.add(antinode)
    return f"{len(antinodes)}"

def star_two(data:tuple[dict[str,IType],tuple[int,int]]) -> str:
    antinodes:set[Coordinate] = set()
    antennas, (width,height) = data
    for group in antennas.values():
        for a,b in permutations(group,2):
            d_x = a.x - b.x
            d_y = a.y - b.y
            antinode = a
            while antinode.in_range(width,height):
                antinodes.add(antinode)
                antinode = Coordinate(antinode.x+d_x,antinode.y+d_y)
    
    return f"{len(antinodes)}"

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_08.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_08.txt"
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
