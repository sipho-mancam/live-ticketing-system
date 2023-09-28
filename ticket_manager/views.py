from django.shortcuts import render
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
        return render(request, 'create_ticket_form.html', {})
    if request.method == 'POST':
        dept_name = request.POST['dept_name']
        ticket_descr = request.POST['ticket_description']

        connector = db_connector.create_db_connector()

        connector.insert_tickets(())


        return HttpResponse("We received a form submit request")