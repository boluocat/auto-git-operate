from pathlib import Path
from sys import argv
import time
from git_operation import init_repository

git_url = f'{argv[1]}'
local_git_path = Path(argv[2])
# git_url = f'git@github.com:boluocat/git_test.git'
# local_git_path = Path(f'e:/git/python-tools/git_test')

now = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())
print(f'{now}  Clone the repository from git remote')
init_repository.clone_repository(git_url, local_git_path)