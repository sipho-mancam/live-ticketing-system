import mysql.connector
from constants import *


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
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"SELECT {columns} FROM {table} WHERE {condition}")
            for item in cursor:
                res.append(item)
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
        
    def update_data(self, table:str, data:list[tuple]): # (column, id, value)
        tables_id_cols = DB_TABLE_PKS
        data  = self._make_list(data)

        cursor = self.connection.cursor()
        try:
            for col, val, id in data:
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

    cursor = db.insert_tickets(tickets)

    print(cursor)

    # Close the connection when done
    db.close_connection()