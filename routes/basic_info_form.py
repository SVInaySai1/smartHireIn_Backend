import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from database_connection import get_db_connection
import pymysql

app = Flask(__name__)

def create_basic_info():
    data = request.json
    required_fields = ['job_position', 'job_category', 'job_type', 'department', 'job_location', 'hiring_type', 'no_of_opening']
    
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({'error': 'Invalid input'}), 400

    query = """
    INSERT INTO basic_info_form (job_position, job_category, job_type, department, job_location, hiring_type, no_of_opening)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        data['job_position'], data['job_category'], data['job_type'], 
        data['department'], data['job_location'], data['hiring_type'], 
        data['no_of_opening']
    )

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                connection.commit()
                return jsonify({'message': 'Basic info created successfully'}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500

def get_basic_info():
    job_position = request.args.get('job_position')
    
    if not job_position:
        return jsonify({'error': 'Invalid input'}), 400

    query = "SELECT * FROM basic_info_form WHERE job_position = %s"
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (job_position,))
                basic_info = cursor.fetchone()
                if basic_info is None:
                    return jsonify({'message': 'Basic info not found'}), 404
                return jsonify(basic_info), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500

def update_basic_info():
    data = request.json
    job_position = data.get('job_position')
    
    if not job_position:
        return jsonify({'error': 'Invalid input'}), 400

    fields_to_update = {
        'job_category': data.get('job_category'),
        'job_type': data.get('job_type'),
        'department': data.get('department'),
        'job_location': data.get('job_location'),
        'hiring_type': data.get('hiring_type'),
        'no_of_opening': data.get('no_of_opening')
    }
    
    update_clauses = []
    update_params = []
    for field, value in fields_to_update.items():
        if value:
            update_clauses.append(f"{field} = %s")
            update_params.append(value)

    if not update_clauses:
        return jsonify({'error': 'No valid fields to update'}), 400

    update_query = f"UPDATE basic_info_form SET {', '.join(update_clauses)} WHERE job_position = %s"
    update_params.append(job_position)

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(update_query, tuple(update_params))
                connection.commit()
                if cursor.rowcount == 0:
                    return jsonify({'message': 'Basic info not found'}), 404
                return jsonify({'message': 'Basic info updated successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500

def delete_basic_info():
    data = request.json
    job_position = data.get('job_position')
    
    if not job_position:
        return jsonify({'error': 'Invalid input'}), 400

    query = "DELETE FROM basic_info_form WHERE job_position = %s"

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (job_position,))
                connection.commit()
                if cursor.rowcount == 0:
                    return jsonify({'message': 'Basic info not found'}), 404
                return jsonify({'message': 'Basic info deleted successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500

