from dataclasses import dataclass;
import re

ROOM_WIDTH:int = 101
ROOM_HEIGHT:int = 103

def wrap(val:int,limit:int) -> int:
    if val > limit:
        return val - limit
    elif val < 0:
        return limit - val
    else:
        return val

class DynamicBot:
    """A robot in 'mid-flight.'"""
    def __init__(self, x, y, h, v):
        self.x = x
        self.y = y
        self.h = h
        self.v = v
    
    def update(self):
        self.x = wrap(self.x + self.h,ROOM_WIDTH)
        self.y = wrap(self.y + self.v,ROOM_HEIGHT)

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

if __name__ == "__main__":
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
