from dataclasses import dataclass;

@dataclass
class OrderRule:
    """One pair of page-numbers that need to be in first-last order for the
    entire sequence to be valid."""
    left:int
    right:int

IType = tuple[list[OrderRule],list[list[int]]]

def parse_input(input_content:str) -> IType:
    rules:list[OrderRule] = list()
    sequences:list[list[int]] = list()
    line_iter = iter(input_content.splitlines())
    for order_line in line_iter:
        if order_line == "":
            break
        left,right = order_line.split('|')
        rules.append(OrderRule(int(left),int(right)))
    
    for sequence_line in line_iter:
        line_values = [int(x) for x in sequence_line.split(',')]   
        sequences.append(line_values)
    
    return (rules,sequences)

def star_one(data:IType) -> str:
    rules,sequences = data
    retval = 0
    for seq in sequences:
        for rule in rules:
            try:
                l_index, r_index = seq.index(rule.left),seq.index(rule.right)
                if l_index > r_index:
                    break
            except:
                continue
        else:
            midpoint = int((len(seq) - 1) / 2)
            retval += seq[midpoint]
    return f"{retval}"

def star_two(data:IType) -> str:
    pass

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_05.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_05.txt"
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
