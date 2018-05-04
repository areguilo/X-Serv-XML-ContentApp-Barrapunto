from django.shortcuts import render
from django.http import HttpResponse
from .models import Pages

from django.views.decorators.csrf import csrf_exempt
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
from urllib.request import urlopen
from .xml-parser-barrapunto import myContentHandler

# Create your views here.
def mainPage(request):
    list = Pages.objects.all()
    response = '<ul><h2>'
    for item in list:
        print(item.name)
        response = response + '<li><a href=http://localhost:8000/' + str(item.name) + ">" + item.name + '</a></li>'
    response = response + '</ul></h2>'
    response = "<h1>Hi!, these are our contents managed:</h1>" + response
    return HttpResponse(response)

def contentPage(request, identifier):
    if request.method == "GET":
        try:
            object = Pages.objects.get(name = identifier)
            response = object.page + '<br><br><a href=http://localhost:8000/> Return to Main menu </a>'
            return HttpResponse(response)
        except Pages.DoesNotExist:
            return HttpResponse("There are not pages for this object")
    else:
        page = Pages(name = identifier, page = request.body)
        page.save()
        return HttpResponse( page.name + "created")
