# vim: set ts=4 sts=4 sw=4 expandtab:
# from datetime import date, timedelta
# import time
# import argparse

import sqlite3
import os
import api.scripts.laundry.Campus as Campus
from api.scripts.util.logger import log


def main():
    with sqlite3.connect(os.environ['DB_LOCATION']) as con:
        for room in Campus.scrape_rooms():
            query = {'name': room['name'], 'id': room['id']}
            log("found room {0} with {1} machine(s)".format(room['name'], len(room['machines'])))
            con.execute("INSERT OR REPLACE INTO laundry_rooms (id, name) VALUES (?, ?)", (room['id'], room['name']))
            for machine in room['machines']:
                if (machine['type'] == "washFL" or
                    machine['type'] == "dblDry" or
                    machine['type'] == "washNdry" or
                    machine['type'] == "dry"):
                    con.execute("INSERT OR REPLACE INTO laundry_machines (id, room_id, type) VALUES (?, ?, ?)",
                                    (machine['appliance_desc_key'], room['id'], machine['type']))

if __name__ == "__main__":
    main()
