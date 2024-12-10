from dataclasses import dataclass;
from collections import deque

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
    # The logic for this defrag method is... odd. Very odd.
    ordered:list[Block] = [b for b in data] #Copy the input, will be moving this around a bunch
    max_id = max(blk.id for blk in data if blk.id is not None)

    for to_move in range(max_id,-1,-1):
        source = -1
        src_len = -1
        for index, blk in enumerate(ordered):
            if blk.id == to_move:
                source = index
                src_len = blk.length
                break
        dest = -1
        dst_len = -1
        for index, blk in enumerate(ordered):
            if blk.id is None and blk.length >= src_len:
                dest = index
                dst_len = blk.length
                break
            if index > source:
                break
        if dest == -1 or source < dest:
            continue #No suitable destination. 
        #Want to keep unallocated space contiguous...
        #First, if the destination area exactly fits, move the file in there.
        if src_len == dst_len:
            ordered[dest].id = to_move
            ordered[source].id = None
        else:
            #Otherwise: swap the blocks around, and add a new empty block to hold the additional free space.
            new_empty = Block(dst_len - src_len)
            ordered[dest],ordered[source] = ordered[source],ordered[dest]
            ordered.insert(dest+1,new_empty)# this will wreak merry havoc on execution time :(
            source += 1
        



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
