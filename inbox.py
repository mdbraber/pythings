#!/usr/local/bin/python3.6
from things import *

for task in Things.inbox():
    task_tags = f'(tags: {task.tags})' if task.tags else ""
    print(f'- {" ".join([task.title,task_tags])}')
