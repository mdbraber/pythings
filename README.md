# pythings
Python interface for Cultured Code Things 3 (using SQLite, Python3.6 and peewee-orm)

# Create database views

This database uses four different database views to ease the handling of items (basically to limit
any queries to non-trashed items and have different views from Tasks, Headings and Projects). See
models.py for the SQL to create these views.

The SQL to create these database views:

```
CREATE VIEW ItemView AS SELECT * FROM TMTask WHERE trashed = 0
CREATE VIEW TaskView AS SELECT * FROM TMTask WHERE type = 0 AND trashed = 0
CREATE VIEW ProjectView AS SELECT * FROM TMTask WHERE type = 1 AND trashed = 0
CREATE VIEW HeadingView AS SELECT * FROM TMTask WHERE type = 2 AND trashed = 0
```

# Required

- Python 3.6 (this code uses formatted string-literals)
- [peewee-orm](https://github.com/coleifer/peewee)
