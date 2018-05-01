from peewee import *
from peewee import _date_part
from datetime import datetime
from pathlib import Path
import time
import sqlparse

database = SqliteDatabase(str(Path.home()) + '/Library/Containers/com.culturedcode.ThingsMac/Data/Library/Application Support/Cultured Code/Things/Things.sqlite3', **{})

class FloatDateTimeField(Field):
    field_type = 'float'

    def python_value(self, value):
        if value and value > 0.0:
            value = datetime.fromtimestamp(value)
        else:
            value = None
        return value

    def db_value(self, value):
        return time.mktime(value.timetuple()) if value is not None else value

    year = property(_date_part('year'))
    month = property(_date_part('month'))
    day = property(_date_part('day'))
    hour = property(_date_part('hour'))
    minute = property(_date_part('minute'))
    second = property(_date_part('second'))

class BaseModel(Model):

    class Meta:
        database = database
        pragmas = (('temp_store', True))

class Meta(BaseModel):
    key = TextField(null=True, primary_key=True)
    value = TextField(null=True)

    class Meta:
        table_name = 'Meta'

class Area(BaseModel):
    index = IntegerField(null=True)
    title = TextField(null=True)
    uuid = TextField(null=True, primary_key=True)
    visible = IntegerField(null=True)

    class Meta:
        table_name = 'TMArea'

class Contact(BaseModel):
    appleaddressbookid = TextField(column_name='appleAddressBookId', null=True)
    displayname = TextField(column_name='displayName', null=True)
    emails = TextField(null=True)
    firstname = TextField(column_name='firstName', null=True)
    index = IntegerField(null=True)
    lastname = TextField(column_name='lastName', null=True)
    uuid = TextField(null=True, primary_key=True)

    class Meta:
        table_name = 'TMContact'

class Tag(BaseModel):
    index = IntegerField(null=True)
    parent = TextField(null=True)
    shortcut = TextField(null=True)
    title = TextField(null=True)
    useddate = FloatDateTimeField(column_name='usedDate', null=True)
    uuid = TextField(null=True, primary_key=True)

    class Meta:
        table_name = 'TMTag'

ItemTagDeferred = DeferredThroughModel()
TaskTagDeferred = DeferredThroughModel()
ProjectTagDeferred = DeferredThroughModel()

class BaseItem(BaseModel):
    aftercompletionreferencedate = FloatDateTimeField(column_name='afterCompletionReferenceDate', null=True)
    alarmtimeoffset = FloatDateTimeField(column_name='alarmTimeOffset', null=True)
    area = ForeignKeyField(Area, db_column='area', backref='tasks', null=True)
    checklistitemscount = IntegerField(column_name='checklistItemsCount', null=True)
    creationdate = FloatDateTimeField(column_name='creationDate', null=True)
    delegate = TextField(null=True)
    duedate = FloatDateTimeField(column_name='dueDate', null=True)
    duedateoffset = IntegerField(column_name='dueDateOffset', null=True)
    duedatesuppressiondate = FloatDateTimeField(column_name='dueDateSuppressionDate', null=True)
    heading = ForeignKeyField('self', db_column='actionGroup', backref='items', null=True)
    index = IntegerField(null=True)
    instancecreationcount = IntegerField(column_name='instanceCreationCount', null=True)
    instancecreationpaused = IntegerField(column_name='instanceCreationPaused', null=True)
    instancecreationstartdate = FloatDateTimeField(column_name='instanceCreationStartDate', null=True)
    lastalarminteractiondate = FloatDateTimeField(column_name='lastAlarmInteractionDate', null=True)
    nextinstancestartdate = FloatDateTimeField(column_name='nextInstanceStartDate', null=True)
    """ Notes """
    notes = TextField(null=True)
    """ Number of open Checklistitems? """
    openchecklistitemscount = IntegerField(column_name='openChecklistItemsCount', null=True)
    """ Non-deleted, non-completed sub-items """
    openuntrashedleafactionscount = IntegerField(column_name='openUntrashedLeafActionsCount', null=True)
    project = ForeignKeyField('self', db_column='project', backref='items', null=True)
    recurrencerule = BlobField(column_name='recurrenceRule', null=True)
    repeatingtemplate = TextField(column_name='repeatingTemplate', index=True, null=True)
    """
    Start:
    0: Inbox ("not started")
    1: Started ("normal")
    2: Someday ("postponed")
    """
    start = IntegerField(index=True, null=True)
    """
    Bucket in Today
    """
    startbucket = IntegerField(column_name='startBucket', null=True)
    startdate = FloatDateTimeField(column_name='startDate', null=True)
    """
    Item status:
    0: Uncompleted / Open
    1: Unknown(?)
    2: Cancelled
    3: Completed
    """
    status = IntegerField(null=True)
    """ Completion date """
    stopdate = FloatDateTimeField(column_name='stopDate', null=True)
    """ Item title """
    title = TextField(null=True)
    """ Item index (order) the Today view """
    todayindex = IntegerField(column_name='todayIndex', null=True)
    todayindexreferencedate = FloatDateTimeField(column_name='todayIndexReferenceDate', null=True)
    trashed = IntegerField(null=True)
    type = IntegerField(index=True, null=True)
    """ Non-deleted (completed or non-completed) sub-items """
    untrashedleafactionscount = IntegerField(column_name='untrashedLeafActionsCount', null=True)
    """ Last modification date """
    usermodificationdate = FloatDateTimeField(column_name='userModificationDate', null=True)
    """ Unique identifier """
    uuid = TextField(null=True, primary_key=True)

    class Meta:
        table_name = 'TMTask'
        indexes = (
            (('start', 'type'), False),
            (('stopdate', 'alarmtimeoffset'), False),
        )

class Heading(BaseItem):
    heading = TextField(column_name="actionGroup", null=True)

    class Meta:
        table_name = 'HeadingView'

class Project(BaseItem):
    heading = TextField(column_name="actionGroup", null=True)
    project = TextField(column_name="project", null=True)

    class Meta:
        table_name = 'ProjectView'

class Task(BaseItem):
    heading = ForeignKeyField(Heading, db_column='actionGroup', backref='tasks', null=True)
    project = ForeignKeyField(Project, db_column='project', backref='tasks', null=True)

    class Meta:
        table_name = 'TaskView'

class Item(BaseItem):
    heading = ForeignKeyField(Heading, db_column='actionGroup', backref='tasks', null=True)
    project = ForeignKeyField(Project, db_column='project', backref='tasks', null=True)

    class Meta:
        table_name = 'ItemView'

class Checklistitem(BaseModel):
    creationdate = FloatDateTimeField(column_name='creationDate', null=True)
    index = IntegerField(null=True)
    status = IntegerField(null=True)
    stopdate = FloatDateTimeField(column_name='stopDate', null=True)
    #task = TextField(index=True, null=True)
    task = ForeignKeyField(Task, db_column = 'task', backref='checklistitems')
    title = TextField(null=True)
    usermodificationdate = FloatDateTimeField(column_name='userModificationDate', null=True)
    uuid = TextField(null=True, primary_key=True)

    class Meta:
        table_name = 'TMChecklistItem'

class ItemTag(BaseModel):
    tag = ForeignKeyField(Tag, db_column='tags', backref='items')
    task = ForeignKeyField(Item, db_column='tasks', backref='tags')

    class Meta:
        table_name = 'TMTaskTag'
        primary_key = False

class TaskTag(BaseModel):
    tag = ForeignKeyField(Tag, db_column='tags', backref='tasks')
    task = ForeignKeyField(Task, db_column='tasks', backref='tags')

    class Meta:
        table_name = 'TMTaskTag'
        primary_key = False

class ProjectTag(BaseModel):
    tag = ForeignKeyField(Tag, db_column='tags', backref='projects')
    task = ForeignKeyField(Project, db_column='tasks', backref='tags')

    class Meta:
        table_name = 'TMTaskTag'
        primary_key = False

class AreaTag(BaseModel):
    tag = ForeignKeyField(Tag, db_column='tags', backref='areas')
    task = ForeignKeyField(Project, db_column='tasks', backref='tags')

    class Meta:
        table_name = 'TMTaskTag'
        primary_key = False
