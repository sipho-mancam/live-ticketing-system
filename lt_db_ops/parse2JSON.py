from .constants import *
from .db_connector import create_db_connector, DBEndpoint
from pprint import pprint
import json
import datetime

def ticket_time_date(ticket)->dict:
    s_date = ticket[COL_TIC_START_DATE]
    ticket[COL_TIC_START_DATE] = s_date.__str__()
    ticket[COL_TIC_CLOSE_DATE] = ticket[COL_TIC_CLOSE_DATE].__str__()
    return ticket

def tasks_time_parse(tasks:list[dict])->list[dict]:
    res = []
    for task in tasks:
        task[COL_TAS_ASSIGNED_DATE] = task[COL_TAS_ASSIGNED_DATE].__str__()
        res.append(task)
    return res

def create_ticket_json(ticket: dict)->dict: # this will fetch all 
    ticket_id = ticket[COL_TIC_ID]
    ticket = ticket_time_date(ticket)

    db_connector = create_db_connector()
    tasks = db_connector.read_tasks(ticket_id)
    tasks = tasks_time_parse(tasks)
    ticket[TASKS] = tasks
    db_connector.close_connection()

    return ticket

def parse_tickets(tickets:list[dict])->list[dict]:
    res = []
    for ticket in tickets:
        ticket = create_ticket_json(ticket)
        res.append(ticket)
    return res

