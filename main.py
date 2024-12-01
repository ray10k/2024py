from days import *
from time import perf_counter

def run_day(day:int) -> bool:
    assert day in range(1,26)
    
    day_line = f"{current_day:02}"
    parse, star_one, star_two = eval(f"(day_{day_line}.parse_input, day_{day_line}.star_one, day_{day_line}.star_two)")
    input_file = f"input/day_{day_line}.txt"
    input_path = Path(__file__).parent / input_file
    input_data = ""
    with open(input_path) as i_file:
        input_data = i_file.read()
    print(f"Starting day {day_line}.")
    start_time = perf_counter()
    parsed = parse(input_data)
    parse_time = perf_counter()
    result_one = star_one(parsed)
    one_time = perf_counter()
    result_two = star_two(parsed)
    two_time = perf_counter()
    
    print(f"Output 1: {result_one}\nOutput 2: {result_two}")
    print(f"parse/s1/s2 timing: {parse_time-start_time:.3}/{one_time-parse_time:.3}/{two_time-one_time:.3}")
    
    return result_one is not None and result_two is not None

if __name__ == "__main__":
    from argparse import ArgumentParser
    from pathlib import Path
    
    parser = ArgumentParser(prog="Advent of Code 2024",description="A system for running your solutions to the Advent of Code puzzles, 2024 edition!",epilog="Merry coding!")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-A','--All',action='store_true',help="Run all puzzles, instead of up to the first one that returns None.")
    group.add_argument('-d','--day',nargs='+',help="Run only the specified days.", type=int)
    
    arguments = parser.parse_args()
    
    if arguments.day is None:
        #Run all days starting at 1.
        for current_day in range(1,26):
            if not (run_day(current_day) or arguments.All):
                break
    else:
        #Filter down to the valid days.
        valid_days = filter(lambda x: x in range(1,26),arguments.day)
        for day in valid_days:
            run_day(day)
    