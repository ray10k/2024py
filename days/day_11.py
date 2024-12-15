
IType = int

def parse_input(input_content:str) -> list[IType]:
    return [int(x) for x in input_content.split()]

def tick_rocks(initial:dict[int,int]) -> dict[int,int]:
    retval = dict()
    
    for rock,count in initial.items():
        if rock == 0:
            ones = retval.get(1,0) + count
            retval[1] = ones
            continue
        strnum = str(rock)
        if len(strnum) % 2 == 0:
            splitpoint = int(len(strnum)/2)
            left,right = int(strnum[:splitpoint]),int(strnum[splitpoint:])
            lcount = retval.get(left,0) + count
            retval[left] = lcount
            rcount = retval.get(right,0) + count
            retval[right] = rcount
        else:
            ncount = retval.get(2024*rock,0) + count
            retval[2024*rock] = ncount
    
    return retval

def star_one(data:list[IType]) -> str:
    stones = dict()
    for stone in data:
        count = stones.get(stone,0) + 1
        stones[stone] = count
    
    for _ in range(25):
        stones = tick_rocks(stones)
    
    return f"{sum(stones.values())}"
    
    

def star_two(data:list[IType]) -> str:
    stones = dict()
    for stone in data:
        count = stones.get(stone,0) + 1
        stones[stone] = count
    
    for _ in range(75):
        stones = tick_rocks(stones)
    
    return f"{sum(stones.values())}"

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_11.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_11.txt"
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
