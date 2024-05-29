import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from schemas.company_db import initialize_database
from database_connection import get_db_connection
import pymysql

app = Flask(__name__)

@app.route('/create_company', methods=['POST'])
def create_company():
    data = request.json
    company_name = data.get('company_name')
    website_url = data.get('website_url')
    phone_no = data.get('phone_no')
    industry_name = data.get('industry_name')
    
    if not company_name or not website_url or not phone_no or not industry_name:
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO company (company_name, website_url, phone_no, industry_name) VALUES (%s, %s, %s, %s)", 
                       (company_name, website_url, phone_no, industry_name))
        connection.commit()
        return jsonify({'message': 'Company created successfully'}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_company', methods=['GET'])
def get_company():
    company_name = request.args.get('company_name')
    
    if not company_name:
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM company WHERE company_name = %s", (company_name,))
        company = cursor.fetchone()
        if company is None:
            return jsonify({'message': 'Company not found'}), 404
        return jsonify(company), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/update_company', methods=['PUT'])
def update_company():
    data = request.json
    company_name = data.get('company_name')
    website_url = data.get('website_url')
    phone_no = data.get('phone_no')
    industry_name = data.get('industry_name')
    
    if not company_name or (not website_url and not phone_no and not industry_name):
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        if website_url:
            cursor.execute("UPDATE company SET website_url = %s WHERE company_name = %s", (website_url, company_name))
        if phone_no:
            cursor.execute("UPDATE company SET phone_no = %s WHERE company_name = %s", (phone_no, company_name))
        if industry_name:
            cursor.execute("UPDATE company SET industry_name = %s WHERE company_name = %s", (industry_name, company_name))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Company not found'}), 404
        return jsonify({'message': 'Company updated successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_company', methods=['DELETE'])
def delete_company():
    data = request.json
    company_name = data.get('company_name')
    
    if not company_name:
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM company WHERE company_name = %s", (company_name,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Company not found'}), 404
        return jsonify({'message': 'Company deleted successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
        
if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
