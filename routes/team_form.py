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
    name_of_members = data.get('name_of_members')  # Corrected variable name
    
    if not team_head:
        return jsonify({'error': 'Missing team_head'}), 400
    elif not team_name:
        return jsonify({'error': 'Missing team_name'}), 400
    elif not no_of_members:
        return jsonify({'error': 'Missing no_of_members'}), 400
    elif not name_of_members:
        return jsonify({'error': 'Missing name_of_members'}), 400

    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO team_form (team_name, team_head, no_of_members, name_of_members) VALUES (%s, %s, %s, %s)",
                       (team_name, team_head, no_of_members, name_of_members))
        connection.commit()
        return jsonify({'message': 'Team created successfully'}), 201
    except psycopg2.Error as e:
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_teams', methods=['GET'])
def get_teams():
    connection = get_postgresql_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cursor.execute("SELECT * FROM team_form")
        teams = cursor.fetchall()
        team_list = []
        for team in teams:
            team_dict = {
                "id": team['id'],
                "team_name": team['team_name'],
                "team_head": team['team_head'],
                "no_of_members": team['no_of_members'],
                "name_of_members": team['name_of_members']
            }
            team_list.append(team_dict)
        return jsonify(team_list), 200
    except psycopg2.Error as e:
        print(f"Error: {e}")  # Log the error for debugging
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
    name_of_members = data.get('name_of_members')

    if not team_name or (not team_head and not no_of_members and not name_of_members):
        return jsonify({'error': 'Invalid input'}), 400

    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        update_statements = []
        params = []
        if team_head:
            update_statements.append("team_head = %s")
            params.append(team_head)
        if no_of_members:
            update_statements.append("no_of_members = %s")
            params.append(no_of_members)
        if name_of_members:
            update_statements.append("name_of_members = %s")
            params.append(name_of_members)

        if update_statements:
            update_clause = ", ".join(update_statements)
            sql = f"UPDATE team_form SET {update_clause} WHERE team_name = %s"
            cursor.execute(sql, params + [team_name])
            connection.commit()

            if cursor.rowcount == 0:
                return jsonify({'message': 'Team not found'}), 404
            return jsonify({'message': 'Team updated successfully'}), 200
        else:
            return jsonify({'message': 'No fields to update'}), 
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

@app.route('/get_team_by_name', methods=['GET'])
def get_team_by_name():
    team_name = request.args.get('team_name')

    if not team_name:
        return jsonify({'error': 'Team name is required'}), 400

    connection = get_postgresql_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cursor.execute("SELECT * FROM team_form WHERE team_name = %s", (team_name,))
        team = cursor.fetchone()
        if team is None:
            return jsonify({'message': 'Team not found'}), 404
        return jsonify(dict(team)), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_all_teams', methods=['DELETE'])
def delete_all_teams():
    try:
        with get_postgresql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM team_form")
                connection.commit()
                if cursor.rowcount == 0:
                    return jsonify({'message': 'No teams found to delete'}), 404
                return jsonify({'message': 'All teams deleted successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500