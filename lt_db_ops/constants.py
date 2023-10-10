
DATABASE_NAME = 'live_ticketing_db'

TABLE_DEPARTMENTS = 'department'
TABLE_EMPLOYEES = 'employees'
TABLE_TASKS = 'tasks'
TABLE_TICKETS = 'tickets'
TABLE_EVENT_TRACKER = 'events_tracker'
TABLE_EVENT_OBJECTS = 'event_objects'
TABLE_EVENT_ACTION = 'event_action'
TABLE_EMAIL_RECORDS = 'email_records'
TABLE_EMAIL_TEMPLATES = 'email_templates'

#DEPARTMENTS COLUMNS
COL_DEP_ID = 'dept_id'
COL_DEP_NAME = 'dept_name'
COL_DEP_MANAGER = 'manager'

# EMPLOYEES COLUMNS
COL_EMP_ID = 'employees_id'
COL_EMP_NAME = 'name'
COL_EMP_EMAIL = 'email'
COL_EMP_DEPT = 'department' # FK --> Department ID
COL_EMP_POSITION = 'position'

#TASKS COLUMNS
COL_TAS_ID = 'task_id'
COL_TAS_DESCRIPTION = 'description'
COL_TAS_TICKET_ID = 'ticket_id' #FK --> Ticket ID
COL_TAS_STATUS = 'status' 
COL_TAS_ASSIGNED_TO = 'assigned_to'
COL_TAS_ASSIGNED_DATE = 'assigned_date'

#TICKETS COLUMNS
COL_TIC_ID = 'ticket_id' # PK Unique
COL_TIC_ASSIGNED_TO = 'assigned_to' #FK --> Employees ID
COL_TIC_STATUS = 'status'
COL_TIC_START_DATE = 'start_date'
COL_TIC_CLOSE_DATE = 'close_date'
COL_TIC_DEPARTMENT = 'department' #FK --> Department ID
COL_TIC_DESCRIPTION = 'description'
COL_TIC_OWNER = 'owner' # FK --> Employees ID ... the person who opened the ticket

# Events Tracker COLUMNS
COL_EVT_EVENT_ID = 'event_id'
COL_EVT_TICKET_ID = 'ticket_id'
COL_EVT_OBECT = 'object'
COL_EVT_ACTION = 'action'
COL_EVT_TIMESTAMP = 'time_stamp'
COL_EVT_EMPLOYEE_ID = 'employee_id'

# EVents Action COLUMNS
COL_EVA_ID = 'action_id'
COL_EVA_NAME = 'action_name'

#EVENT OBJECT COLUMNS
COL_EVO_ID=  'object_id'
COL_EVO_NAME = 'object_name'

# EMAIL RECORDS COLUMNS
COL_ER_ID = 'email_id'
COL_ER_SUBJECT = 'subject'
COL_ER_TEMPLATE = 'template'
COL_ER_RECIPIENT = 'recipient'
COL_ER_TICKET_ID = 'ticket_id'
COL_ER_STATUS = 'status'
COL_ER_ACTUATOR = 'actuator'

# EMAIL TEMPLATES COLUMNS
COL_ET_ID = 'id'
COL_ET_TEMPLATE_NAME = 'template_name'



DB_TABLE_PKS = {
    TABLE_DEPARTMENTS : COL_DEP_ID,
    TABLE_EMPLOYEES : COL_EMP_ID,
    TABLE_TASKS : COL_TAS_ID,
    TABLE_TICKETS : COL_TIC_ID,
    TABLE_EVENT_TRACKER: COL_EVT_EVENT_ID,
    TABLE_EVENT_ACTION:COL_EVA_ID,
    TABLE_EVENT_OBJECTS:COL_EVO_ID,
    TABLE_EMAIL_RECORDS:COL_ER_ID,
    TABLE_EMAIL_TEMPLATES:COL_ET_ID
}

DB_USER_NAME = 'root'
DB_PASSWORD = 'seb4vision23'
DB_HOST = 'localhost'

STATUS_OPEN = 0
STATUS_COMPLETE = 2
STATUS_PRELIM_COMPLETE = 1

TASKS = 'tasks'

#Actions 
ACTION_CREATED = 'CREATED'
ACTION_ASSIGNED = 'ASSIGNED'
ACTION_CLOSED = 'CLOSED'
ACTION_OPENED = 'OPENED'
ACTION_DELETED = 'DELETED'

# OBJECTS
OBJECT_TASK = 'Task'
OBJECT_TICKET = 'Ticket'

#email templates

TEMPLATE_TICKET_ASSIGNED = 'ticket_assigned.html'
TEMPLATE_TICKET_CLOSED = 'ticket_closed.html'
TEMPLATE_TASK_ASSIGNED = 'task_assigned.html'

TEMPLATE_BASE_PATH = 'emails/'

SUBJECT_TICKET_ASSIGNED = 'Ticket Assigned'
SUBJECT_TICKET_CLOSED = 'Ticket Closed'
SUBJECT_TASK_ASSIGNED = 'Task Assigned'

EMAIL_RECORD_STATUS_SENT = 1
EMAIL_RECORD_STATUS_PENDING = 0 # the default status.
