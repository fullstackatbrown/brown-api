from flask import request, jsonify
from api import con, app, make_json_error, support_jsonp
from api.meta import require_client_id
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


@app.route('/dining/schedule')
@support_jsonp
@require_client_id()
def req_dining_menu():
    ''' Endpoint for all menu requests (see README for documentation) '''
    with con.cursor() as cur:
        cur.execute("SELECT * FROM dining_halls")
        hall_result = cur.fetchall()
        dining_halls = [{"dining_hall": h[0]} for h in hall_result]
        for hall in dining_halls:
            cur.execute("SELECT * FROM dining_data WHERE dining_hall = %s ORDER BY created_at DESC LIMIT 1", (hall['dining_hall'],))
            hall_data = cur.fetchone()
            if hall_data is not None:
                hall['special_data'] = json.loads(hall_data[2])
                hall['weekly_schedule'] = json.loads(hall_data[3])
                hall['daily_schedule'] = json.loads(hall_data[4])
        cur.close()
        return jsonify(num_results=len(dining_halls), results=dining_halls)
