import sys
import os
import re
from flask import Flask, request, jsonify
from database_connection import get_postgresql_connection
import psycopg2
import psycopg2.extras

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)

# Regular expressions for validation
email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
phone_regex = re.compile(r'^[6-9]\d{9}$')

def is_valid_email(email):
    return email_regex.match(email) is not None

def is_valid_phone(phone):
    return phone_regex.match(phone) is not None

@app.route('/create_profile', methods=['POST'])
def create_profile():
    data = request.json
    email_id = data.get('email_id')
    phone = data.get('phone')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not email_id or not phone or not first_name or not last_name:
        return jsonify({'error': 'All fields are required'}), 400
    if not is_valid_email(email_id):
        return jsonify({'error': 'Invalid email address'}), 400
    if not is_valid_phone(phone):
        return jsonify({'error': 'Invalid phone number'}), 400

    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO profile_form (email_id, phone, first_name, last_name) VALUES (%s, %s, %s, %s)",
            (email_id, phone, first_name, last_name)
        )
        connection.commit()
        return jsonify({'message': 'Profile created successfully'}), 201
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_profile', methods=['GET'])
def get_profile():
    email_id = request.args.get('email_id')

    if not email_id:
        return jsonify({'error': 'Invalid input'}), 400
    if not is_valid_email(email_id):
        return jsonify({'error': 'Invalid email address'}), 400

    connection = get_postgresql_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cursor.execute(
            "SELECT email_id, phone, first_name, last_name FROM profile_form WHERE email_id = %s",
            (email_id,)
        )
        profile = cursor.fetchone()
        if profile is None:
            return jsonify({'message': 'Profile not found'}), 404
        return jsonify(dict(profile)), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/update_profile', methods=['PUT'])
def update_profile():
    data = request.json
    email_id = data.get('email_id')
    phone = data.get('phone')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not email_id or (not phone and not first_name and not last_name):
        return jsonify({'error': 'Invalid input'}), 400
    if not is_valid_email(email_id):
        return jsonify({'error': 'Invalid email address'}), 400
    if phone and not is_valid_phone(phone):
        return jsonify({'error': 'Invalid phone number'}), 400

    connection = get_postgresql_connection()
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
    except psycopg2.Error as e:
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
    if not is_valid_email(email_id):
        return jsonify({'error': 'Invalid email address'}), 400

    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM profile_form WHERE email_id = %s", (email_id,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Profile not found'}), 404
        return jsonify({'message': 'Profile deleted successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_all_profiles', methods=['GET'])
def get_all_profiles():
    try:
        connection = get_postgresql_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM profile_form")
        profiles = cursor.fetchall()
        profiles_list = []
        for profile in profiles:
            profile_dict = {
                "email_id": profile['email_id'],
                "phone": profile['phone'],
                "first_name": profile['first_name'],
                "last_name": profile['last_name']
            }
            profiles_list.append(profile_dict)
        return jsonify(profiles_list), 200
    except psycopg2.Error as e:
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_all_profiles', methods=['DELETE'])
def delete_all_profiles():
    try:
        connection = get_postgresql_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM profile_form")
        connection.commit()
        return jsonify({'message': 'All profiles deleted successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
