import sys
import os
from flask import Flask, request, jsonify
from database_connection import get_postgresql_connection
import psycopg2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)

@app.route('/create_location', methods=['POST'])
def create_location():
    data = request.json
    location_name = data.get('location_name')
    city = data.get('city')
    state = data.get('state')
    zip_code = data.get('zip_code')
    time_zone = data.get('time_zone')
    country = data.get('country')
    
    if not location_name:
        return jsonify({'error': 'Missing location_name'}), 400
    if not city:
        return jsonify({'error': 'Missing city'}), 400
    if not state:
        return jsonify({'error': 'Missing state'}), 400
    if not zip_code:
        return jsonify({'error': 'Missing zip_code'}), 400
    if not time_zone:
        return jsonify({'error': 'Missing time_zone'}), 400
    if not country:
        return jsonify({'error': 'Missing country'}), 400
    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO location_form (location_name, city, state, zip_code, time_zone, country) VALUES (%s, %s, %s, %s, %s, %s)", 
                       (location_name, city, state, zip_code, time_zone, country))
        connection.commit()
        return jsonify({'message': 'Location created successfully'}), 201
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_location', methods=['GET'])
def get_location():
    location_name = request.args.get('location_name')
    
    if not location_name:
        return jsonify({'error': 'Missing location_name parameter'}), 400

    connection = get_postgresql_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cursor.execute("SELECT * FROM location_form WHERE location_name = %s", (location_name,))
        location = cursor.fetchone()
        if location is None:
            return jsonify({'message': 'Location not found'}), 404
        return jsonify(dict(location)), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/update_location', methods=['PUT'])
def update_location():
    data = request.json
    location_name = data.get('location_name')
    city = data.get('city')
    state = data.get('state')
    zip_code = data.get('zip_code')
    time_zone = data.get('time_zone')
    country = data.get('country')
    
    if not location_name or (not city and not state and not zip_code and not time_zone and not country):
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        if city:
            cursor.execute("UPDATE location_form SET city = %s WHERE location_name = %s", (city, location_name))
        if state:
            cursor.execute("UPDATE location_form SET state = %s WHERE location_name = %s", (state, location_name))
        if zip_code:
            cursor.execute("UPDATE location_form SET zip_code = %s WHERE location_name = %s", (zip_code, location_name))
        if time_zone:
            cursor.execute("UPDATE location_form SET time_zone = %s WHERE location_name = %s", (time_zone, location_name))
        if country:
            cursor.execute("UPDATE location_form SET country = %s WHERE location_name = %s", (country, location_name))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Location not found'}), 404
        return jsonify({'message': 'Location updated successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_location', methods=['DELETE'])
def delete_location():
    data = request.json
    location_name = data.get('location_name')
    
    if not location_name:
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM location_form WHERE location_name = %s", (location_name,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Location not found'}), 404
        return jsonify({'message': 'Location deleted successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_all_locations', methods=['GET'])
def get_all_locations():
    try:
        connection = get_postgresql_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM location_form")
        locations = cursor.fetchall()
        locations_list = []
        for location in locations:
            location_dict = {
                "id": location['id'],
                "location_name": location['location_name'],
                "city": location['city'],
                "state": location['state'],
                "zip_code": location['zip_code'],
                "time_zone": location["time_zone"],
                "country": location["country"]
            }
            locations_list.append(location_dict)
        return jsonify(locations_list), 200
    except psycopg2.Error as e:
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_all_locations', methods=['DELETE'])
def delete_all_locations():
    try:
        connection = get_postgresql_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM location_form")
        connection.commit()
        return jsonify({'message': 'All locations deleted successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
