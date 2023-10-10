from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from lt_db_ops import db_connector, utils, parse2JSON, constants
from .emails import start_mail_runner
import threading
#from pprint import pprint

# Create your views here.

# start the emailing service
mail_thread = threading.Thread(target=start_mail_runner)
mail_thread.start()


def default_view(request:HttpRequest)->HttpResponse:
    #Define the subject, HTML template, context, and recipients
    # subject = 'Test Mailing Service'
    # html_template = 'emails/task_assigned.html'
    # context = {'name': 'No Reply'}
    # to_emails = ['siphom@seb4vision.co.za']
    # send_html_email(subject, html_template, context, to_emails
   
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
            owner = connector.read_employee_from_email(request.user.email)
            owner_id = owner[0][constants.COL_EMP_ID]
            ticket_id = connector.create_ticket(dept_manager, dept_id, ticket_descr, owner_id).lastrowid

            #Email record this will schedule an email to be sent to the department manager
            subject = constants.SUBJECT_TICKET_ASSIGNED
            template_id = connector.get_template_id(constants.TEMPLATE_TICKET_ASSIGNED)
            recipient = dept_manager
            ticket = ticket_id
            status = constants.EMAIL_RECORD_STATUS_PENDING
            actuator = request.user.email
            connector.append_mail_record(subject, template_id, recipient, ticket, status, actuator).lastrowid

            # Ticket was created, we need to log an event for this
            action_id = connector.get_action_id(constants.ACTION_CREATED)
            object_id = connector.get_object_id(constants.OBJECT_TICKET)
            employee_d = owner_id
            connector.add_event(ticket_id, object_id, action_id, employee_d)
            connector.close_connection()

            return default_view(request)

    return render(request, 'not_signed_in.html', {})
    

def view_ticket(request:HttpRequest, id:int):

    if not request.user.is_authenticated:
        return render(request, 'not_signed_in.html', {})

    if request.method == 'GET':
        connector = db_connector.create_db_connector()
        res = connector.read_one_ticket(id)
        events = connector.read_event_data(id)
        print(events)
        context = {}
        employee  = []
        user = request.user
        if user.email is not None:
            employee = connector.read_employee_from_email(user.email)
        context['is_employee'] = len(employee) > 0
        context['events'] = events
 
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

        #Email record this will schedule an email to be sent to the department manager
        subject = constants.SUBJECT_TICKET_ASSIGNED
        template_id = connector.get_template_id(constants.TEMPLATE_TASK_ASSIGNED)
        recipient = assign_to
        ticket = ticket_id
        status = constants.EMAIL_RECORD_STATUS_PENDING
        actuator = request.user.email
        connector.append_mail_record(subject, template_id, recipient, ticket, status, actuator)


        # Tick was reassigned --> let's add an event for it.
        action_id = connector.get_action_id(constants.ACTION_ASSIGNED)
        object_id = connector.get_object_id(constants.OBJECT_TICKET)
        connector.add_event(ticket_id, object_id, action_id, assign_to)

        connector.close_connection()
    r_url = request.headers['Referer']
    return redirect(r_url)


def close_task(request:HttpRequest, id:int):
    task_id = id
    connector = db_connector.create_db_connector()
    connector.close_task(task_id);  

    #event 
    task = connector.read_one_task(task_id)
    ticket_id = task[0][constants.COL_TAS_TICKET_ID]
    employeeid = task[0][constants.COL_TAS_ASSIGNED_TO]
    object_id = connector.get_object_id(constants.OBJECT_TASK)
    action_id = connector.get_action_id(constants.ACTION_CLOSED)
    connector.add_event(ticket_id, object_id, action_id, employeeid)

    connector.close_connection()

    return redirect(request.headers['Referer'])

def re_open_task(request:HttpRequest, id:int):
    task_id = id
    connector = db_connector.create_db_connector()
    connector.re_open_task(task_id); 

    #event 
    task = connector.read_one_task(task_id)
    ticket_id = task[0][constants.COL_TAS_TICKET_ID]
    employeeid = task[0][constants.COL_TAS_ASSIGNED_TO]
    object_id = connector.get_object_id(constants.OBJECT_TASK)
    action_id = connector.get_action_id(constants.ACTION_OPENED)
    connector.add_event(ticket_id, object_id, action_id, employeeid)

    connector.close_connection()
    return redirect(request.headers['Referer'])

def delete_task(request:HttpRequest, task_id:int):
    r_url = request.headers['Referer']
    connector = db_connector.create_db_connector()

    #event 
    task = connector.read_one_task(task_id)
    ticket_id = task[0][constants.COL_TAS_TICKET_ID]
    employeeid = task[0][constants.COL_TAS_ASSIGNED_TO]
    object_id = connector.get_object_id(constants.OBJECT_TASK)
    action_id = connector.get_action_id(constants.ACTION_DELETED)
    connector.add_event(ticket_id, object_id, action_id, employeeid)
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

        #Email record this will schedule an email to be sent to the department manager
        subject = constants.SUBJECT_TASK_ASSIGNED
        template_id = connector.get_template_id(constants.TEMPLATE_TASK_ASSIGNED)
        recipient = assigned_to
        ticket = ticket_id
        status = constants.EMAIL_RECORD_STATUS_PENDING
        actuator = request.user.email
        connector.append_mail_record(subject, template_id, recipient, ticket, status, actuator)

        action_id = connector.get_action_id(constants.ACTION_ASSIGNED)
        object_id = connector.get_object_id(constants.OBJECT_TASK)
        connector.add_event(ticket_id, object_id, action_id, assigned_to)

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

