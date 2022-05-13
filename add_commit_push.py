from sys import argv
import time
from pathlib import Path
from git_operation import repo_operation

local_git_path = Path(argv[1])
target_add_file = argv[2].split(',') #list
commit_comment = argv[3] #string

the_repo = repo_operation(local_git_path)

now = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())
print(f'{now}  Process new files, include: Add,commit,push')

the_repo.check_status()
the_repo.add_changes(target_add_file)
the_repo.add_commit(commit_comment)
the_repo.push_to_remote()