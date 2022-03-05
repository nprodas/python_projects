import flask
from flask import jsonify
from flask import request
from sql_shortcuts import create_connection
from sql_shortcuts import execute_read_query
from sql_shortcuts import execute_query


app = flask.Flask(__name__)  # sets up the app
app.config["DEBUG"] = True  # allow to show errors in browser

conn = create_connection(
    'cis3368.c2qcuzhb6ali.us-east-1.rds.amazonaws.com', 'nprodas', 'nprodas3368', 'CIS3368_db')

# GET method API is used to get trip id from URL params
@app.route('/api/trip', methods=['GET'])
def get_trip():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID provided!'

    # SQL script gets trip table and for loop iterates until id matches 
    trips = execute_read_query(conn, "SELECT * FROM trip")
    results = []

    for trip in trips:
        if trip['id'] == id:
            results.append(trip)
    # result is return in json format
    return jsonify(results)


# POST method API takes a json body script and adds the new trip to the table
@app.route('/api/trip', methods=['POST'])
def add_trip():
    request_data = request.get_json()
    new_trip = request_data['trip_name']
    new_destination = request_data['destination_id']
    new_transport = request_data['transportation']
    new_startdate = request_data['start_date']
    new_enddate = request_data['end_date']

    add_query = "INSERT INTO trip (trip_name, destination_id, transportation, start_date, end_date) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
        new_trip, new_destination, new_transport, new_startdate, new_enddate)

    execute_query(conn, add_query)

    return 'New trip has been added'

# PUT method API that gets trip id from URL params to update that trip's attributes
@app.route('/api/trip', methods=['PUT'])
def update_trip():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID provided!'
    
    # json body script is used to get data
    update_data = request.get_json()

    # for loop iterates through the json script and updates trip with given attributes using SQL
    for data in update_data:
        update_query = "UPDATE trip SET {} = '{}' WHERE id = {}".format(
            data, update_data[data], id)
        execute_query(conn, update_query)

    return 'Trip has been updated'

# POST method API takes a json body script and adds the new destination to the table
@app.route('/api/destination', methods=['POST'])
def add_destination():
    request_data = request.get_json()
    new_country = request_data['country']
    new_city = request_data['city']
    new_sightseeing = request_data['sightseeing']

    add_query = "INSERT INTO destination (country, city, sightseeing) VALUES ('{}', '{}', '{}')".format(
        new_country, new_city, new_sightseeing)

    execute_query(conn, add_query)

    return 'New destination has been added'

# PUT method API that gets destination id from URL params to update that destination attributes
@app.route('/api/destination', methods=['PUT'])
def update_destination():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID provided!'
    # json body script is used to get data
    update_data = request.get_json()

    # for loop iterates through the json script and updates destination with given attributes using SQL
    for data in update_data:
        update_query = "UPDATE destination SET {} = '{}' WHERE id = {}".format(
            data, update_data[data], id)
        execute_query(conn, update_query)

    return 'Destination has been updated'

# DELETE method API uses json get request for id
@app.route('/api/destination', methods=['DELETE'])
def delete_destination():
    request_data = request.get_json()
    idToDelete = int(request_data['id'])

    # destination is deteled using SQL script
    remove_query = "DELETE FROM destination WHERE id = {}".format(idToDelete)
    execute_query(conn, remove_query)

    return 'Destination has been deleted'

if __name__ == "__main__":
    app.run()