#!/usr/local/bin/python3
from things import *

# Configuration
limit = 0

# Initialize loop
last = None
project_count = 0
project_level = heading_level = task_level = 0
SPACE = "  "

for task in Things.someday():
    if task.area and Things.switch(task, last, 'area'):
        project_count  = 0
        project_level = heading_level = task_level = 1
        print(f'\n# {task.area.title.upper()}\n')
    if task.project and Things.switch(task, last, 'project'):
        project_count = 0
        task_level = heading_level = project_level + 1
        print(f'{SPACE*project_level}* {task.project.title}')
    if not limit or project_count < limit:
        task_tags = f'(tags: {task.tags})' if task.tags else ""
        print(f'{SPACE*task_level}- {" ".join([task.title,task_tags])}')

    if task.project or task.heading: project_count += 1
    last = task
