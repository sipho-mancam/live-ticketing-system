from constants import *
from db_connector import *
from parse2JSON import *
from utils import *

connector = create_db_connector()

def insert_dummy_employees():

    d_employees = [
        ("Sipho Mancam", "siphom@seb4vision.co.za", 1, "Software Developer"),
        ("Koketso Something", "koketsom@seb4vision.co.za", 2, "Hadware Developer"),
        ("Sbonelo Khuzwayo", "sbonelo@seb4vision.co.za", 3, "VR Developer"),
        ("Sabelo Khuzwayo", "sabelo@seb4vision.co.za", 4, "AR"),
        ("Prince Mtshakatshaka", "princem@seb4vision.co.za", 5, "Graphic Designer"),
        ("Hlatshwayo Khuzwayo", "hs@seb4vision.co.za", 6, "operator"),
        ("Siya Mentoor", "siyam@seb4vision.co.za", 7, "Hardware Staff")
    ]

    connector.insert_employees(d_employees)


insert_dummy_employees()


def insert_dummy_departments():
    departments = [
        ("R & D (Software Development)", 1),
        ("VR ", 2),
        ("AR", 1),
        ("Operations", 1),
        ("HR", 1),
        ("Graphics Design", 1),
        ("Hardware", 1)
    ]
    connector.insert_department(departments)

def insert_dummy_tickets():
    pass

def attact_x_tasks_to_tickets(ticket_ids:int):
    pass