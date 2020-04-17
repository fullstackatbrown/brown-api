from flask import request, jsonify
from api import con, app, make_json_error, support_jsonp
from api.meta import require_client_id
import requests
import sqlite3
import json
import os

from datetime import datetime, date, timedelta
from difflib import get_close_matches

'''
DATABASE OBJECTS: View templates on the private, repository README.
Nutritional info is not yet finished. Contact Joe for a preliminary template.
'''

# simplify database names
# menus = db.dining_menus
# hours = db.dining_hours
# nutritional_info = db.dining_nutritional_info
# all_foods = db.dining_all_foods

# TODO these should be updated with the database
# create list of valid eatery names and valid food names
valid_eatery_names = ['ratty', 'vdub']
valid_food_names = []


@app.route('/dining')
@support_jsonp
@require_client_id()
def dining_index():
    return make_json_error('No method specified. '
                           'See documentation for endpoints.')


@app.route('/dining/cafe/<cafe_id>')
@support_jsonp
@require_client_id()
def req_cafe(cafe_id):
    hall_url = "http://legacy.cafebonappetit.com/api/2/cafes?cafe=" + cafe_id
    data = requests.get(hall_url).json()
    return jsonify(results=data)


@app.route('/dining/cafe/<cafe_id>/menu/<date>')
@support_jsonp
@require_client_id()
def req_menu_date(cafe_id, date):
    hall_url = "http://legacy.cafebonappetit.com/api/2/menus?cafe=" + cafe_id + "&date=" + date
    data = clean_data(requests.get(hall_url).json())
    return jsonify(results=data)


@app.route('/dining/cafe/<cafe_id>/menu')
@support_jsonp
@require_client_id()
def req_menu(cafe_id):
    hall_url = "http://legacy.cafebonappetit.com/api/2/menus?cafe=" + cafe_id
    data = clean_data(requests.get(hall_url).json())
    return jsonify(results=data)

def clean_data(data):
        dishes = data['items']
        items_augmented = {}
        with con.cursor() as cur:
            for id in dishes:
                dish = dishes[id]
                cur.execute("SELECT * FROM dishes WHERE id = %s", (id,))
                dish_data = cur.fetchone()
                if dish_data is None:
                    vegetarian = ('1' in dish['cor_icon'])
                    vegan = ('4' in dish['cor_icon'])
                    gluten_free = ('9' in dish['cor_icon'])
                    halal = ('10' in dish['cor_icon'])
                    kosher = ('11' in dish['cor_icon'])
                    cur.execute("INSERT INTO dishes (id, name, description, \
                        vegetarian, vegan, gluten_free, halal, kosher) VALUES \
                        (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (dish['id'], dish['label'], dish['description'],
                        vegetarian, vegan, gluten_free, halal, kosher))
                else:
                    # Gather ratings
                    print("Gather ratings")
                dish_obj = {
                                'id': dish['id'],
                                'name': dish['label'],
                                'description': dish['description'],
                                'vegetarian': ('1' in dish['cor_icon']),
                                'vegan': ('4' in dish['cor_icon']),
                                'gluten_free': ('9' in dish['cor_icon']),
                                'halal': ('10' in dish['cor_icon']),
                                'kosher': ('11' in dish['cor_icon'])
                            }
                items_augmented[dish['id']] = dish_obj
        # Delete irrelevant sections
        del data['items']
        del data['cor_icons']
        del data['superplates']
        del data['version']
        # Replace all item data with relevant info
        for day_i, day in enumerate(data['days']):
            for cafe_id in day['cafes']:
                data['days'][day_i]['cafes'][cafe_id]['dayparts'] = data['days'][day_i]['cafes'][cafe_id]['dayparts'][0]
                for daypart_i, daypart in enumerate(day['cafes'][cafe_id]['dayparts']):
                    for station_i, station in enumerate(daypart['stations']):
                        for item_i, item in enumerate(station['items']):
                            data['days'][day_i]['cafes'][cafe_id]['dayparts'][daypart_i]['stations'][station_i]['items'][item_i] = items_augmented[item]
        return data
