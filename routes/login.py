from flask import request, jsonify
import re
import pymysql
from werkzeug.security import check_password_hash
from database_connection import get_db_connection

def login():
    data = request.json
    useremail = data.get('useremail')
    password = data.get('password')
    
    if not useremail or not password:
        return jsonify({'error': 'Invalid input'}), 400
    
    if not re.match(r'^\S+@\S+\.\S+$', useremail):
        return jsonify({'error': 'Invalid email format'}), 400
    
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM registration_form WHERE useremail = %s", (useremail,))
        user = cursor.fetchone()
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        
        if not check_password_hash(user['password'], password):
            return jsonify({'error': 'Incorrect password'}), 401
        
        return jsonify({'message': 'Login successful'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
