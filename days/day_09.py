from dataclasses import dataclass;
from typing import Iterator, Union

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
    memory:list[int] = [-1] * total_length
    write_pointer:int = 0
    
    #Expand blocks
    for block in data:
        if block.id is not None:
            for i in range(block.length):
                memory[i+write_pointer] = block.id
        write_pointer += block.length
    
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

    #Calculate checksum
    retval = 0
    for position,value in enumerate(memory):
        if value == -1:
            break
        retval += position * value
    return f"{retval}"

@dataclass(slots=True,repr=False)
class LinkedBlock:
    """Quickly slapped-together linked list implementation. Handle with care."""
    length:int
    id:int|None = None
    prev:Union["LinkedBlock",None] = None
    next:Union["LinkedBlock",None] = None
    
    def insert_after(self,other:"LinkedBlock"):
        """Puts this node after a given node. Should only be done with a newly
        made node, or a node that has been popped out."""
        old_next = self.next
        self.next = other
        if other is not None:
            other.prev = self
            other.next = old_next
        if old_next is not None:
            old_next.prev = other
    
    def append(self,other:"LinkedBlock"):
        """Puts a node after a given node. Should only be done on the last
        node in the list."""
        self.next = other
        other.prev = self
    
    def pop(self) -> "LinkedBlock":
        """Remove this node from the list. 'safe' to use."""
        n,p = self.next,self.prev
        if n is not None:
            n.prev = p
        if p is not None:
            p.next = n
        self.next = None
        self.prev = None
        return self
    
    def checksum(self,starting_index:int) -> int:
        if self.id is None or self.id == 0:
            return 0
        return sum(self.id * (starting_index+i) for i in range(self.length))
    
    def get_iter(self,read_forward:bool) -> Iterator["LinkedBlock"]:
        return LinkedIterator(self,read_forward)
    
    def __repr__(self):
        return f"LinkedBlock({self.length},{self.id},{"other" if self.prev is not None else "None"},{"other" if self.next is not None else "None"})"

@dataclass
class LinkedIterator:
    current:LinkedBlock
    forward:bool
    
    def __next__(self):
        to_yield = self.current
        if self.current is not None:
            self.current = getattr(self.current,"next" if self.forward else "prev")
            return to_yield
        else:
            raise StopIteration
        
    def __iter__(self):
        return self

def star_two(data:list[IType]) -> str:
    max_id = max(d.id for d in data if d.id is not None)
    
    start = LinkedBlock(data[0].length,data[0].id)
    current = start
    
    for blk in data[1:]:
        newblock = LinkedBlock(blk.length,blk.id)
        current.append(newblock)
        current = newblock
    end = current
    #linked list constructed. Start moving things around.
    for to_find in range(max_id,-1,-1):
        source:LinkedBlock = None
        for blk in end.get_iter(False):
            if blk.id == to_find:
                source = blk
                break
        #print(f"Found block with id {to_find}, length {source.length}")
        dest:LinkedBlock = None
        for blk in start.get_iter(True):
            if blk is source:
                break
            elif blk.id is None and blk.length >= source.length:
                dest = blk
                break
        
        if dest is None:
            continue
        
        diff = dest.length - source.length
        
        if diff > 0:
            remainder = LinkedBlock(diff,None)
            dest.insert_after(remainder)
        dest.id = source.id
        dest.length = source.length
        source.id = None
    retval = 0
    offset = 0
    for blk in start.get_iter(True):
        retval += blk.checksum(offset)
        offset += blk.length
    
    return f"{retval}"
    

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
