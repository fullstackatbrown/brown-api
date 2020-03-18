# vim: set ts=4 sts=4 sw=4 expandtab:
from bs4 import BeautifulSoup as soup
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from api.scripts.laundry import Room, util

#https://www.laundryview.com/api/c_room?loc=1921&rdm=1584493236500

_brown_campus_id = "selectProperty?property=1921"
_campus_url = "http://laundryview.com/{0}".format(_brown_campus_id)

def scrape_rooms():
    ''' collection is a pymongo collection object '''
    # html = util.get_html(_campus_url)
    browser = webdriver.PhantomJS()
    browser.get(url)
    html = browser.page_source
    print(_campus_url)
    parsed = soup(html, 'html5lib')
    links = parsed.find('div', {'ng-click': 'ctrl.goToRoom(room)'})
    print(html)
    print(links)
    for link in links:
        rid = hash(link)
        name = link.text.strip()
        room = {'name': name, 'id': rid}
        with sqlite3.connect(os.environ['DB_LOCATION']) as con:
            c = con.execute("SELECT * FROM laundry_rooms WHERE name=:name AND ", {"key": client_id})
            existing_room = c.fetchone()
        existing_room = collection.find(room)

        if not existing_room == None:
            room = Room.scrape_machines(room)
        else:
            room['machines'] = existing_room[0]['machines']
        yield room
