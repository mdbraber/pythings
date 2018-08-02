#!/usr/local/bin/python3
from things import *

last = None
for item in Things.logbook():

    if Things.switch2(item, last, 'stopdate.month'):
        month = item.stopdate.strftime('%B')
        print('')
        print(month)
        print('-'*len(month))

    item_notes = ' ^' if item.notes else ""
    item_tags = f'(tags: {item.tags})' if item.tags else ""
    item_stopdate = str(item.stopdate.strftime('%e %b'))
    item_type = '*' if item.type == Things.TYPE_PROJECT else "-"
    item_project = f'({item.project.title})' if item.project else ""
    item_remaining = f'[{item.openuntrashedleafactionscount}]' if item.openuntrashedleafactionscount >= 0 else ""
    item_title = item.title + item_notes
    print(f'{item_type} {" ".join(filter(None, [item_stopdate,item_title,item_project,item_remaining,item_tags]))}')

    last = item
