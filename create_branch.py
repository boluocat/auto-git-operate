from sys import argv
import time
from pathlib import Path
from git_operation import repo_operation

local_git_path = Path(argv[1])
target_branch = argv[2].split(',')
the_repo = repo_operation(local_git_path)

now = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())
print(f'{now}  Create new branch')
the_repo.create_branches(target_branch)