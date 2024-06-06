import sys
import os
import re
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
import pymysql

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database_connection import get_db_connection

app = Flask(__name__)

def is_valid_mobile(mobile_number):
    return re.match(r'^[6-9]\d{9}$', mobile_number) is not None 

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

    full_mobile_number = f"{country_code}{mobile_number}"
    hashed_password = generate_password_hash(password)

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO registration_form (first_name, last_name, country_code, mobile_number, useremail, password, gender) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, country_code, full_mobile_number, useremail, hashed_password, gender))
        connection.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

def get_user():
    useremail = request.args.get('useremail')
    
    if not useremail:
        return jsonify({'error': 'User email is required'}), 400

    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM registration_form WHERE useremail = %s", (useremail,))
        user = cursor.fetchone()
        if user is None:
            return jsonify({'message': 'User not found'}), 404
        return jsonify(user), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

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

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        sql = f"UPDATE registration_form SET {set_clause} WHERE useremail = %s"
        cursor.execute(sql, params)
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'User not found'}), 404
        return jsonify({'message': 'User updated successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

def delete_user():
    data = request.json
    useremail = data.get('useremail')
    
    if not useremail:
        return jsonify({'error': 'User email is required'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM registration_form WHERE useremail = %s", (useremail,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'User not found'}), 404
        return jsonify({'message': 'User deleted successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()