import requests
import sqlite3
import json
import os
import re
import time
import datetime
import hashlib
from urllib.parse import unquote
from bs4 import BeautifulSoup as soup
from datetime import date, timedelta

class Eatery:
    def __init__(self, name):
        self.name = name

    base_url = "https://dining.brown.edu/cafe/"

    def scrape(self):
        ''' This method is called on each eatery by 'scraper.py'
            Scrape menus and hours for this eatery and add them to database
            Return number of menus and hours scraped
        '''
        html = get_html(self.base_url + self.name)
        parsed = soup(html, 'html5lib')
        # file = open("tests/testing.htm", "r")
        # parsed = soup(file.read(), 'html5lib')
        # if get_hours:
        data = self.scrape_schedule(parsed)
        self.scrape_menus(parsed, data)
        self.update_db(data)
        return data

    def scrape_schedule(self, parsed):
        ''' Get weekly schedule and special information
        '''

        schedule = {'special': [], 'daily_schedule': [], 'weekly_schedule': []}
        table = parsed.find('div', {'class': 'site-panel__cafeinfo-inner'})
        special_hours_container = table.find('div', {'class': 'cafe-hours-special'})
        if special_hours_container is not None:
            special_hours_li_list = special_hours_container.find_all('li', {'class': 'day-part dotted-leader-container'})
            for special_hours_li in special_hours_li_list:
                info = special_hours_li.find_all('span')
                if len(info) < 2:
                    return None
                if ("Closed" in info[0].text):
                    schedule['special'].append({"closed": clean_string(info[1].text)})
                else:
                    schedule['special'].append({clean_string(info[0].text): clean_string(info[1].text)})
        weekly_hours_label = table.find(text='Weekly Schedule')
        if weekly_hours_label is not None:
            weekly_hours_container = weekly_hours_label.parent.parent.find('ul')
            if weekly_hours_container is not None:
                weekly_hours_li_list = weekly_hours_container.find_all('li')
                for weekly_hours_li in weekly_hours_li_list:
                    meal_name = clean_string(weekly_hours_li.find('span', {'class': 'pull-left'}).text)
                    meal_schedule = clean_string(weekly_hours_li.find('span', {'class': 'pull-right'}).text)
                    schedule['weekly_schedule'].append({'meal_name': meal_name, 'meal_schedule': clean_string(meal_schedule)})

        # Uncomment to enable initial parsing
        # daily_hours_container = table.find('ul', {'class': 'site-panel__cafeinfo-hours'})
        # if (daily_hours_container != None):
        #     daily_hours_li_list = daily_hours_container.find_all('li')
        #     for daily_hours_li in daily_hours_li_list:
        #         meal_name = clean_string(daily_hours_li.find('span', {'class': 'pull-left'}).text)
        #         meal_schedule = clean_string(daily_hours_li.find('span', {'class': 'pull-right'}).text)
        #         schedule['daily_schedule'].append({'meal_name': meal_name, 'meal_schedule': meal_schedule, "menu": []})
        return schedule

    def scrape_menus(self, parsed, data):
        ''' Scrape all available menus for this eatery
            Return number of menus added, add all menus to database
        '''
        meals_titles = parsed.find_all('h2', {'class': 'site-panel__daypart-panel-title'})
        if meals_titles is not None:
            for meal_title in meals_titles:
                meal_hours = meal_title.parent.parent.find('li', {'class': 'site-panel__daypart-utility-menu-item'}).text
                meal_content = meal_title.parent.parent.parent.find('div', {'class': 'c-tab__content-inner site-panel__daypart-tab-content-inner'})
                timespan = create_timespan(meal_hours)
                meal = {
                        'meal_title': clean_string(meal_title.text),
                        'menu': [],
                        'timespan': timespan
                }
                current_station = ""
                for element in meal_content:
                    if element.name == 'h3':
                        current_station = clean_string(element.text)
                    if element.name == 'div':
                        dish_title = clean_string(element.find('button', {'class': 'h4 site-panel__daypart-item-title'}).text)
                        dish_description = element.find('div', {'class': 'site-panel__daypart-item-description'}).text.replace('\n', '').replace('\t', '')
                        dish_vegetarian = element.find('img',
                        {'title': 'Vegetarian: Contains no meat, fish, poultry, shellfish or products derived from these sources but may contain dairy or eggs'})
                        dish_hours = re.findall("[01]?[0-9]:.*", dish_title.replace(',', ''))
                        dish_hours
                        if len(dish_hours) == 0:
                            dish_hours = timespan
                        else:
                            dish_hours = create_timespan(dish_hours[0])
                        dish = {
                            'dish_name': clean_string(re.split("\d.*", dish_title)[0]),
                            'dish_description': dish_description,
                            'vegetarian': dish_vegetarian is not None,
                            'station': current_station,
                            'timespan': dish_hours
                        }
                        meal['menu'].append(dish)
                data['daily_schedule'].append(meal)


    def update_db(self, data):
        ''' Add a single menu to the database
            Return True if successful, otherwise False
        '''
        with sqlite3.connect(os.environ['DB_LOCATION']) as con:
            for meal in data['daily_schedule']:
                for dish in meal['menu']:
                    # Create IDs by hashing name and description
                    dish_id = str(hashlib.sha1((dish['dish_name'] + dish['dish_description']).encode('utf-8')).hexdigest())
                    c = con.execute("INSERT OR REPLACE INTO dishes (id, name, description, vegetarian, station, meal, dining_hall) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (dish_id, dish['dish_name'], dish['dish_description'], dish['vegetarian'], dish['station'], meal['meal_title'], self.name))
            now = datetime.datetime.now()
            id = abs(hash(datetime.datetime.now()))
            con.execute("INSERT OR REPLACE INTO dining_data (id, dining_hall, special_data, weekly_schedule, daily_schedule, year, month, day, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (id, self.name, json.dumps(data['special']),
                        json.dumps(data['weekly_schedule']),
                        json.dumps(data['daily_schedule']), int(now.year),
                        int(now.month), int(now.day), str(datetime.datetime.now())))

# Helper methods
def create_timespan(str):
    s_e_tuple = clean_string(str).split(" - ")
    try:
        start_time = datetime.datetime.strptime(s_e_tuple[0], "%I:%M %p")
    except ValueError:
        try:
            start_time = datetime.datetime.strptime(s_e_tuple[0], "%I:%M%p")
        except ValueError:
            start_time = datetime.datetime.strptime(s_e_tuple[0], "%I%p")
    try:
        end_time = datetime.datetime.strptime(s_e_tuple[1], "%I:%M %p")
    except ValueError:
        try:
            end_time = datetime.datetime.strptime(s_e_tuple[1], "%I:%M%p")
        except ValueError:
            end_time = datetime.datetime.strptime(s_e_tuple[1], "%I%p")
    now = datetime.datetime.now()
    start_time = start_time.replace(year=now.year, month=now.month, day=now.day).isoformat()
    end_time = end_time.replace(year=now.year, month=now.month, day=now.day).isoformat()
    timespan = {
        'start_time': start_time,
        'end_time': end_time
    }
    return timespan

def clean_string(str):
    str = str.replace(u'\xa0', u' ').replace('\n', '').replace('	', '').replace('  ', '')
    if str[0] == " ":
        str = str[1:]
    if str[-1] == " ":
        str = str[:-1]
    return str

def get_html(url):
    ''' The HTML data for a given URL '''
    return requests.get(url, verify=False).text
