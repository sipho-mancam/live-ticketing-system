from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from lt_db_ops import db_connector, utils, parse2JSON

# Create your views here.

def default_view(request:HttpRequest)->HttpResponse:
    connector = db_connector.create_db_connector()
    tickets = connector.read_tickets()
    tickets = parse2JSON.parse_tickets(tickets)
    print(tickets)
    return HttpResponse(tickets) #render(request, 'defaultView.html', {})