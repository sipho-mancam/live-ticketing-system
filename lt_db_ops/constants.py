
DATABASE_NAME = 'live_ticketing_db'

TABLE_DEPARTMENTS = 'department'
TABLE_EMPLOYEES = 'employees'
TABLE_TASKS = 'tasks'
TABLE_TICKETS = 'tickets'

#DEPARTMENTS COLUMNS
COL_DEP_ID = 'dept_id'
COL_DEP_NAME = 'dept_name'

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


DB_TABLE_PKS = {
    TABLE_DEPARTMENTS : COL_DEP_ID,
    TABLE_EMPLOYEES : COL_EMP_ID,
    TABLE_TASKS : COL_TAS_ID,
    TABLE_TICKETS : COL_TIC_ID
}

DB_USER_NAME = 'root'
DB_PASSWORD = 'seb4vision23'
DB_HOST = 'localhost'

STATUS_OPEN = 0
STATUS_COMPLETE = 2
STATUS_PRELIM_COMPLETE = 1

TASKS = 'tasks'
