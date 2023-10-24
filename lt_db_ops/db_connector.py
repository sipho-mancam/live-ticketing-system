import mysql.connector
from .constants import *
import datetime
import time
from . import utils

class DatabaseConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.table_id_cols = DB_TABLE_PKS

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                pass
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            raise(mysql.connector.Error("Failed to connect to mysql server"))

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
        

    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            self.connection.rollback()
        finally:
            return cursor
    
    def is_connected(self):
        if self.connection:
            return self.is_connected()
        else:
            return False

    def insert_data(self, table:str, columns:tuple, data:list[tuple]):
        if type(columns) is tuple:
            s = [c for c in columns]
            cols = "(" +" , ".join(s) + ")"
            pc_holder = "(" + " , ".join(["%s" for c in columns]) + ")"
        elif type(columns) is str:
            s = "(" + columns + ")"
            cols = s
            pc_holder = "(%s)"
        else:
            s = "("+columns + ")"
            cols = s
            pc_holder = "(%s)"
        
        cursor = self.connection.cursor()
        try:
            for item in data:
                cursor.execute(f"INSERT INTO {table} {cols} VALUES {pc_holder}", item)
            self.connection.commit()
            print("Data inserted successfully")
        except mysql.connector.Error as err:
            self.connection.rollback()
            print("Error: {}".format(err))
            return "Error: {}".format(err) , -1
            
        finally:
            return cursor
            cursor.close()
            

    def read_data(self, table:str=None, columns:tuple|str=None, condition:str=None, query=None):
        res = []
        if type(columns) is tuple:
            columns = " ,".join(columns)
        
        cursor = self.connection.cursor()
        try:
            if query is None:
                cursor.execute(f"SELECT {columns} FROM {table} WHERE {condition}")
            else:
                cursor.execute(query)

            cols = cursor.column_names;
            d_obj = {}
            for item in cursor:
                for name, value in zip(cols, item):
                    d_obj[name] = value
                res.append(d_obj)
                d_obj = {}
            return res
        except mysql.connector.Error as err:
            self.connection.rollback()
            print("Error: {}".format(err))
            return "Error: {}".format(err) , -1
    
    def get_id_by_name(self, table, condition):
        id_col = self.table_id_cols[table]
        columns = (f"{id_col}", )
        if id_col is not None:
            data = self.read_data(table, columns, condition)
            if type(data) is list:
                return data[0]
        return {}

    def read_event_data(self, ticket_id):
        res = []
        
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT " 
                                "et.time_stamp, "
                                "et.ticket_id, "
                                "eo.object_name, "
                                "ea.action_name, "
                                "e.name, "
                                "e.employees_id "
                            "FROM events_tracker et "
                            "JOIN tickets t ON t.ticket_id = et.ticket_id "
                            "JOIN employees e ON e.employees_id = et.employee_id "
                            "JOIN event_action ea ON ea.action_id = et.action "
                            "JOIN event_objects eo ON eo.object_id = et.object "
                            "WHERE et.ticket_id = {} ORDER BY et.time_stamp DESC; ".format(ticket_id))
            cols = cursor.column_names;
            d_obj = {}
            for item in cursor:
                for name, value in zip(cols, item):
                    if name == 'time_stamp':
                        d_obj[name] = value.__str__()
                    else:
                        d_obj[name] = value

                res.append(d_obj)
                d_obj = {}
            return res
        except mysql.connector.Error as err:
            self.connection.rollback()
            print("Error: {}".format(err))
            return "Error: {}".format(err) , -1
        
    def _make_list(self, param):
        if type(param) is not list:
            return [param]
        else:
            return param

    def update_data(self, table:str, columns:list[str], id:list[str]|str, values:list[str]):
        columns = self._make_list(columns)
        id = self._make_list(id)
        values = self._make_list(values)
        tables_id_cols = DB_TABLE_PKS

        cursor = self.connection.cursor()
        try:
            for col, val, id in zip(columns, values, id):
               cursor.execute(f"UPDATE {table} SET {col} = {val} WHERE {tables_id_cols[table]} = {id}")
            self.connection.commit()
            print("Data updated successfully")
        except mysql.connector.Error as err:
            self.connection.rollback()
            print("Error: {}".format(err))
            return "Error: {}".format(err) , -1
        
    def delete_data(self, table:str, condition:str):
        tables_id_cols = DB_TABLE_PKS
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"DELETE FROM {table} WHERE {condition}")
            self.connection.commit()
            print("Record Deleted Successfully")
            return cursor
        except mysql.connector.Error as err:
            self.connection.rollback()
            print(f"Error: {err}")
            return f"Error: {err}", -1

        

class DBEndpoint(DatabaseConnector):
    def __init__(self, host, user, password, database):
        super().__init__(host, user, password, database)

    def insert_email_record(self, record:tuple|list[tuple]):
        record = self._make_list(record)

        return self.insert_data(TABLE_EMAIL_RECORDS, 
                                (COL_ER_SUBJECT, COL_ER_TEMPLATE, COL_ER_RECIPIENT, COL_ER_TICKET_ID, COL_ER_STATUS, COL_ER_ACTUATOR),
                                record)
    
    def get_unsent_records(self):
        query = f"""SELECT 
                    er.email_id,
                    er.subject,
                    er.ticket_id,
                    er.actuator,
                    e.name as recipient_name,
                    e.email as recipient_email,
                    et.template_name as template,
                    er.time_stamp
                FROM live_ticketing_db.email_records er
                JOIN live_ticketing_db.employees e ON e.employees_id = er.recipient
                JOIN live_ticketing_db.email_templates et ON et.id = er.template
                WHERE er.status = 0;"""
        return self.read_data(query=query)
    
    def update_unsent_to_sent_batch(self, ids:list|int):
        ids = self._make_list(ids)
        for id in ids:
            self.update_data(TABLE_EMAIL_RECORDS, COL_ER_STATUS, id, EMAIL_RECORD_STATUS_SENT)
        
        return None

    def get_template_id(self, template_name):
        condition = f"{COL_ET_TEMPLATE_NAME} = '{template_name}'"
        id =  self.get_id_by_name(TABLE_EMAIL_TEMPLATES, condition)
        if len(id.keys()) > 0:
            return id[self.table_id_cols[TABLE_EMAIL_TEMPLATES]]
        return id    
    
    def append_mail_record(self, subject:str, template_id:int, recipient_id:int, ticket_id:int, status:int, actuator:str, **kwargs):
        record = (subject, template_id, recipient_id, ticket_id, status, actuator)
        return self.insert_email_record(record)
    
    def insert_employees(self, employees:list):
        if type(employees) is tuple:
            employees = [employees]
        return self.insert_data(TABLE_EMPLOYEES, 
                                (COL_EMP_NAME,COL_EMP_EMAIL, COL_EMP_DEPT, COL_EMP_POSITION),
                                employees)
    
    def insert_tickets(self, tickets:list|tuple):
        if type(tickets) is tuple:
            tickets = self._make_list(tickets)
        return self.insert_data(TABLE_TICKETS, 
                                (COL_TIC_ASSIGNED_TO, COL_TIC_STATUS, COL_TIC_START_DATE, COL_TIC_CLOSE_DATE, COL_TIC_DEPARTMENT, COL_TIC_DESCRIPTION, COL_TIC_OWNER), 
                                tickets)

    def insert_tasks(self, tasks:list|tuple):
        tasks = self._make_list(tasks)

        return self.insert_data(TABLE_TASKS, 
                                (COL_TAS_DESCRIPTION, COL_TAS_TICKET_ID, COL_TAS_STATUS, COL_TAS_ASSIGNED_TO, COL_TAS_ASSIGNED_DATE), 
                                tasks)
    
    def insert_event(self, event:tuple):
        event = self._make_list(event)
        return self.insert_data(TABLE_EVENT_TRACKER, 
                                (COL_EVT_TICKET_ID, COL_EVT_OBECT, COL_EVT_ACTION, COL_EVT_EMPLOYEE_ID), 
                                event)
    def insert_filter(self, e_id:int, q_filter:str):
        f = (e_id, q_filter)
        f = self._make_list(f)
        return self.insert_data(TABLE_USER_FILTERS, 
                                (COL_UF_EID, COL_UF_FQ),
                                f)

    def does_have_filter(self, e_id:int)->bool:
        res = self.read_filter(e_id)
        return len(res)>0
    
    def read_filter(self, e_id:int):
        condition = f"{COL_UF_EID} = {e_id}"
        f_res = self.read_data(TABLE_USER_FILTERS, ('*',), condition)
        if len(f_res) > 0:
            return f_res[0][COL_UF_FQ]
        else:
            return ""    
    
    def add_event(self, ticket_id, object_id, action_id, employee_id):
        evt = (ticket_id, object_id, action_id, employee_id)
        return self.insert_event(evt)
    
    def create_task(self, ticket_id:int, assigned_to:int, description:str):
        assigned_date = utils.get_current_date_string()
        task = (description, ticket_id, STATUS_OPEN, assigned_to, assigned_date)
        return self.insert_tasks(task)

    def create_ticket(self, assign_to:int, department:int, description:str, owner:int):
        start_date = utils.get_current_date_string()
        ticket = (assign_to, STATUS_OPEN, start_date, None, department, description, owner)
        return self.insert_tickets(ticket)

    def insert_department(self, departments:list|tuple):
        departments = self._make_list(departments) # departments is a list of ('department', manager_id)
        return self.insert_data(TABLE_DEPARTMENTS, (COL_DEP_NAME, COL_DEP_MANAGER), departments)
    

    def read_employees(self, cols = ("*",),  condition = None)->list[tuple]:       
        if condition is None:
            condition = f"{COL_EMP_ID} > 0" # this will select all the employees on the db
        return self.read_data(TABLE_EMPLOYEES, cols, condition)
    
    def read_one_employee(self, id):
        condition = f"{COL_EMP_ID} = {id}"
        return self.read_employees(condition=condition)
    
    def read_employee_from_email(self, email) ->list[tuple]:
        condition=  f"{COL_EMP_EMAIL} = '{email}'"
        return self.read_employees(condition=condition)
    
    def read_departments(self, cols = ("*",),  condition = None)->list[tuple]:
        if condition is None:
            condition = f"{COL_DEP_ID} > 0" # this will return all departments
        return self.read_data(TABLE_DEPARTMENTS, cols, condition)

    def read_one_department(self, id)->list[tuple]:
        condition = f"{COL_DEP_ID} = {id}"
        return self.read_departments(condition=condition)
    
    def read_department_by_name(self, name:str)->list[tuple]:
        condition = f"{COL_DEP_NAME} = '{name}'"
        return self.read_departments(condition=condition)
    
    def read_tasks(self, ticket_id)->list[tuple]:
        condition = f"{COL_TAS_TICKET_ID} = {ticket_id} ORDER BY status ASC, assigned_date DESC"
        return self.read_data(TABLE_TASKS, ("*", ), condition)
    
    def read_one_task(self, task_id)->list[tuple]:
        condition = f"{COL_TAS_ID} = {task_id}"
        return self.read_data(TABLE_TASKS, ("*", ), condition=condition)
    
    def read_tickets(self, cols = ("*",),  condition = None)->list[tuple]:
        if condition is None:
            condition = f"{COL_TIC_ID} > 0 ORDER BY start_date DESC" # this will return all tickets
        else:
            condition = f"{condition} ORDER BY start_date DESC"
        return self.read_data(TABLE_TICKETS, cols, condition)
    
    def read_one_ticket(self, ticket_id)->list[tuple]:
        condition = f"{COL_TIC_ID} = {ticket_id}"
        return self.read_tickets(condition=condition)
    
    def read_actions(self)->list[tuple]:
        return self.read_data(TABLE_EVENT_ACTION, ('action_name',))

    def read_objects(self)->list[tuple]:
        return self.read_data(TABLE_EVENT_OBJECTS, ('object_name', ))
    
    def get_object_id(self, object_name:str)->list[tuple]:
        condition = f"{COL_EVO_NAME} = '{object_name}'"
        res = self.read_data(TABLE_EVENT_OBJECTS, (COL_EVO_ID, ), condition)
        if len(res) > 0:
            id_t  = res[0]
            id = id_t[COL_EVO_ID]
        return id
    
    def get_action_id(self, action_name:str)->int:
        condition = f"{COL_EVA_NAME} = '{action_name}' "
        res = self.read_data(TABLE_EVENT_ACTION, (COL_EVA_ID, ), condition)
        if len(res) > 0:
            id_t  = res[0]
            id = id_t[COL_EVA_ID]
        return id
    
    def update_ticket_status(self, ticket_id, status):
        return self.update_data(TABLE_TICKETS, COL_TIC_STATUS, ticket_id, status)
    
    def update_task_status(self, task_id, status):
        return self.update_data(TABLE_TASKS, COL_TAS_STATUS, task_id, status)

    def update_ticket_department(self, ticket_id, department):
        return self.update_data(TABLE_TICKETS, COL_TIC_DEPARTMENT, ticket_id, department)

    def update_ticket_descrition(self, ticket_id, desc):
        desc = f"'{desc}'"
        return self.update_data(TABLE_TICKETS, COL_TIC_DESCRIPTION, ticket_id, desc)
    
    def update_filter(self, e_id, f_query):
        f_query = f"'{f_query}'"
        return self.update_data(TABLE_USER_FILTERS, COL_UF_FQ, e_id, f_query)
    
    def re_assign_ticket(self, ticket_id, emp_id):
        return self.update_data(TABLE_TICKETS, COL_TIC_ASSIGNED_TO, ticket_id, emp_id)
    
    def close_ticket(self, ticket_id):
        c_date = f"'{utils.get_current_date_string()}'"
        self.update_data(TABLE_TICKETS, COL_TIC_CLOSE_DATE, ticket_id, c_date)
        return self.update_ticket_status(ticket_id, STATUS_COMPLETE)
    
    def close_task(self, task_id):
        return self.update_task_status(task_id, STATUS_COMPLETE)
    
    def re_open_task(self, task_id):
        return self.update_task_status(task_id, STATUS_OPEN)

    def delete_task(self, task_id):
        condition = f"{COL_TAS_ID} = {task_id}"
        return self.delete_data(TABLE_TASKS, condition)
    

def create_db_connector()->DBEndpoint:
    connector = DBEndpoint(DB_HOST, DB_USER_NAME, DB_PASSWORD, DATABASE_NAME)
    connector.connect()
    return connector;

