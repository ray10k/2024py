from dataclasses import dataclass;
from typing import Literal;

@dataclass
class Block:
    """Representation of one 'unit' of input-data. May represent as little
    as a single character from input, as much as the entire file, or anywhere
    inbetween."""
    length:int
    id:int|None = None

IType = Block

def parse_input(input_content:str) -> list[IType]:
    retval = list()
    current_id = 0
    is_file = True
    for char in input_content.strip():
        length = int(char)
        if is_file:
            retval.append(Block(length,current_id))
            current_id += 1
        else:
            retval.append(Block(length))
        is_file = not is_file
    return retval

def star_one(data:list[IType]) -> str:
    total_length:int = sum(block.length for block in data)
    print(f"Total length: {total_length}")
    memory:list[int] = [-1] * total_length
    write_pointer:int = 0
    
    #Expand blocks
    for block in data:
        if block.id is not None:
            for i in range(block.length):
                memory[i+write_pointer] = block.id
        write_pointer += block.length
    print("blocks expanded.")
    print(memory[0:100])
    
    #defragment
    write_pointer = 0
    read_pointer:int = total_length - 1
    def swap(left:int,right:int):
        temp = memory[left]
        memory[left] = memory[right]
        memory[right] = temp

    while write_pointer < read_pointer:
        while memory[read_pointer] == -1:
            read_pointer -= 1
        if memory[write_pointer] != -1:
            write_pointer += 1
            continue
        swap(write_pointer,read_pointer)
    print("memory defragmented.")
    print(memory[0:100])

    #Calculate checksum
    retval = 0
    for position,value in enumerate(memory):
        if value == -1:
            break
        retval += position * value
    return f"{retval}"

def star_two(data:list[IType]) -> str:
    pass

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_09.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_09.txt"
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
