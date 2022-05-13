from pathlib import Path
import git
import os

class init_repository():
    @classmethod
    def clone_repository(cls, git_url, local_git_path):
        try:
            repo = git.Repo.clone_from(url = git_url, to_path = local_git_path)
            print(f'Clone the git repository successfully')
        except git.exc.GitCommandError as e:
            print(f'git.exc.GitCommandError:{e}')
        
        exists_file = os.listdir(local_git_path)
        if len(exists_file) == 1 and exists_file[0] == '.git':
            print(f'This is an empty repository. Start to create \'README.md\' for this repository.')
            open(f'{local_git_path}/README.md','w').close()
            local_git = repo.git
            local_git.add('README.md')
            local_git.commit('-m', 'to active repository')
            origin = repo.remote()
            origin.push()
            print(f'Send the first file to repository')
        else:
            pass



class repo_operation():

    def __init__(self, local_git_path: Path) -> 'git.Repo':
        self.repo = git.Repo(local_git_path)
        self.git = self.repo.git
        self.remote = self.repo.remote()

    def check_active_branch(self) -> 'Nothing to see here':
        print(f'The active branch is \'{self.repo.active_branch}\'')

    def check_remote_branch(self) -> list:
        remote_branch_str = self.git.branch('-r').replace(' ', '').replace('origin/HEAD->','').replace('origin/','')
        remote_branch_list = remote_branch_str.split('\n')
        print(f'The remote branch: {remote_branch_list[1:]}')
        return remote_branch_list[1:]
    
    def check_local_branch(self) -> dict:
        branch_dict = {}
        for each_branch in self.repo.branches:
            branch_dict[each_branch.name] = each_branch
        branchs = list(branch_dict.keys())
        if (branch_number := len(branchs)) > 1:
            print(f'There are {branch_number} branches in local, they are {branchs}')
        else:
            print(f'There is only {branch_number} branch, it is {branchs}')

        return branch_dict

    def create_branches(self, branch_names: list) -> 'Nothing to see here':
        if  isinstance(branch_names, list):
            for each_branch in branch_names:
                self.repo.create_head(each_branch, 'HEAD')
                print(f'Created a new branch: \"{each_branch}\"')
        else:
            print(f'Please input a list for branch names.')
        

    def check_out_branch(self, target_branch_name: str) -> 'Nothing to see here':
        targe_branch_head = self.check_local_branch()[target_branch_name]
        print(f'It\'s ready for checking out to \'{target_branch_name}\'')
        self.repo.head.reference = targe_branch_head
        print(f'Check out to \"{target_branch_name}\" completely')

    def check_status(self) -> None or list:
        present_status = self.git.status()
        no_change = 'nothing to commit, working tree clean'
        have_change = 'Untracked files:'
        print(present_status)
        if no_change in present_status:
            return None
        elif have_change in present_status:
            first_part, key_part = present_status.split('(use "git add <file>..." to include in what will be committed)\n')
            untracked_files_part, *nots = key_part.split('\n\nnothing added to commit but untracked files present (use "git add" to track)')
            untracked_files = untracked_files_part.replace('\t','').split('\n')
            return untracked_files
    
    def add_changes(self, files: list) -> 'Nothing to see here':
        for each_file in files:
            try:
                self.git.add(each_file)
                print(f'Add {each_file} successfully')
            except git.exc.GitCommandError as e:
                print(f'Failed to add \'{each_file}\': {e}')

        assert isinstance(files, list), 'The input parameter should be a list'

    def restore_add(self, files: list) -> 'Nothing to see here':
        for each_file in files:
            try:
                self.git.restore('--staged',each_file)
                print(f'Restored {each_file} successfully')
            except git.exc.GitCommandError as e:
                print(f'Failed to restore \'{each_file}\': {e}')

        assert isinstance(files, list), 'The input parameter should be a list'

    def add_commit(self, commit_info: str) -> 'Nothing to see here':
        try:
            self.git.commit('-m', commit_info)
            print(f'Add the commit successfully')
        except git.exc.GitCommandError as e:
            error_info = str(e).split('\n')[-1]
            print(f'Failed to add commit: {error_info}')

        assert isinstance(commit_info, str), 'The input parameter should be a string'

    def reset_commit(self, commit_times: int = 1) -> 'Nothing to see here':
        self.git.reset('--soft', f'HEAD~{commit_times}')
        print(f'Completely reset {commit_times} commits from branch')

    def reset_commit_plus_add(self, commit_times = 1) -> 'Nothing to see here':
        self.git.reset('--hard', f'HEAD~{commit_times}')
        print(f'Completely reset {commit_times} adds with commits from branch')

    def push_to_remote(self) -> 'Nothing to see here':
        target_barch = self.repo.head.reference
        print(f'It\'s ready for pushing \'{target_barch}\' to remote')
        self.remote.push(target_barch)
        print(f'Push \'{target_barch}\' to remote completely')
    
    def get_git_log(self) -> list:
        print(f'The git log is following:\n\n{self.git.log("--pretty=format:%H   %an %ae   %ai   %s")}')

        return self.repo.head.reference.log()
