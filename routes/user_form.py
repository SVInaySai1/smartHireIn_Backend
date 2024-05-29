import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from schemas.user_form_db import initialize_database
from database_connection import get_db_connection
import pymysql

app = Flask(__name__)

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    user_name = data.get('user_name')
    department = data.get('department')
    gender = data.get('gender')
    admin_access = data.get('admin_access')
    role = data.get('role')
    
    if not user_name or not department or not gender or not admin_access or not role:
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO user_form (user_name, department, gender, admin_access, role) VALUES (%s, %s, %s, %s, %s)", 
                       (user_name, department, gender, admin_access, role))
        connection.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_user', methods=['GET'])
def get_user():
    user_name = request.args.get('user_name')
    
    if not user_name:
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM user_form WHERE user_name = %s", (user_name,))
        user = cursor.fetchone()
        if user is None:
            return jsonify({'message': 'User not found'}), 404
        return jsonify(user), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/update_user', methods=['PUT'])
def update_user():
    data = request.json
    user_name = data.get('user_name')
    department = data.get('department')
    gender = data.get('gender')
    admin_access = data.get('admin_access')
    role = data.get('role')
    
    if not user_name or (not department and not gender and not admin_access and not role):
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        if department:
            cursor.execute("UPDATE user_form SET department = %s WHERE user_name = %s", (department, user_name))
        if gender:
            cursor.execute("UPDATE user_form SET gender = %s WHERE user_name = %s", (gender, user_name))
        if admin_access:
            cursor.execute("UPDATE user_form SET admin_access = %s WHERE user_name = %s", (admin_access, user_name))
        if role:
            cursor.execute("UPDATE user_form SET role = %s WHERE user_name = %s", (role, user_name))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'User not found'}), 404
        return jsonify({'message': 'User updated successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    data = request.json
    user_name = data.get('user_name')
    
    if not user_name:
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM user_form WHERE user_name = %s", (user_name,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'User not found'}), 404
        return jsonify({'message': 'User deleted successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)