import os
import re
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from database_connection import get_db_connection
import pymysql

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'images'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def save_image(image):
    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        return image_path
    return None

def is_valid_phone(phone_no):
    return re.match(r'^[6-9]\d{9}$', phone_no) is not None

@app.route('/create_company', methods=['POST'])
def create_company():
    data = request.form
    company_name = data.get('company_name')
    website_url = data.get('website_url')
    phone_no = data.get('phone_no')
    industry_name = data.get('industry_name')
    image = request.files.get('image')
    
    if not company_name or not website_url or not phone_no or not industry_name:
        return jsonify({'error': 'Invalid input'}), 400
    
    if not is_valid_phone(phone_no):
        return jsonify({'error': 'Invalid phone number'}), 400

    image_path = save_image(image)

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO company (company_name, website_url, phone_no, industry_name, image) VALUES (%s, %s, %s, %s, %s)", 
                       (company_name, website_url, phone_no, industry_name, image_path))
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
    data = request.form
    company_name = data.get('company_name')
    website_url = data.get('website_url')
    phone_no = data.get('phone_no')
    industry_name = data.get('industry_name')
    image = request.files.get('image')
    
    if not company_name or (not website_url and not phone_no and not industry_name and not image):
        return jsonify({'error': 'Invalid input'}), 400

    if phone_no and not is_valid_phone(phone_no):
        return jsonify({'error': 'Invalid phone number'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        if website_url:
            cursor.execute("UPDATE company SET website_url = %s WHERE company_name = %s", (website_url, company_name))
        if phone_no:
            cursor.execute("UPDATE company SET phone_no = %s WHERE company_name = %s", (phone_no, company_name))
        if industry_name:
            cursor.execute("UPDATE company SET industry_name = %s WHERE company_name = %s", (industry_name, company_name))
        if image:
            image_path = save_image(image)
            cursor.execute("UPDATE company SET image = %s WHERE company_name = %s", (image_path, company_name))
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
