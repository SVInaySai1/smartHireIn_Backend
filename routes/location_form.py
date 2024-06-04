import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from database_connection import get_db_connection
import pymysql

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
    
    if not location_name or not city or not state or not zip_code or not time_zone or not country:
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO location_form (location_name, city, state, zip_code, time_zone, country) VALUES (%s, %s, %s, %s, %s, %s)", 
                       (location_name, city, state, zip_code, time_zone, country))
        connection.commit()
        return jsonify({'message': 'Location created successfully'}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_location', methods=['GET'])
def get_location():
    location_name = request.args.get('location_name')
    
    if not location_name:
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM location_form WHERE location_name = %s", (location_name,))
        location = cursor.fetchone()
        if location is None:
            return jsonify({'message': 'Location not found'}), 404
        return jsonify(location), 200
    except pymysql.MySQLError as e:
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

    connection = get_db_connection()
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
    except pymysql.MySQLError as e:
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

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM location_form WHERE location_name = %s", (location_name,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Location not found'}), 404
        return jsonify({'message': 'Location deleted successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
