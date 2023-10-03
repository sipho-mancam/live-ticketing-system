from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from lt_db_ops import db_connector, utils, parse2JSON, constants

from pprint import pprint

# Create your views here.

def default_view(request:HttpRequest)->HttpResponse:
    connector = db_connector.create_db_connector()
    tickets = connector.read_tickets()
    tickets = parse2JSON.parse_tickets(tickets)
    connector.close_connection()
    return render(request, 'defaultView.html', {'tickets':tickets}) #render(request, 'defaultView.html', {})


def create_ticket(request:HttpRequest)->HttpResponse:
    if request.user.is_authenticated:
        if request.method == 'GET':
            if request.user.is_authenticated:
                context = {}
                connector = db_connector.create_db_connector()
                departments = connector.read_departments()
                context['departments'] = departments
                connector.close_connection()
                return render(request, 'create_ticket_form.html', context)
            else:
                return default_view(request)
        if request.method == 'POST':
            # this is where the ticket is created from the user
            
                dept_id = request.POST['dept_id']
                ticket_descr = request.POST['ticket_description']
                connector = db_connector.create_db_connector()
                dept = connector.read_one_department(dept_id)
                dept_manager = dept[0][constants.COL_DEP_MANAGER]
                print(request.user.email)
                owner = connector.read_employee_from_email(request.user.email)
                owner_id = owner[0][constants.COL_EMP_ID]
                connector.create_ticket(dept_manager, dept_id, ticket_descr, owner_id)
                connector.close_connection()

                return default_view(request)

    return HttpResponse("Please login to access the service you are requesting")
    

def view_ticket(request:HttpRequest, id:int):

    if request.method == 'GET':
        connector = db_connector.create_db_connector()
        res = connector.read_one_ticket(id)
        
        if len(res) != 0:
            ticket = parse2JSON.create_ticket_json(res[0])
            return render(request, 'view_ticket.html', {'ticket_info':ticket})
        return render(request, 'view_ticket.html', {})
    else:
        print("This is a post request")
    
    return HttpResponse(f"Viewing TIcket: {id}")

def close_task(request:HttpRequest, id:int):
    task_id = id
    connector = db_connector.create_db_connector()
    connector.close_task(task_id);  
    return redirect(request.headers['Referer'])

def re_open_task(request:HttpRequest, id:int):
    task_id = id
    connector = db_connector.create_db_connector()
    connector.re_open_task(task_id);  
    return redirect(request.headers['Referer'])

def close_ticket(request:HttpRequest, id:int):
    pass

def create_task(request:HttpRequest):
    f_data = request.POST
    assigned_to = f_data['assign_to']
    ticket_id = f_data['ticket_id']
    task_description = f_data['task_description']
    r_url = request.headers['Referer'];
    connector = db_connector.create_db_connector()
    connector.create_task(ticket_id, assigned_to, task_description)
    connector.close_connection()
    return redirect(r_url)

def create_task_form(request:HttpRequest, ticket_id:int):
    connector = db_connector.create_db_connector()
    context = {}
    ticket = connector.read_one_ticket(ticket_id)
    department_id = ticket[0]['department']
    employees = connector.read_data(constants.TABLE_EMPLOYEES, ("*", ), f"{constants.COL_EMP_DEPT} = {department_id}")
    context['ticket_id'] = ticket_id
    context['employees'] = employees
    connector.close_connection()
    return render(request, 'create_task_form.html', {'ticket_info':context})

