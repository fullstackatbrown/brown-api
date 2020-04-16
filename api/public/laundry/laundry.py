# vim: set ts=4 sts=4 sw=4 expandtab:
from flask import request, jsonify
from api import app, make_json_error, support_jsonp
from api.meta import require_client_id
from api.scripts.laundry import Room
import sqlite3
import os

'''
DATABASE OBJECTS: View templates on the private repository README.
'''

# simplify database names
# ldb = db.laundry


@app.route('/laundry')
@support_jsonp
@require_client_id()
def laundry_index():
    return make_json_error('No method specified. '
                           'See documentation for endpoints.')


@app.route('/laundry/rooms')
@support_jsonp
@require_client_id()
def req_laundry_room_list():
    with sqlite3.connect(os.environ['DB_LOCATION']) as con:
        c = con.execute("SELECT * FROM laundry_rooms")
        results = c.fetchall()
        result_list = [{"name": r[1], "id": r[0]} for r in results]
        return jsonify(num_results=len(result_list), results=result_list)

@app.route('/laundry/rooms/<room_id>')
@support_jsonp
@require_client_id()
def req_room_detail(room_id):
    with sqlite3.connect(os.environ['DB_LOCATION']) as con:
        c = con.execute("SELECT * FROM laundry_rooms WHERE id = ?", (int(room_id),))
        room = c.fetchone()
        if room is None:
            return make_json_error('Room not found')
        c = con.execute("SELECT * FROM laundry_machines WHERE room_id = ?", (int(room_id),))
        machines = c.fetchall()
        machine_list = [{"id": r[0], "room_id": r[1], "type": r[2]} for r in machines]
        room = {"id": room[0], "name": room[1], "machines": machine_list}
        return jsonify(result=room)

@app.route('/laundry/rooms/<room_id>/machines')
@support_jsonp
@require_client_id()
def req_machines(room_id):
    # TODO make a type field to filter on (washer, dryer, etc)
    with sqlite3.connect(os.environ['DB_LOCATION']) as con:
        machine_list = []
        if bool(request.args.get('get_status')):
            machine_list = Room.get_machine_statuses(room_id)
        else:
            c = con.execute("SELECT * FROM laundry_machines WHERE room_id = ?", (int(room_id),))
            machines = c.fetchall()
            if machines is None:
                return make_json_error('Machines not found')
            machine_list = [{"id": r[0], "room_id": r[1], "type": r[2]} for r in machines]

        # support a get_status parameter to optionally get machine statuses


        return jsonify(results=machine_list)


@app.route('/laundry/rooms/<room_id>/machines/<machine_id>')
@support_jsonp
@require_client_id()
def req_machine_details(room_id, machine_id):
    machine_return = {}
    # support a get_status parameter to optionally get machine status
    if bool(request.args.get('get_status')):
        machines = Room.get_machine_statuses(room_id)
        machine_return = list(filter(lambda x: x['id'] == str(machine_id), machines))
        if len(machine_return) is 0:
            return make_json_error("Machine not found")
        else:
            machine_return = machine_return[0]
    else:
        with sqlite3.connect(os.environ['DB_LOCATION']) as con:
            c = con.execute("SELECT * FROM laundry_machines WHERE id = ? AND room_id = ?", (int(machine_id), int(room_id)))
            machine = c.fetchone()
            print(machine)
            if machine is None:
                return make_json_error('Machines not found')
            machine_return = {"id": machine[0], "room_id": machine[1], "type": machine[2]}
    return jsonify(result=machine_return)
