from dataclasses import dataclass
from collections import namedtuple
import re
from typing import Literal

Point = namedtuple("Point", "x y")


@dataclass
class ClawGame:
    """Representation of one 'unit' of input-data. May represent as little
    as a single character from input, as much as the entire file, or anywhere
    inbetween."""
    button_a:Point
    button_b:Point
    prize_spot:Point

    def split_print(self):
        print(f"{self.button_a.x}A + {self.button_b.x}B == {self.prize_spot.x}")
        print(f"{self.button_a.y}A + {self.button_b.y}B == {self.prize_spot.y}")

IType = ClawGame

def parse_input(input_content:str) -> list[IType]:
    retval:list[ClawGame] = list()

    button_patt = re.compile(r"Button [AB]: X\+(\d+), Y\+(\d+)")
    prize_patt = re.compile(r"Prize: X=(\d+), Y=(\d+)")

    lines = iter(input_content.splitlines())
    try:
        while True:
            button_a = button_patt.match(next(lines))
            button_b = button_patt.match(next(lines))
            prize = prize_patt.match(next(lines))

            button_a = Point(int(button_a.group(1)),int(button_a.group(2)))
            button_b = Point(int(button_b.group(1)),int(button_b.group(2)))
            prize = Point(int(prize.group(1)),int(prize.group(2)))
            retval.append(ClawGame(button_a,button_b,prize))
            next(lines)
    except StopIteration as e:
        print(e)
        pass

    return retval

def determinant(left:Point, right:Point) -> int:
    return (left.x*right.y) - (right.x*left.y)

class ButtonMatrix:
    def __init__(self, ax:int|Point, ay:int|Point, bx:int|None=None, by:int|None=None):
        if isinstance(ax,Point) and isinstance(ay,Point):
            self.ax = ax.x
            self.ay = ax.y
            self.bx = ay.x
            self.by = ay.y
        elif all(isinstance(v,int) for v in [ax,bx,ay,by]):
            self.ax = ax
            self.ay = ay
            self.bx = bx
            self.by = by
        else:
            raise ValueError()
    
    def determinant(self) -> int:
        return (self.ax * self.by) - (self.ay * self.bx)
    
    def replace_col(self,column:Literal["x","y"],new_values:Point) -> "ButtonMatrix":
        if column == "x":
            return ButtonMatrix(new_values.x,self.ay,new_values.y,self.by)
        elif column == "y":
            return ButtonMatrix(self.ax,new_values.x,self.bx,new_values.y)
        else:
            raise ValueError()
        
    def result(self,a_press:int,b_press:int) -> Point:
        res_x = (self.ax * a_press) + (self.bx * b_press)
        res_y = (self.ay * a_press) + (self.by * b_press)
        return Point(int(res_x),int(res_y))
    
    def __repr__(self):
        return f"ButtonMatrix({self.ax},{self.ay},{self.bx},{self.by})"

def star_one(data:list[IType]) -> str:
    retval = 0

    for game in data:
        game.split_print()
        button_m = ButtonMatrix(game.button_a,game.button_b)
        x_rep = ButtonMatrix(game.prize_spot,game.button_b)
        y_rep = ButtonMatrix(game.button_a,game.prize_spot)

        det = button_m.determinant()
        if det == 0:
            continue
        a_press = x_rep.determinant() / det
        b_press = y_rep.determinant() / det
        if a_press <= 100 and b_press <= 100 and a_press.is_integer() and b_press.is_integer():
            retval += a_press + (3*b_press)

    return f"{retval}"

def star_two(data:list[IType]) -> str:
    pass

if __name__ == "__main__":
    from pathlib import Path
    source = input("Path to input data? (leave blank for 'input/day_13.txt')")
    if source == "" :
        source = Path(__file__).parent.parent / "input" / "day_13.txt"
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
