import os
import subprocess
from github import Github

# 计算某个 commit 的变更行数
def get_commit_lines(commit):
    command = ['git', 'diff', '--shortstat', commit]
    output = subprocess.check_output(command).decode('utf-8').strip()
    parts = output.split()
    added = int(parts[1])
    deleted = int(parts[3])
    return added - deleted


# 计算所有 commit 的变更行数
def get_total_lines(pr):
    commits = pr.get_commits()
    lines = sum(get_commit_lines(commit.sha) for commit in commits)
    return lines


# 获取 Pull Request 的对象
g = Github(os.getenv('GITHUB_TOKEN'))
repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
pr_number = os.getenv('GITHUB_PULL_REQUEST_NUMBER')
pr = repo.get_pull(pr_number)

# 计算总行数并打标签
total_lines = get_total_lines(pr)
labels = []
if total_lines >= 1:
    labels.append('1+')
if total_lines >= 40:
    labels.append('40+')
if total_lines >= 100:
    labels.append('100+')
if total_lines >= 500:
    labels.append('500+')
if total_lines >= 1000:
    labels.append('1000+')
if total_lines >= 2000:
    labels.append('2000+')
if total_lines >= 5000:
    labels.append('5000+')
pr.add_to_labels(*labels)
