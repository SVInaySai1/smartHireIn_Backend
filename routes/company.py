import os
import re
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, send_from_directory, url_for
from werkzeug.utils import secure_filename
from database_connection import get_postgresql_connection
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'images'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def save_image(image):
    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        return filename  # Return just the filename
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

    image_filename = save_image(image)

    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO company (company_name, website_url, phone_no, industry_name, image) VALUES (%s, %s, %s, %s, %s)", 
                       (company_name, website_url, phone_no, industry_name, image_filename))
        connection.commit()
        return jsonify({'message': 'Company created successfully'}), 201
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_company', methods=['GET'])
def get_company():
    company_name = request.args.get('company_name')
    
    if not company_name:
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_postgresql_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cursor.execute("SELECT * FROM company WHERE company_name = %s", (company_name,))
        company = cursor.fetchone()
        if company is None:
            return jsonify({'message': 'Company not found'}), 404
        
        company_dict = dict(company)
        if company_dict['image']:
            company_dict['image_url'] = url_for('uploaded_file', filename=company_dict['image'], _external=True)
        else:
            company_dict['image_url'] = None  # Or any default image URL you want to use
        return jsonify(company_dict), 200
    except psycopg2.Error as e:
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

    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        if website_url:
            cursor.execute("UPDATE company SET website_url = %s WHERE company_name = %s", (website_url, company_name))
        if phone_no:
            cursor.execute("UPDATE company SET phone_no = %s WHERE company_name = %s", (phone_no, company_name))
        if industry_name:
            cursor.execute("UPDATE company SET industry_name = %s WHERE company_name = %s", (industry_name, company_name))
        if image:
            image_filename = save_image(image)
            cursor.execute("UPDATE company SET image = %s WHERE company_name = %s", (image_filename, company_name))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Company not found'}), 404
        return jsonify({'message': 'Company updated successfully'}), 200
    except psycopg2.Error as e:
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

    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM company WHERE company_name = %s", (company_name,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Company not found'}), 404
        return jsonify({'message': 'Company deleted successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/get_all_companies', methods=['GET'])
def get_all_companies():
    query = "SELECT id, company_name, website_url, phone_no, industry_name, image FROM company"
    try:
        connection = get_postgresql_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query)
        companies = cursor.fetchall()
        companies_list = []
        for company in companies:
            company_dict = {
                "id": company['id'],
                "company_name": company['company_name'],
                "website_url": company['website_url'],
                "phone_no": company['phone_no'],
                "industry_name": company['industry_name'],
                "image_path": company['image']  # Only include the image path without building URL
            }
            companies_list.append(company_dict)
        return jsonify(companies_list), 200
    except psycopg2.Error as e:
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_all_companies', methods=['DELETE'])
def delete_all_companies():
    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM company")
        connection.commit()
        return jsonify({'message': 'All companies deleted successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()