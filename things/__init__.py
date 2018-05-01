from .models import *
import sqlparse

class Things(object):

    TYPE_TASK = 0
    TYPE_PROJECT = 1
    TYPE_HEADING = 2

    UUID_LENGTH_NORMAL = 33
    UUID_LENGTH_RECURRING = 45

    @staticmethod
    def expand_sql(sql):
        statement = sql[0]
        params = [ 'NULL' if x == None else x for x in sql[1] ]
        statement = statement.replace('?','{}')
        return sqlparse.format(statement.format(*params),reindent=True)

    @staticmethod
    def switch(current, last, field):
        if not (current and last):
            return bool(getattr(current, field))

        return (getattr(last, field) != getattr(current, field))

    @staticmethod
    def switch2(current, last, method):
        if not (current and last):
            return bool(eval('current.'+method))

        if ((not eval('last.'+method)) or eval('last.'+method) != eval('current.'+method) ):
            return True

        return False


    @staticmethod
    def inbox():
        return (Task
            .select(Task, Project, fn.group_concat(Tag.title).alias('tags'))
            .join(Project, JOIN.LEFT_OUTER)
            .switch(Task)
            .join(TaskTag, JOIN.LEFT_OUTER)
            .join(Tag, JOIN.LEFT_OUTER)
            .where((Task.start == 0) & (Task.status == 0))
            .group_by(Task)
            .order_by(Task.index)
        )

    @staticmethod
    def today():
        return (Item
            .select(Item, Project, fn.group_concat(Tag.title).alias('tags'))
            .join(Project, JOIN.LEFT_OUTER)
            .switch(Item)
            .join(ItemTag, JOIN.LEFT_OUTER)
            .join(Tag, JOIN.LEFT_OUTER)
            .where((Item.startdate.is_null(False)) & (Item.status == 0) & (Item.start == 1))
            .group_by(Item)
            .order_by(Item.startbucket, Item.todayindex)
        )

    @staticmethod
    def upcoming():
        refdate = datetime.today()
        return (Item
            .select(Item, Project, fn.group_concat(Tag.title).alias('tags'))
            .join(Project, JOIN.LEFT_OUTER)
            .switch(Item)
            .join(ItemTag, JOIN.LEFT_OUTER)
            .join(Tag, JOIN.LEFT_OUTER)
            .where((Item.status == 0) & ( ( (Item.start == 2) & ( (Item.startdate > refdate) | (Item.nextinstancestartdate > refdate) ) ) | (Item.duedate > refdate ) ) )
            .group_by(Item)
            .order_by(fn.COALESCE(Item.startdate, Item.duedate, Item.nextinstancestartdate))
        )

    @staticmethod
    def anytime():
        return (Task
            .select(Task, Project, Heading, Area, fn.group_concat(Tag.title).alias('tags'))
            .join(TaskTag, JOIN.LEFT_OUTER)
            .join(Tag, JOIN.LEFT_OUTER)
            .switch(Task)
            .join(Heading, JOIN.LEFT_OUTER)
            .switch(Task)
            .join(Project, JOIN.LEFT_OUTER, on=((Task.project == Project.uuid) | (Heading.project == Project.uuid)))
            .switch(Task)
            .join(Area, JOIN.LEFT_OUTER, on=((Task.area == Area.uuid) | (Project.area == Area.uuid)))
            .where((Task.start == 1) & (Task.status == 0))
            .group_by(Task.uuid)
            .order_by(Area.index, Project.index, Task.type, Heading.index, Task.index)
        )

    @staticmethod
    def someday():
        return (Task
            .select(Task, Project, Heading, Area, fn.group_concat(Tag.title).alias('tags'))
            .join(TaskTag, JOIN.LEFT_OUTER)
            .join(Tag, JOIN.LEFT_OUTER)
            .switch(Task)
            .join(Heading, JOIN.LEFT_OUTER)
            .switch(Task)
            .join(Project, JOIN.LEFT_OUTER, on=((Task.project == Project.uuid) | (Heading.project == Project.uuid)))
            .switch(Task)
            .join(Area, JOIN.LEFT_OUTER, on=((Task.area == Area.uuid) | (Project.area == Area.uuid)))
            .where((Task.start == 2) & (Task.status == 0))
            .group_by(Task.uuid)
            .order_by(Area.index, Project.index, Task.type, Heading.index, Task.index)
        )

    @staticmethod
    def logbook():
        return (Item
            .select(Item, Project, fn.group_concat(Tag.title).alias('tags'))
            .join(Project, JOIN.LEFT_OUTER)
            .switch(Item)
            .join(ItemTag, JOIN.LEFT_OUTER)
            .join(Tag, JOIN.LEFT_OUTER)
            .where((Item.status == 3) & ((((fn.LENGTH(Item.uuid) == 36) & (Item.type == Things.TYPE_TASK))) | (fn.LENGTH(Item.uuid).in_([36,45]) & (Item.type == Things.TYPE_PROJECT)) ))
            .group_by(Item)
            .order_by(Item.stopdate.desc())
        )
