from dataclasses import dataclass;
from itertools import product

@dataclass(frozen=True)
class Calibration:
    result: int
    values: list[int]
    
    def calculate(self, bitfield:int) -> bool:
        retval = self.values[0]
        for i,value in enumerate(self.values[1:]):
            if (bitfield & (1<<i)):
                retval += value
            else:
                retval *= value
            if retval > self.result:
                return False
        return retval == self.result
    
    def tri_calculate(self, tritfield:list[int]) -> bool:
        retval = self.values[0]
        for mask,value in zip(tritfield,self.values[1:]):
            if mask == 0:
                retval *= 10 ** len(str(value))
                retval += value
            elif mask == 1:
                retval *= value
            else:
                retval += value
            if retval > self.result:
                return False
        return retval == self.result
    
IType = Calibration

def parse_input(input_content:str) -> list[IType]:
    retval:list[Calibration] = list()
    for line in input_content.splitlines():
        result,rest = line.split(':')
        rest = rest.strip()
        retval.append(Calibration(int(result),[int(x) for x in rest.split(' ')]))
    return retval

def star_one(data:list[IType]) -> str:
    retval = 0
    
    for datum in data:
        bitcount = len(datum.values)
        maximum = 2 ** (bitcount-1)
        for bitfield in range(maximum+1):
            if datum.calculate(bitfield):
                retval += datum.result
                break
    
    return f"{retval}"

def star_two(data:list[IType]) -> str:
    retval = 0
    
    for datum in data:
        bitcount = len(datum.values)
        for tritfield in product(range(3),repeat=bitcount-1):
            if datum.tri_calculate(tritfield):
                retval += datum.result
                break
    return f"{retval}"

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_07.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_07.txt"
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
