from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from lt_db_ops import db_connector, utils, parse2JSON


# Create your views here.

def default_view(request:HttpRequest)->HttpResponse:
    connector = db_connector.create_db_connector()
    tickets = connector.read_tickets()
    tickets = parse2JSON.parse_tickets(tickets)
    connector.close_connection()
    return render(request, 'defaultView.html', {'tickets':tickets}) #render(request, 'defaultView.html', {})


def create_ticket(request:HttpRequest)->HttpResponse:
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'create_ticket_form.html', {})
        else:
            return default_view(request)
    if request.method == 'POST':
        dept_name = request.POST['dept_name']
        ticket_descr = request.POST['ticket_description']
        connector = db_connector.create_db_connector()

        connector.close_connection()
        return HttpResponse("We received a form submit request")
    

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