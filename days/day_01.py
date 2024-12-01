from dataclasses import dataclass;

@dataclass
class ListEntry:
    """Representation of one 'unit' of input-data. May represent as little
    as a single character from input, as much as the entire file, or anywhere
    inbetween."""
    left:int
    right:int

IType = ListEntry

def parse_input(input_content:str) -> list[IType]:
    retval = list()
    for line in input_content.strip().splitlines():
        left,right = line.split("   ")
        retval.append(ListEntry(int(left),int(right)))
    return retval

def star_one(data:list[IType]) -> str:
    left_list = list()
    right_list = list()
    for item in data:
        left_list.append(item.left)
        right_list.append(item.right)
    left_list.sort()
    right_list.sort()
    retval = 0
    for left,right in zip(left_list,right_list):
        retval += abs(left - right)
    return f"{retval}"

def star_two(data:list[IType]) -> str:
    from collections import Counter
    left = list()
    right = Counter()
    for item in data:
        left.append(item.left)
        right.update((item.right,))
    retval = 0
    for item in left:
        retval += (item * right.get(item,0))
    return f"{retval}"

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_01.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_01.txt"
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
