import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sys
import os
from flask import Flask, request, jsonify
from database_connection import get_postgresql_connection
import psycopg2

app = Flask(__name__)

@app.route('/create_team_user', methods=['POST'])
def create_user():
    data = request.json
    user_name = data.get('user_name')
    department = data.get('department')
    gender = data.get('gender')
    admin_access = data.get('admin_access')
    role = data.get('role')

    if not user_name or not department or not gender or not role:
        return jsonify({'error': 'Invalid input'}), 400

    if admin_access not in ["yes", "no"]:
        return jsonify({'error': 'Invalid input for admin_access'}), 400

    admin_access_bool = True if admin_access == "yes" else False

    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO user_form (user_name, department, gender, admin_access, role) VALUES (%s, %s, %s, %s, %s)", 
                       (user_name, department, gender, admin_access_bool, role))
        connection.commit()
        return jsonify({'message': 'Team user created successfully'}), 201
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_user', methods=['GET'])
def get_user():
    user_name = request.args.get('user_name')
    
    if not user_name:
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_postgresql_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cursor.execute("SELECT * FROM user_form WHERE user_name = %s", (user_name,))
        user = cursor.fetchone()
        if user is None:
            return jsonify({'message': 'User not found'}), 404
        return jsonify(dict(user)), 200
    except psycopg2.Error as e:
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
    
    if not user_name or (department is None and gender is None and admin_access is None and role is None):
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        if department:
            cursor.execute("UPDATE user_form SET department = %s WHERE user_name = %s", (department, user_name))
        if gender:
            cursor.execute("UPDATE user_form SET gender = %s WHERE user_name = %s", (gender, user_name))
        if admin_access is not None:
            if admin_access not in ["yes", "no"]:
                return jsonify({'error': 'Invalid input for admin_access'}), 400
            admin_access_bool = True if admin_access == "yes" else False
            cursor.execute("UPDATE user_form SET admin_access = %s WHERE user_name = %s", (admin_access_bool, user_name))
        if role:
            cursor.execute("UPDATE user_form SET role = %s WHERE user_name = %s", (role, user_name))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'User not found'}), 404
        return jsonify({'message': 'User updated successfully'}), 200
    except psycopg2.Error as e:
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

    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM user_form WHERE user_name = %s", (user_name,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'User not found'}), 404
        return jsonify({'message': 'User deleted successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_all_users', methods=['GET'])
def get_all_users():
    query = "SELECT * FROM user_form"
    try:
        connection = get_postgresql_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query)
        users = cursor.fetchall()
        users_list = []
        for user in users:
            user_dict = {
                "user_name": user['user_name'],
                "department": user['department'],
                "gender": user['gender'],
                "admin_access": 'yes' if user['admin_access'] else 'no',
                "role": user['role']
            }
            users_list.append(user_dict)
        return jsonify(users_list), 200
    except psycopg2.Error as e:
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_all_users', methods=['DELETE'])
def delete_all_users():
    try:
        connection = get_postgresql_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM user_form")
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'No users found to delete'}), 404
        return jsonify({'message': 'All users deleted successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)