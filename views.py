import urllib
import re
from icalendar import Calendar, Event, UTC
from datetime import datetime, timedelta, date
from xml.dom import minidom

from django.http import *
from django.shortcuts import *
from django.template import loader, Context

BASE_WEATHER_URL = 'http://weather.yahooapis.com/forecastrss?p=%s' 
WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'

# yahoo condition codes, converted to unicode symbols
CONDITION_CODES = {
'0':u'\u2608',
'1':u'\u2608',
'2':u'\u2608',
'3':u'\u2608',
'4':u'\u2608',
'5':u'\u2614',
'6':u'\u2614',
'7':u'\u2603',
'8':u'\u2614',
'9':u'\u2602',
'10':u'\u2614',
'11':u'\u2614',
'12':u'\u2614',
'13':u'\u2603',
'14':u'\u2603',
'15':u'\u2603',
'16':u'\u2603',
'17':u'\u2614',
'18':u'\u2614',
'19':u'\u2600',
'20':u'\u2600',
'21':u'\u2600',
'22':u'\u2600',
'23':u'\u263C',
'24':u'\u263C',
'25':u'\u2603',
'26':u'\u2601',
'27':u'\u2601',
'28':u'\u2601',
'29':u'\u263C',
'30':u'\u263C',
'31':u'\u2600',
'32':u'\u2600',
'33':u'\u2600',
'34':u'\u2600',
'35':u'\u2614',
'36':u'\u2600',
'37':u'\u2608',
'38':u'\u2608',
'39':u'\u2608',
'40':u'\u2602',
'41':u'\u2603',
'42':u'\u2603',
'43':u'\u2603',
'44':u'\u263C',
'45':u'\u2608',
'46':u'\u2603',
'47':u'\u2607',
'3200':u'\u26A0', }

# for versions of python earlier than 2.61, we need this
MONTHS_TO_NUM = {'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5, 'JUN':6,
                 'JUL':7, 'AUG':8, 'SEP':9, 'OCT':10,'NOV':11,'DEC':12,}


def for_zip(request, location):
    url = BASE_WEATHER_URL % location
    dom = minidom.parse(urllib.urlopen(url))
    forecasts = []

    link = dom.getElementsByTagName('link')
    url = link[0].childNodes[0].data


    for node in dom.getElementsByTagNameNS(WEATHER_NS, 'forecast'):
        forecasts.append({
            'date': node.getAttribute('date'),
            'low': node.getAttribute('low'),
            'high': node.getAttribute('high'),
            'condition_code': node.getAttribute('code'),
            'condition': node.getAttribute('text')
        })

    cal = Calendar()
    cal.add('prodid', '-//django-weathercal//camronflanders.com//')
    cal.add('version', '2.0')

    for forecast in forecasts:
        parsed_date = re.search("(\d{2})\s(\w{3})\s(\d{4})", forecast['date'])

        day = int(parsed_date.group(1))
        month = int(MONTHS_TO_NUM['%s' % parsed_date.group(2).upper()])
        year = int(parsed_date.group(3))

        startdate = date(year, month, day)
        enddate = date(year, month, day) + timedelta(1)

        e = Event()
        e.add('summary', u'%s %s, %s\u00B0/%s\u00B0' % (CONDITION_CODES[forecast['condition_code']], forecast['condition'], forecast['high'], forecast['low']))
        e.add('dtstart', startdate)
        e.add('dtend', enddate)
        e.add('dtstamp', datetime.now())
        e.add('url', url)

        cal.add_component(e)

    response = HttpResponse(mimetype="text/calendar")
    response.write(cal.as_string())
    return response
