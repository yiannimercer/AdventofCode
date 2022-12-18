from dotenv import load_dotenv
load_dotenv()

import aocd
data = aocd.get_data(day=7, year=2022)

sample = '''$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''

def directory_triager(command_string):
    lines = iter(command_string.splitlines())
    assert next(lines) == "$ cd /"
    cwd = "/"  
    directories = {"/": 0}  # map of dirs to their cumulative size
    parent_folders = []  # cwd stack
    for line in lines:
        line = line.split()
        length = len(line)
        command1 = line[0] if length >= 1 else None
        command2 = line[1] if length >= 2 else None
        command3 = line[2] if length >= 3 else None
        # IF MOVING BACK ONE DIRECTORY, CWD BECOMES THE LAST SAVED PARENT DIRECTORY
        if ["$", "cd", ".."] == line:        
            cwd = parent_folders.pop()
        # IF MOVING 
        elif command1 == "$" and command2 == "cd" and command3 != None: 
            parent_folders.append(cwd)
            cwd += command3 + "/"
        elif ["$", "ls"] == line:
            pass
        elif (length == 2) and (command1 == "dir"):
            directories[cwd + command2 + "/"] = 0
        elif command1.isdigit():
            size = int(command1)
            for d in parent_folders + [cwd]:
                directories[d] += size
        else:
            print(f"FAILED ON: LINE: {line}")
    return directories

sample_directory = directory_triager(sample)
data_directory = directory_triager(data)

# ANSWER FOR PART A
answer_a = sum(dir for dir in data_directory.values() if dir <= 100000)

aocd.submit(answer_a, day=7, year=2022)

# ANSWER FOR PART B
hard_drive_maximum = 70000000
required_update_space = 30000000
used_space = data_directory['/']
available_space = hard_drive_maximum - used_space
need_to_delete = required_update_space - available_space

print(f"We need to delete {need_to_delete} worth of space")

answer_b = min(dir for dir in data_directory.values() if dir >= need_to_delete)

aocd.submit(answer_b, day=7, year=2022)