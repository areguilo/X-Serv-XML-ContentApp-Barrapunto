#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

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
                barrapunto.write("<h2><li>Title: " + self.theContent + "</li>" )
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                print(5)
                print (" Link: " + self.theContent + ".")
                barrapunto.write("<li><a href =" + self.theContent + ">" + str(self.theContent) + "</a></h2></li>")
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog
# Load parser and driver
barrapunto = open('barrapunto.html','w')

opening_lines = '<!DOCTYPE html>' + '\n' + '<html>' + '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />' + '\n'
opening_lines  += '<head>' + '\n' + '<title>/.Titulares</title>' + '\n' + '</head>' + '\n'
opening_lines +=  '<h1>Titulares de Barrapunto: </h1>' + '\n'
opening_lines += '<body>' + '\n'

barrapunto.write(opening_lines)


theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!

xmlFile = urllib.request.urlopen('http://barrapunto.com/index.rss')
theParser.parse(xmlFile)
barrapunto.write('\n'+ '</body>' + '\n' + '</html>'+ '\n')

print ("Parse complete")
