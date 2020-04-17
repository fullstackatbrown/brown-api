# vim: set ts=4 sts=4 sw=4 expandtab:
import re
import datetime
import requests
from api.scripts.laundry import util
import os

_room_url = "http://www.laundryview.com/api/currentRoomData?school_desc_key=1921&location="
_machine_id_re = re.compile(r'machine(Status|Data)([0-9]+)')


def to_str(room):
    return room['name'] + ' (' + room['id'] + ')'


def scrape_machines(room):
    timestamp = datetime.datetime.utcnow().timestamp()
    _this_room_url = _room_url + room['id'] + "&rdm=" + str(int(timestamp))
    machines = requests.get(_this_room_url, verify="false").json()['objects']
    room['machines'] = list(machines)
    return room


def get_machine_statuses(room_id):
    timestamp = datetime.datetime.utcnow().timestamp()
    _this_room_url = _room_url+ room_id + "&rdm=" + str(int(timestamp))
    machines = requests.get(_this_room_url, verify="false").json()['objects']
    machine_list = []
    for machine in machines:
        if (machine['type'] == "washFL" or
            machine['type'] == "washNdry" or
            machine['type'] == "dry"):
            new_machine = {
                            "id": int(machine['appliance_desc_key']),
                            "room_id": int(room_id),
                            "type": machine['type'],
                            "avail": machine['time_left_lite'] is 'Avaliable',
                            "time_remaining": machine['time_remaining'],
                            "average_run_time": machine['average_run_time']
                          }
            machine_list.append(new_machine)
        elif (machine['type'] == "dblDry"):
            new_machine = {
                            "id": machine['appliance_desc_key'],
                            "room_id": room_id,
                            "type": machine['type'],
                            "avail1": machine['time_left_lite'] is 'Avaliable',
                            "time_remaining1": machine['time_remaining'],
                            "average_run_time1": machine['average_run_time'],
                            "avail2": machine['time_left_lite2'] is 'Avaliable',
                            "time_remaining2": machine['time_remaining2'],
                            "average_run_time2": machine['average_run_time2']
                          }
            machine_list.append(new_machine)
    return machine_list
