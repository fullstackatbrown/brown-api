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
    _this_room_url = _room_url + room_id + "&rdm=" + str(int(timestamp))
    machines = requests.get(_this_room_url, verify="false").json()['objects']
    machine_list = []
    for machine in machines:
        # Some "ghost" machines exist without an appliance_desc, or with an empty one
        try:
            if not machine['appliance_desc']:
                continue
        except KeyError:
            continue

        if (machine['type'] == 'washFL' or
            machine['type'] == 'dry'):
            new_machine = {
                            "id": int(machine['appliance_desc_key']),
                            "room_id": int(room_id),
                            "machine_no": int(machine['appliance_desc']),
                            "type": 'wash' if machine['type'] == 'washFL' else 'dry',
                            "avail": machine['time_left_lite'] == 'Available',
                            "ext_cycle": machine['time_left_lite'] == 'Ext. Cycle',
                            "offline": machine['time_left_lite'] in ['Offline', 'Out of service'],
                            "time_remaining": machine['time_remaining'],
                            "average_run_time": machine['average_run_time']
                          }
            machine_list.append(new_machine)
        elif (machine['type'] == 'washNdry' or
              machine['type'] == 'dblDry'):
            # For washNdry, new_machine1 should be a dryer while new_machine2 should be a washer
            new_machine1 = {
                             "id": int(machine['appliance_desc_key']),
                             "room_id": int(room_id),
                             "machine_no": int(machine['appliance_desc']),
                             "type": 'dry',
                             "avail": machine['time_left_lite'] == 'Available',
                             "ext_cycle": machine['time_left_lite'] == 'Ext. Cycle',
                             "offline": machine['time_left_lite'] in ['Offline', 'Out of service'],
                             "time_remaining": machine['time_remaining'],
                             "average_run_time": machine['average_run_time']
                           }
            new_machine2 = {
                             "id": int(machine['appliance_desc_key2']),
                             "room_id": int(room_id),
                             "machine_no": int(machine['appliance_desc2']),
                             "type": 'wash' if machine['type'] == 'washNdry' else 'dry',
                             "avail": machine['time_left_lite2'] == 'Available',
                             "ext_cycle": machine['time_left_lite2'] == 'Ext. Cycle',
                             "offline": machine['time_left_lite2'] in ['Offline', 'Out of service'],
                             "time_remaining": machine['time_remaining2'],
                             "average_run_time": machine['average_run_time2']
                           }
            machine_list.append(new_machine1)
            machine_list.append(new_machine2)

    return machine_list
