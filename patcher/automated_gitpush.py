import os
def auto_git_update_yaml():
    os.chdir('..')
    os.system('git add patcher/version_history')
    os.system('git commit -m "auto version_history.yaml update')
    os.system('git push origin master')
auto_git_update_yaml()


