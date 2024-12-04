from dataclasses import dataclass;

@dataclass
class WordSearch:
    """A whole bunch of XMAS."""
    search: str
    """The lines of the word-field, as a single string."""
    width: int
    """The number of characters per line."""
    height: int
    """The number of lines."""
    
    def coordinate(self,x:int, y:int) -> str|None:
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return self.search[(y * (self.width+1)) + x]
        return None
    
    def diagonals(self,x:int, y:int) -> tuple[str,str,str,str]|None:
        if x >= 1 and x < (self.width-1) and y >= 1 and y < (self.height-1):
            return (self.coordinate(x-1,y-1),self.coordinate(x+1,y-1),self.coordinate(x+1,y+1),self.coordinate(x-1,y+1))
        return None

IType = WordSearch

DIRECTIONS = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]

def parse_input(input_content:str) -> IType:
    lines = input_content.splitlines()
    return WordSearch(input_content,len(lines[0]),len(lines))

def xmas_coords(start_coord:tuple[int,int],d_offset:tuple[int,int],search:WordSearch) -> None|list[tuple[int,int]]:
    retval = list()
    for step, letter in enumerate("XMAS"):
        x = start_coord[0] + (step * d_offset[0])
        y = start_coord[1] + (step * d_offset[1])
        if search.coordinate(x,y) != letter:
            return None
        retval.append((x,y))
    return retval

def find_xmas(start_coord:tuple[int,int],d_offset:tuple[int,int],search:WordSearch) -> bool:
    return xmas_coords(start_coord,d_offset,search) is not None

def star_one(data:IType) -> str:
    retval = 0
    valids = set()
    for y in range(data.height):
        for x in range(data.width):
            index = data.coordinate(x,y)
            if index == 'X':
                for d in DIRECTIONS:
                    found = xmas_coords((x,y),d,data)
                    if found is not None:
                        retval += 1
                        valids.update(found)
    """for y in range(data.height):
    for x in range(data.width):
        if (x,y) in valids:
            print(data.coordinate(x,y),end="")
        else:
            print(end=" ")
    print()""" #uncomment to print out the locations of the "valid" letters.
    
    return f"{retval}"

def star_two(data:IType) -> str:
    retval = 0
    for y in range(data.height):
        for x in range(data.width):
            if data.coordinate(x,y) == 'A':
                surrounding = data.diagonals(x,y)
                if surrounding is None:
                    continue
                for step in range(4):
                    if surrounding[step] == 'M':
                        string = "".join(surrounding[(step+i)%4] for i in range(4))
                        if string == "MMSS":
                            retval += 1
                            continue
    return f"{retval}"

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_04.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_04.txt"
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
