from dataclasses import dataclass;

@dataclass
class OrderRule:
    """One pair of page-numbers that need to be in first-last order for the
    entire sequence to be valid."""
    left:int
    right:int
    
    def rule_applies(self,values:list[int]) -> bool:
        return self.left in values and self.right in values
    
    def check_rule(self,values:list[int]) -> bool:
        if self.left not in values or self.right not in values:
            return True
        return values.index(self.left) < values.index(self.right)

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
            if not rule.check_rule(seq):
                break
        else:
            midpoint = int((len(seq) - 1) / 2)
            retval += seq[midpoint]
    return f"{retval}"

def star_two(data:IType) -> str:
    rules, sequences = data
    retval = 0
    unsorted = list()
    for seq in sequences:
        for rule in rules:
            if not rule.check_rule(seq):
                unsorted.append(seq)
                break
    
    for to_sort in unsorted:
        sort_rules = [rule for rule in filter(lambda x: x.rule_applies(to_sort),rules)]
        reorder = [x for x in to_sort]
        while not all(r.check_rule(reorder) for r in sort_rules):
            for r in sort_rules:
                if not r.check_rule(reorder):
                    l_index = reorder.index(r.left)
                    r_index = reorder.index(r.right)
                    temp = reorder[l_index]
                    reorder[l_index] = reorder[r_index]
                    reorder[r_index] = temp
        midpoint = int((len(reorder) - 1) / 2)
        retval += reorder[midpoint]
    return f"{retval}"

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
