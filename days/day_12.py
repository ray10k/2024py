from dataclasses import dataclass;

@dataclass
class InputItem:
    """Representation of one 'unit' of input-data. May represent as little
    as a single character from input, as much as the entire file, or anywhere
    inbetween."""
    a: str

IType = InputItem

def parse_input(input_content:str) -> list[IType]:
    return list()

def star_one(data:list[IType]) -> str:
    pass

def star_two(data:list[IType]) -> str:
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
