import mysql.connector
from constants import *
import datetime
import time
import utils

class DatabaseConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except mysql.connector.Error as err:
            print("Error: {}".format(err))

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Connection to MySQL database closed")

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
            cursor.close()

    def read_data(self, table:str, columns:tuple|str, condition:str):
        res = []
        if type(columns) is tuple:
            columns = " ,".join(columns)
        
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"SELECT {columns} FROM {table} WHERE {condition}")
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
        

class DBEndpoint(DatabaseConnector):
    def __init__(self, host, user, password, database):
        super().__init__(host, user, password, database)

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
                                (COL_TIC_ASSIGNED_TO, COL_TIC_STATUS, COL_TIC_START_DATE, COL_TIC_CLOSE_DATE, COL_TIC_DEPARTMENT, COL_TIC_DESCRIPTION), 
                                tickets)

    def insert_tasks(self, tasks:list|tuple):
        tasks = self._make_list(tasks)

        return self.insert_data(TABLE_TASKS, 
                                (COL_TAS_DESCRIPTION, COL_TAS_TICKET_ID, COL_TAS_STATUS, COL_TAS_ASSIGNED_TO, COL_TAS_ASSIGNED_DATE), 
                                tasks)

    def insert_department(self, departments:list|tuple):
        if type(departments) is tuple:
            departments = [departments]
        return self.insert_data(TABLE_DEPARTMENTS, (COL_DEP_NAME), departments)
    

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
    
    def read_tasks(self, ticket_id)->list[tuple]:
        condition = f"{COL_TAS_TICKET_ID} = {ticket_id}"
        return self.read_data(TABLE_TASKS, ("*", ), condition)
    
    def read_tickets(self, cols = ("*",),  condition = None)->list[tuple]:
        if condition is None:
            condition = f"{COL_TIC_ID} > 0" # this will return all tickets
        return self.read_data(TABLE_TICKETS, cols, condition)
    
    def read_one_ticket(self, ticket_id)->list[tuple]:
        condition = f"{COL_TIC_ID} = {ticket_id}"
        return self.read_tickets(condition=condition)
    
    def update_ticket_status(self, ticket_id, status):
        return self.update_data(TABLE_TICKETS, COL_TIC_STATUS, ticket_id, status)

    def update_ticket_department(self, ticket_id, department):
        return self.update_data(TABLE_TICKETS, COL_TIC_DEPARTMENT, ticket_id, department)

    def update_ticket_descrition(self, ticket_id, desc):
        desc = f"'{desc}'"
        return self.update_data(TABLE_TICKETS, COL_TIC_DESCRIPTION, ticket_id, desc)
    
    def close_ticket(self, ticket_id):
        c_date = f"'{utils.get_current_date_string()}'"
        self.update_data(TABLE_TICKETS, COL_TIC_CLOSE_DATE, ticket_id, c_date)
        return self.update_ticket_status(ticket_id, STATUS_COMPLETE)


def create_db_connector()->DBEndpoint:
    connector = DBEndpoint(DB_HOST, DB_USER_NAME, DB_PASSWORD, DATABASE_NAME)
    connector.connect()
    return connector;


# Example usage
if __name__ == "__main__":
    # Replace with your own database credentials
    db = DBEndpoint(host=DB_HOST, user=DB_USER_NAME, password=DB_PASSWORD, database=DATABASE_NAME)
    db.connect()

    values = [("Sipho Mancam", "siphom@seb4vision.co.za", 2, "Software Developer"), 
              ("Sipho Mancam", "sipho2m@seb4vision.co.za", 2, "Software Developer"),
              ("Sipho Mancam", "siphom3@seb4vision.co.za", 2, "Software Developer"),
              ("Sipho Mancam", "siphom4@seb4vision.co.za", 2, "Software Developer")]
    

    tickets = (1, 1, '2023-09-28 10:04:03', '2023-09-28 10:04:23', 1, "Test the tuple")

    departments = [("R & D",), 
                   ("VR",), 
                   ("AR",), 
                   ("Production",), 
                   ("HR",), 
                   ("Graphics",)
                   ]
    
    tasks = [
        ("Please check the ticker on VR3 it's not working", 8, STATUS_OPEN, 1, "2023-09-28 10:04:03"),
        ("Please check the ticker on VR3 it's not working", 8, STATUS_OPEN, 1, "2023-09-28 10:04:03"),
        ("Please check the ticker on VR3 it's not working", 8, STATUS_OPEN, 1, "2023-09-28 10:04:03"),
        ("Please check the ticker on VR3 it's not working", 9, STATUS_OPEN, 1, "2023-09-28 10:04:03"),
    ]


    db.insert_tasks(tasks)

    cursor = db.close_ticket(8)

    print(cursor)

    # Close the connection when done
    db.close_connection()