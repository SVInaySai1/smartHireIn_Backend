import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from database_connection import get_postgresql_connection
import psycopg2

app = Flask(__name__)

@app.route('/create_team', methods=['POST'])
def create_team():
    data = request.json
    team_name = data.get('team_name')
    team_head = data.get('team_head')
    no_of_members = data.get('no_of_members')
    name_of_member = data.get('name_of_member')
    
    if not team_name or not team_head or not no_of_members or not name_of_member:
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO team_form (team_name, team_head, no_of_members, name_of_member) VALUES (%s, %s, %s, %s)", 
                       (team_name, team_head, no_of_members, name_of_member))
        connection.commit()
        return jsonify({'message': 'Team created successfully'}), 201
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_team', methods=['GET'])
def get_team():
    team_name = request.args.get('team_name')
    
    if not team_name:
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_postgresql_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cursor.execute("SELECT * FROM team_form WHERE team_name = %s", (team_name,))
        team = cursor.fetchone()
        if team is None:
            return jsonify({'message': 'Team not found'}), 404
        return jsonify(team), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/update_team', methods=['PUT'])
def update_team():
    data = request.json
    team_name = data.get('team_name')
    team_head = data.get('team_head')
    no_of_members = data.get('no_of_members')
    name_of_member = data.get('name_of_member')
    
    if not team_name or (not team_head and not no_of_members and not name_of_member):
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        if team_head:
            cursor.execute("UPDATE team_form SET team_head = %s WHERE team_name = %s", (team_head, team_name))
        if no_of_members:
            cursor.execute("UPDATE team_form SET no_of_members = %s WHERE team_name = %s", (no_of_members, team_name))
        if name_of_member:
            cursor.execute("UPDATE team_form SET name_of_member = %s WHERE team_name = %s", (name_of_member, team_name))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Team not found'}), 404
        return jsonify({'message': 'Team updated successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_team', methods=['DELETE'])
def delete_team():
    data = request.json
    team_name = data.get('team_name')
    
    if not team_name:
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM team_form WHERE team_name = %s", (team_name,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Team not found'}), 404
        return jsonify({'message': 'Team deleted successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
