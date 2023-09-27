import mysql.connector



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
            s = columns
            cols = s
            pc_holder = "%s"
        else:
            s = columns
            cols = s
            pc_holder = "%s"
        

        print(f"INSERT INTO {table} {cols} VALUES {pc_holder}")
        cursor = self.connection.cursor()
        try:
            for item in data:
                cursor.execute(f"INSERT INTO {table} ({cols}) VALUES ({pc_holder})", item)
            self.connection.commit()
            print("Data inserted successfully")
        except mysql.connector.Error as err:
            self.connection.rollback()
            print("Error: {}".format(err))
            return "Error: {}".format(err) , -1
            
        finally:
            cursor.close() 

class DBEndpoint(DatabaseConnector):
    def __init__(self, host, user, password, database):
        super().__init__(host, user, password, database)

    def insert_employees(self, employees:list):
        if type(employees) is tuple:
            employees = [employees]
        return self.insert_data("employees", ('name','email', 'department', 'position'), employees)

    def insert_tickets(self, tickets:list|tuple):
        if type(tickets) is tuple:
            tickets = [tickets]
        return self.insert_data("tickets", ('assigned_to', 'status', 'start_date', 'close_date', 'department', 'description'), tickets)

    def insert_tasks(self, tasks:list|tuple):
        if type(tasks) is tuple:
            tasks = [tasks]
        return self.insert_data("tasks", ('description', 'ticket_id', 'status', 'assigned_to', 'assigned_date'), tasks)

    def insert_department(self, departments:list|tuple):
        if type(departments) is tuple:
            departments = [departments]
        return self.insert_data("department", 'name', departments)

# Example usage
if __name__ == "__main__":
    # Replace with your own database credentials
    db = DBEndpoint(host='localhost', user='root', password='seb4vision23', database='live_ticketing_db')
    db.connect()

    # # Example query
    create_table_query = """
    INSERT INTO 
        live_ticketing_db.employees (name, email, department, position) 
    VALUES
        (%s, %s , %s, %s)
    """

    values = [("Sipho Mancam", "siphom@seb4vision.co.za", 2, "Software Developer"), 
              ("Sipho Mancam", "sipho2m@seb4vision.co.za", 2, "Software Developer"),
              ("Sipho Mancam", "siphom3@seb4vision.co.za", 2, "Software Developer"),
              ("Sipho Mancam", "siphom4@seb4vision.co.za", 2, "Software Developer")]

    departments = [tuple("R & D"), tuple("VR"), tuple("AR"), tuple("Production"), tuple("HR"), tuple("Graphics")]

    cursor = db.insert_department(departments)

    # Close the connection when done
    db.close_connection()