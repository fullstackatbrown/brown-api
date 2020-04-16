# vim: set ts=4 sts=4 sw=4 expandtab:
# from datetime import date, timedelta
# import time
# import argparse

from api import con
import os
import api.scripts.laundry.Campus as Campus
from api.scripts.util.logger import log


def main():
    with con.cursor() as cur:
        for room in Campus.scrape_rooms():
            query = {'name': room['name'], 'id': room['id']}
            log("found room {0} with {1} machine(s)".format(room['name'], len(room['machines'])))
            try:
                cur.execute("INSERT INTO laundry_rooms (id, name) VALUES (%s, %s)", (room['id'], room['name']))
            except:
                pass
            for machine in room['machines']:
                if (machine['type'] == "washFL" or
                    machine['type'] == "dblDry" or
                    machine['type'] == "washNdry" or
                    machine['type'] == "dry"):
                    try:
                        cur.execute("INSERT INTO laundry_machines (id, room_id, type) VALUES (%s, %s, %s)",
                                        (machine['appliance_desc_key'], room['id'], machine['type']))
                    except:
                        pass

if __name__ == "__main__":
    main()
