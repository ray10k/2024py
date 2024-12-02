from dataclasses import dataclass;

@dataclass
class ReactorReport:
    """One full reactor-report."""
    levels:list[int]

IType = ReactorReport

def parse_input(input_content:str) -> list[IType]:
    retval = list()
    for line in input_content.splitlines():
        levels = [int(x) for x in line.split(' ')]
        retval.append(ReactorReport(levels))
    return retval

def check_falling(l,r) -> bool:
    return l > r and (l - r) in range(1,4)

def check_rising(l,r) -> bool:
    return r > l and (r - l) in range(1,4)


def skip_it(skip:int,to_iterate:list,start:int = 0):
    for index, item in enumerate(to_iterate,start=start):
        if index != skip:
            yield item

def star_one(data:list[IType]) -> str:
    safe_count = 0
    
    for report in data:
        lvl = report.levels
        check = check_rising if lvl[0] < lvl[-1] else check_falling
        if all(check(l,r) for l,r in zip(lvl,lvl[1:])):
            safe_count += 1
    
    return f"{safe_count}"

def star_two(data:list[IType]) -> str:
    safe_count = 0
    
    for report in data:
        lvl = report.levels
        if all(check_rising(l,r) for l,r in zip(lvl,lvl[1:])) or all(check_falling(l,r) for l,r in zip(lvl,lvl[1:])):
            safe_count += 1
            continue
        for skip in range(len(lvl)):
            skip_list = list(skip_it(skip,lvl))
            if all(check_rising(l,r) for l,r in zip(skip_list,skip_list[1:])):
                safe_count += 1
                break
            if all(check_falling(l,r) for l,r in zip(skip_list,skip_list[1:])):
                safe_count += 1
                break
            
    return f"{safe_count}"

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_02.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_02.txt"
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
