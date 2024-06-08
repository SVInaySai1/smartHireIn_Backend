import sys
import os
import re
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database_connection import get_postgresql_connection

app = Flask(__name__)

def is_valid_department_name(department_name):
    return re.match(r'^[a-zA-Z\s]+$', department_name) is not None

@app.route('/create_department', methods=['POST'])
def create_department():
    data = request.json
    department_name = data.get('department_name')
    created_by = data.get('created_by')

    if not all([department_name, created_by]):
        return jsonify({'error': 'Department name and created by fields are required'}), 400

    if not is_valid_department_name(department_name):
        return jsonify({'error': 'Department name can only contain letters and spaces'}), 400

    try:
        with get_postgresql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO department (department_name, created_by, last_modified)
                    VALUES (%s, %s, %s)
                """, (department_name, created_by, datetime.now().strftime('%d/%m/%Y')))
                connection.commit()
        return jsonify({'message': 'Department created successfully'}), 201
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_department', methods=['PUT'])
def update_department():
    data = request.json
    department_name = data.get('department_name')
    updated_by = data.get('updated_by')

    if not department_name:
        return jsonify({'error': 'Department name is required'}), 400

    if not is_valid_department_name(department_name):
        return jsonify({'error': 'Department name can only contain letters and spaces'}), 400

    try:
        with get_postgresql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE department 
                    SET updated_by = %s, last_modified = %s
                    WHERE department_name = %s
                """, (updated_by, datetime.now().strftime('%d/%m/%Y'), department_name))
                connection.commit()
                if cursor.rowcount == 0:
                    return jsonify({'message': 'Department not found'}), 404
                return jsonify({'message': 'Department updated successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/departments', methods=['GET'])
def get_departments():
    try:
        with get_postgresql_connection() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM department")
                departments = cursor.fetchall()
                return jsonify({'departments': [dict(dep) for dep in departments]}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500


@app.route('/delete_department', methods=['DELETE'])
def delete_department():
    data = request.json
    department_name = data.get('department_name')

    if not department_name:
        return jsonify({'error': 'Department name is required'}), 400

    try:
        with get_postgresql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM department WHERE department_name = %s", (department_name,))
                connection.commit()
                if cursor.rowcount == 0:
                    return jsonify({'message': 'Department not found'}), 404
                return jsonify({'message': 'Department deleted successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
