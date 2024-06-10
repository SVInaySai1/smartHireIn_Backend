import sys
import os

import re
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database_connection import get_postgresql_connection

app = Flask(__name__)

def is_valid_mobile(mobile_number):
    return re.match(r'^[6-9]\d{9}$', mobile_number) is not None

def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password) or \
       not re.search(r'[a-z]', password) or \
       not re.search(r'\d', password) or \
       not re.search(r'[!@#$%^&*()-_+=]', password):
        return False
    return True

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    country_code = data.get('country_code')
    mobile_number = data.get('mobile_number')
    useremail = data.get('useremail')
    password = data.get('password')
    re_enter_password = data.get('re_enter_password')
    gender = data.get('gender')

    if not all([first_name, last_name, country_code, mobile_number, useremail, password, re_enter_password, gender]):
        return jsonify({'error': 'All fields are required'}), 400

    if password != re_enter_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    if not is_valid_mobile(mobile_number):
        return jsonify({'error': 'Mobile number must be a valid 10-digit Indian number starting with 6-9'}), 400

    if not is_strong_password(password):
        return jsonify({'error': 'Password must be at least 8 characters long and contain a combination of uppercase letters, lowercase letters, numbers, and symbols'}), 400

    full_mobile_number = f"{country_code}{mobile_number}"
    hashed_password = generate_password_hash(password)

    try:
        with get_postgresql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO registration_form (first_name, last_name, country_code, mobile_number, useremail, password, gender) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (first_name, last_name, country_code, full_mobile_number, useremail, hashed_password, gender))
                connection.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_user', methods=['GET'])
def get_user():
    useremail = request.args.get('useremail')

    if not useremail:
        return jsonify({'error': 'User email is required'}), 400

    try:
        with get_postgresql_connection() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM registration_form WHERE useremail = %s", (useremail,))
                user = cursor.fetchone()
                if user is None:
                    return jsonify({'message': 'User not found'}), 404
                return jsonify(dict(user)), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_user', methods=['PUT'])
def update_user():
    data = request.json
    useremail = data.get('useremail')
    if not useremail:
        return jsonify({'error': 'User email is required'}), 400

    fields = ['first_name', 'last_name', 'country_code', 'mobile_number', 'password', 'gender']
    update_data = {field: data.get(field) for field in fields if data.get(field)}

    if not update_data:
        return jsonify({'error': 'No update data provided'}), 400

    if 'mobile_number' in update_data and not is_valid_mobile(update_data['mobile_number']):
        return jsonify({'error': 'Mobile number must be a valid 10-digit Indian number starting with 6-9'}), 400

    if 'password' in update_data:
        update_data['password'] = generate_password_hash(update_data['password'])

    set_clause = ", ".join(f"{field} = %s" for field in update_data.keys())
    params = list(update_data.values()) + [useremail]

    try:
        with get_postgresql_connection() as connection:
            with connection.cursor() as cursor:
                sql_query = sql.SQL("UPDATE registration_form SET {} WHERE useremail = %s").format(sql.SQL(set_clause))
                cursor.execute(sql_query, params)
                connection.commit()
                if cursor.rowcount == 0:
                    return jsonify({'message': 'User not found'}), 404
                return jsonify({'message': 'User updated successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    data = request.json
    useremail = data.get('useremail')

    if not useremail:
        return jsonify({'error': 'User email is required'}), 400

    try:
        with get_postgresql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM registration_form WHERE useremail = %s", (useremail,))
                connection.commit()
                if cursor.rowcount == 0:
                    return jsonify({'message': 'User not found'}), 404
                return jsonify({'message': 'User deleted successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    

def get_all_users():
    query = "SELECT * FROM registration_form"
    try:
        connection = get_postgresql_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query)
        users = cursor.fetchall()
        if not users:
            return jsonify({'message': 'No users found'}), 404
        users_list = []
        for user in users:
            user_dict = {
                "first_name": user['first_name'],
                "last_name": user['last_name'],
                "country_code": user['country_code'],
                "mobile_number": user['mobile_number'],
                "useremail": user['useremail'],
                "gender": user['gender']
            }
            users_list.append(user_dict)
        return jsonify(users_list), 200
    except psycopg2.Error as e:
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


def delete_all_users():
    try:
        with get_postgresql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM registration_form")
                connection.commit()
                return jsonify({'message': 'All users deleted successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
