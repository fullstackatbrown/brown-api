# vim: set ts=4 sts=4 sw=4 expandtab:
# from datetime import date, timedelta
# import time
# import argparse

import api.scripts.laundry.Campus as Campus
from api.scripts.util.logger import log


def main():
    for room in Campus.scrape_rooms():
        query = {'name': room['name'], 'id': room['id']}
        log("found room {0} with {1} machine(s)".format(
            room['name'], len(room['machines'])))
        # ldb.replace_one(query, room, upsert=True)

if __name__ == "__main__":
    main()
