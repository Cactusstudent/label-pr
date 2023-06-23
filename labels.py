import subprocess

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

import json

with open('config.json', 'r') as f:
    config = json.load(f)

labels = config['labels']
thresholds = config['thresholds']
