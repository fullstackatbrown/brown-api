from sys import argv
from sys import exit
import time
import sqlite3
import os

from api.scripts.eateries import Eatery
from api.scripts.email_handler import send_alert_email

# as you add eateries, simply instantiate their class in this list for them to be scraped.

def scrape(eateries, get_menus=True, get_hours=True, alert=True):
    total_menus, total_hours, total_time = 0, 0, 0
    for eatery in eateries:
        print()
        print("Scraping data for:", eatery.name)
        start = time.time()
        try:
            num_menus, num_hours = eatery.scrape()
        except:
            import traceback
            traceback.print_exc()
            print("Could not scrape data for", eatery.name)
            if alert:
                send_alert_email("Could not scrape data for " + eatery.name, urgent=False)
            continue
        elapsed = time.time() - start
        print(num_menus, "menus and", num_hours, "hours scraped for", eatery.name, "in", str(elapsed), "seconds.")
        total_menus += num_menus
        total_hours += num_hours
        total_time += elapsed
    print()
    print(total_menus, "total menus and", total_hours, "total hours scraped in", total_time, "seconds.")


def main():
    get_menus, get_hours, alert = False, False, True
    eateries = []
    if len(argv) > 1:
        for arg in argv:
            if arg == '--silent' or arg == '-s':
                alert = False
            if arg == '--hours' or arg == '-h':
                get_hours = True
            if arg == '--menus' or arg == '-m':
                get_menus = True
            if arg == '--ratty' or arg == '-r':
                eateries.append(Ratty())
            if arg == '--vdub' or arg == '-v':
                eateries.append(VDub())
            if arg == '--help':
                print("Flags: [--silent --hours --menus --ratty --vdub]")
                exit()

    # if neither menus nor hours specified, scrape both
    if not get_menus and not get_hours:
        get_menus, get_hours = True, True

    # if no eateries specified, scrape all eateries
    add_eateries = ['andrews-commons', 'sharpe-refectory']
    eateries = []
    with sqlite3.connect(os.environ['DB_LOCATION']) as con:
        # Add eateries to be added
        for eatery_name in add_eateries:
            con.execute("INSERT OR REPLACE INTO dining_halls (name) VALUES (?)", (eatery_name,))
        # Fetch the other eateries from the db
        c = con.execute("SELECT * FROM dining_halls")
        dining_halls = c.fetchall()
        for dining_hall in dining_halls:
            eateries.append(Eatery(dining_hall[0]))
    print("Scraping Brown Dining Services' sites for menus and hours...")
    scrape(eateries)
    print("Done scraping.")


if __name__ == '__main__':
    main()
