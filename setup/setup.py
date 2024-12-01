
if __name__ == "__main__":
    from pathlib import Path
    from shutil import copy
    
    destination = input("Specify where to initialize the repository, or leave blank to initialize to the current working directory.")
    root_path = None
    
    if destination == "":
        root_path = Path.cwd()
    else:
        root_path = Path(destination)
    
    (root_path / "input").mkdir(parents=True,exist_ok=True)
    (root_path / "days").mkdir(exist_ok=True)
    
    template_path = Path(__file__).parent / "day_template"
    day_template = ""
    with open(template_path) as t_file:
        day_template = t_file.read()
    
    for day in range(1,26):
        day_number = f"{day:02}"
        day_path = root_path / "days" / f"day_{day_number}.py"
        with open(day_path,"w") as script:
            script.write(day_template.format(day = day_number,result_one = "{result_one}",result_two = "{result_two}"))
        (root_path / "input" / f"day_{day_number}.txt").touch()
    
    main_source = Path(__file__).parent / "main_template"
    main_destination = root_path / "main.py"
    copy(main_source,main_destination)
    
    ignore_source = Path(__file__).parent / "gitignore_template"
    ignore_destination = root_path / ".gitignore"
    copy(ignore_source,ignore_destination)
    
    init_source = Path(__file__).parent / "init_template"
    init_destination = root_path / "days" / "__init__.py"
    copy(init_source,init_destination)
