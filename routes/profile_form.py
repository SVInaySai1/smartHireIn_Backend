import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from database_connection import get_db_connection
import pymysql

app = Flask(__name__)

@app.route('/create_profile', methods=['POST'])
def create_profile():
    data = request.form
    email_id = data.get('email_id')
    phone = data.get('phone')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not email_id or not phone or not first_name or not last_name:
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO profile_form (email_id, phone, first_name, last_name) VALUES (%s, %s, %s, %s)",
                       (email_id, phone, first_name, last_name))
        connection.commit()
        return jsonify({'message': 'Profile created successfully'}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_profile', methods=['GET'])
def get_profile():
    email_id = request.args.get('email_id')

    if not email_id:
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT email_id, phone, first_name, last_name FROM profile_form WHERE email_id = %s", (email_id,))
        profile = cursor.fetchone()
        if profile is None:
            return jsonify({'message': 'Profile not found'}), 404
        return jsonify(profile), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/update_profile', methods=['PUT'])
def update_profile():
    data = request.form
    email_id = data.get('email_id')
    phone = data.get('phone')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not email_id or (not phone and not first_name and not last_name):
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        if phone:
            cursor.execute("UPDATE profile_form SET phone = %s WHERE email_id = %s", (phone, email_id))
        if first_name:
            cursor.execute("UPDATE profile_form SET first_name = %s WHERE email_id = %s", (first_name, email_id))
        if last_name:
            cursor.execute("UPDATE profile_form SET last_name = %s WHERE email_id = %s", (last_name, email_id))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Profile not found'}), 404
        return jsonify({'message': 'Profile updated successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_profile', methods=['DELETE'])
def delete_profile():
    data = request.json
    email_id = data.get('email_id')

    if not email_id:
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM profile_form WHERE email_id = %s", (email_id,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Profile not found'}), 404
        return jsonify({'message': 'Profile deleted successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
