#!/usr/local/bin/python3
from things import *

last = None
for item in Things.today():

    if Things.switch(item, last, 'startbucket'):
        print('\nEvening')

    item_tags = f'(tags: {item.tags})' if item.tags else ""
    item_type = '*' if item.type == Things.TYPE_PROJECT else "-"
    item_remaining = f'[{item.openuntrashedleafactionscount}]' if item.openuntrashedleafactionscount > 0 else ""
    print(f'{item_type} {" ".join([item.title,item_remaining,item_tags])}')

    last = item
