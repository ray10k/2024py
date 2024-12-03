import re

def parse_input(input_content:str) -> str:
    #Just going to use the string-data as, data.
    return input_content

def star_one(data:str) -> str:
    retval = 0
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    for mul in pattern.finditer(data):
        a,b = mul.groups()
        retval += int(a) * int(b)
    return retval

def star_two(data:str) -> str:
    pass

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_03.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_03.txt"
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
