from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from lt_db_ops import db_connector, utils, parse2JSON, constants

from pprint import pprint

# Create your views here.

def default_view(request:HttpRequest)->HttpResponse:
    if request.user.is_authenticated:
        context = {}
        connector = db_connector.create_db_connector()
        tickets = connector.read_tickets()
        tickets = parse2JSON.parse_tickets(tickets)
        user = request.user
        if user.email is not None:
            employee = connector.read_employee_from_email(user.email)
        context['is_employee'] = len(employee) > 0
        context['tickets'] = tickets
        connector.close_connection()
        return render(request, 'defaultView.html', context) #render(request, 'defaultView.html', {})
    else:
      return render(request, 'not_signed_in.html', {})  


def create_ticket(request:HttpRequest)->HttpResponse:
    if request.user.is_authenticated:
        if request.method == 'GET':
            context = {}
            connector = db_connector.create_db_connector()
            departments = connector.read_departments()
            context['departments'] = departments
            connector.close_connection()
            return render(request, 'create_ticket_form.html', context)
            
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

    return render(request, 'not_signed_in.html', {})
    

def view_ticket(request:HttpRequest, id:int):

    if not request.user.is_authenticated:
        return render(request, 'not_signed_in.html', {})

    if request.method == 'GET':
        connector = db_connector.create_db_connector()
        res = connector.read_one_ticket(id)
        context = {}
        employee  = []
        user = request.user
        if user.email is not None:
            employee = connector.read_employee_from_email(user.email)
        context['is_employee'] = len(employee) > 0
 
        if len(res) != 0:
            ticket = parse2JSON.create_ticket_json(res[0])
            context['ticket_info'] = ticket
            if context['is_employee']:
                emp = employee[0]
                context['can_create_task'] = (emp[constants.COL_EMP_EMAIL] == ticket[constants.COL_TIC_ASSIGNED_TO])
                context['can_close_ticket'] = (emp[constants.COL_EMP_EMAIL] == ticket[constants.COL_TIC_ASSIGNED_TO] or emp[constants.COL_EMP_EMAIL] == ticket[constants.COL_TIC_OWNER])
                dep = ticket[constants.COL_TIC_DEPARTMENT]
                d_p = connector.read_department_by_name(dep)

                if type(d_p) is list and len(d_p) > 0:
                    manager = d_p[0][constants.COL_DEP_MANAGER]
                    mg = connector.read_one_employee(manager)
                    if len(mg) > 0:
                        context['is_manager'] = (emp[constants.COL_EMP_EMAIL] == mg[0][constants.COL_EMP_EMAIL]) 
                    
                    if context['is_manager']:
                        department_id = d_p[0][constants.COL_DEP_ID]
                        employees = connector.read_data(constants.TABLE_EMPLOYEES, ("*", ), f"{constants.COL_EMP_DEPT} = {department_id}")
                        context['employees'] = employees
            connector.close_connection()
            return render(request, 'view_ticket.html', context)
        
        return render(request, 'view_ticket.html', {})

def re_assign_ticket(request:HttpRequest):
    if request.method == 'POST':
        f_data = request.POST
        assign_to = f_data['assign_to']
        ticket_id = f_data['ticket_id']
        connector = db_connector.create_db_connector()
        connector.re_assign_ticket(ticket_id, assign_to)
        connector.close_connection()
    r_url = request.headers['Referer']
    return redirect(r_url)


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

def delete_task(request:HttpRequest, task_id:int):
    r_url = request.headers['Referer']
    connector = db_connector.create_db_connector()
    connector.delete_task(task_id)
    connector.close_connection()

    return redirect(r_url)

def close_ticket(request:HttpRequest, id:int):
    pass

def create_task(request:HttpRequest):
    f_data = request.POST
    assigned_to = f_data['assign_to']
    ticket_id = f_data['ticket_id']
    task_description = f_data['task_description']
    
    if assigned_to is not None and ticket_id is not None and task_description is not None:
        connector = db_connector.create_db_connector()
        connector.create_task(ticket_id, assigned_to, task_description)
        connector.close_connection()

    return render(request, 'response.html', {})

def create_task_form(request:HttpRequest, ticket_id:int):
    connector = db_connector.create_db_connector()
    context = {}
    ticket = connector.read_one_ticket(ticket_id)
    if len(ticket) > 0:
        department_id = ticket[0]['department']
        employees = connector.read_data(constants.TABLE_EMPLOYEES, ("*", ), f"{constants.COL_EMP_DEPT} = {department_id}")
        context['ticket_id'] = ticket_id
        context['employees'] = employees
    connector.close_connection()
    return render(request, 'create_task_form.html', {'ticket_info':context})

