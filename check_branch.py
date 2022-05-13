from pathlib import Path
from sys import argv
import time
from git_operation import repo_operation



local_git_path = Path(argv[1])
the_repo = repo_operation(local_git_path)
now = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())
print(f'{now}  Process check brach task')
the_repo.check_remote_branch()
the_repo.check_local_branch()
the_repo.check_active_branch()