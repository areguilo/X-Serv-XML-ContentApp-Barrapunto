from django.shortcuts import render
from django.http import HttpResponse
from .models import Pages

from django.views.decorators.csrf import csrf_exempt
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib.request

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        #self.Cont=1

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                #self.Cont=self.Cont+1
                barrapuntoHtml.write("<h2><li>Title: " + self.theContent + "</li>" )
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                print(5)
                print (" Link: " + self.theContent + ".")
                barrapuntoHtml.write("<li><a href =" + self.theContent + ">" + str(self.theContent) + "</a></h2></li>")
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

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


@csrf_exempt
def contentPage(request, identifier):
    if request.method == "GET":
        try:
            global barrapuntoHtml
            object = Pages.objects.get(name = identifier)

            theParser = make_parser()
            theHandler = myContentHandler()
            theParser.setContentHandler(theHandler)

            xmlFile = urllib.request.urlopen("http://barrapunto.com/index.rss")
            barrapuntoXml = open('barrapunto.rss', 'w')

            rss = xmlFile.read().decode("utf-8")
            barrapuntoXml.write(rss)
            barrapuntoXml.close()

            barrapuntoXml = open('barrapunto.rss', "r")
            barrapuntoHtml = open('barrapunto.html', 'w')

            theParser.parse(barrapuntoXml)
            barrapuntoHtml.write('\n'+ '</body>' + '\n' + '</html>'+ '\n')
            barrapuntoHtml.close()
            #barrapuntoXml.close()

            barrapuntoHtml = open('barrapunto.html', 'r')
            text = barrapuntoHtml.read()
            response = text + object.page
            return HttpResponse(response)
        except Pages.DoesNotExist:
            return HttpResponse("There are not pages for this object")
    else:
        page = Pages(name = identifier, page = request.body)
        page.save()
        return HttpResponse( page.name + "created")
