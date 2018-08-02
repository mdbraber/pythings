from things_object import *
#!/usr/local/bin/python3

query = Things.upcoming()
#print(Things.expand_sql(query.sql()))

for item in Things.upcoming():
    item_tags = f'(tags: {item.tags})' if item.tags else ""
    #item_date = item.startdate.date() if item.startdate else item.duedate.date()

    if item.startdate:
        item_date = str(item.startdate.date())
    elif item.duedate:
        item_date = str(item.duedate.date())
    elif item.nextinstancestartdate:
        item_date = str(item.nextinstancestartdate.date())
    else:
        item_date = ""

    item_type = '*' if item.type == Things.TYPE_PROJECT else "-"
    item_remaining = f'[{item.openuntrashedleafactionscount}]' if item.openuntrashedleafactionscount > 0 else ""
    print(f'{item_type} {" ".join(filter(None, [item_date,item.title,item_remaining,item_tags]))}')
