# vim: set ts=4 sts=4 sw=4 expandtab:
import requests
import datetime
from bs4 import BeautifulSoup as soup
import sqlite3
import os
from api.scripts.laundry import Room, util

_campus_url = "http://www.laundryview.com/api/c_room?loc=1921&rdm="


def scrape_rooms():
    timestamp = datetime.datetime.utcnow().timestamp()

    ''' collection is a pymongo collection object '''
    _this_campus_url = _campus_url + str(int(timestamp))

    rooms = requests.get(_this_campus_url, verify="false").json()['room_data']
    for room in rooms:
        rid = room['laundry_room_location']
        name = room['laundry_room_name']
        room = {'name': name, 'id': rid}
        room = Room.scrape_machines(room)
        yield room
