from dataclasses import dataclass;
import re

ROOM_WIDTH:int = 101
ROOM_HEIGHT:int = 103

def wrap(val:int,limit:int) -> int:
    if val >= limit:
        return val % limit
    elif val < 0:
        return limit + val
    else:
        return val

@dataclass
class DynamicBot:
    """A robot in 'mid-flight.'"""
    x:int
    y:int
    h:int
    v:int
    
    def update(self):
        self.x = wrap(self.x + self.h,ROOM_WIDTH)
        self.y = wrap(self.y + self.v,ROOM_HEIGHT)

def print_bot_map(bots:list[DynamicBot],w:int,h:int):
    here:dict[tuple[int,int],int] = dict()
    display = "0123456789abcdefghijklmnopqrstuvwxyz!"

    for bot in bots:
        count = here.get((bot.x,bot.y),0)
        here[(bot.x,bot.y)] = count + 1

    for y in range(h):
        for x in range(w):
            count = here.get((x,y),0)
            if count == 0:
                print(end=" ")
            elif count < len(display):
                print(display[count],end="")
            else:
                print("@",end="")
        print()

@dataclass(frozen=True,slots=True)
class RobotStats:
    """One security robot's initial state."""
    start_x:int
    start_y:int
    velocity_x:int
    velocity_y:int

    def get_dynamic(self) -> DynamicBot:
        return DynamicBot(self.start_x,self.start_y,self.velocity_x,self.velocity_y)

IType = RobotStats
BOT_PARSE = re.compile(r"p=(?P<x>\d+),(?P<y>\d+) v=(?P<h>\-?\d+),(?P<v>\-?\d+)")

def parse_input(input_content:str) -> list[IType]:
    retval:list[IType] = list()
    for line in input_content.splitlines():
        data = BOT_PARSE.match(line)
        retval.append(RobotStats(int(data.group("x")),int(data.group("y")),int(data.group("h")),int(data.group("v"))))
    return retval

def star_one(data:list[IType]) -> str:
    bots = [init.get_dynamic() for init in data]
    h_mid = int((ROOM_WIDTH - 1) / 2)
    v_mid = int((ROOM_HEIGHT - 1) / 2)

    for _ in range(100):
        for bot in bots:
            bot.update()
    tl = tr = bl = br = 0

    for bot in bots:
        if bot.x < h_mid:
            if bot.y < v_mid:
                tl += 1
            elif bot.y > v_mid:
                bl += 1
        elif bot.x > h_mid:
            if bot.y < v_mid:
                tr += 1
            elif bot.y > v_mid:
                br += 1
    return f"{tl*tr*bl*br}"

def star_two(data:list[IType]) -> str:
    pass

def test_case():
    global ROOM_HEIGHT,ROOM_WIDTH
    ROOM_WIDTH = 11
    ROOM_HEIGHT = 7
    test_data = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
    parsed = parse_input(test_data)
    a_bots = [b.get_dynamic() for b in parsed]

    print_bot_map(a_bots,11,7)
    print("+"*11)

    for i in range(100):
        for bot in a_bots:
            bot.update()

    print_bot_map(a_bots,11,7)

        
    ROOM_WIDTH = 101
    ROOM_HEIGHT = 103

if __name__ == "__main__":
    test_case()
    #print(test_case())
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_14.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_14.txt"
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
