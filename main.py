from flask import Flask
from schemas.all_db import initialize_database
from flask_cors import CORS

from routes.login import login

from email_otp_generation import send_otp_route, verify_otp_route

from routes.department import create_department, get_departments, update_department, delete_department
from routes.basic_info_form import create_basic_info, get_basic_info, update_basic_info, delete_basic_info
from routes.company import create_company, get_company, update_company, delete_company
from routes.location_form import create_location, get_location, update_location, delete_location
from routes.profile_form import create_profile, get_profile, update_profile, delete_profile
from routes.registration_form import create_user as create_registration_user, get_user as get_registration_user, update_user as update_registration_user, delete_user as delete_registration_user
from routes.team_form import create_team, get_team, update_team, delete_team
from routes.team_user_form import create_user as create_team_user, get_user as get_team_user, update_user as update_team_user, delete_user as delete_team_user

app = Flask(__name__)
CORS(app)


# department info form 
app.route('/create_department', methods=['POST'], endpoint='create_department')(create_department)
app.route('/departments', methods=['GET'], endpoint='departments')(get_departments)
app.route('/update_department', methods=['PUT'], endpoint='update_department')(update_department)
app.route('/delete_department', methods=['DELETE'], endpoint='delete_department')(delete_department)

# basic info form 
app.route('/create_basic_info', methods=['POST'], endpoint='create_basic_info')(create_basic_info)
app.route('/get_basic_info', methods=['GET'], endpoint='get_basic_info')(get_basic_info)
app.route('/update_basic_info', methods=['PUT'], endpoint='update_basic_info')(update_basic_info)
app.route('/delete_basic_info', methods=['DELETE'], endpoint='delete_basic_info')(delete_basic_info)

# company
app.route('/create_company', methods=['POST'], endpoint='create_company')(create_company)
app.route('/get_company', methods=['GET'], endpoint='get_company')(get_company)
app.route('/update_company', methods=['PUT'], endpoint='update_company')(update_company)
app.route('/delete_company', methods=['DELETE'], endpoint='delete_company')(delete_company)

# location
app.route('/create_location', methods=['POST'], endpoint='create_location')(create_location)
app.route('/get_location', methods=['GET'], endpoint='get_location')(get_location)
app.route('/update_location', methods=['PUT'], endpoint='update_location')(update_location)
app.route('/delete_location', methods=['DELETE'], endpoint='delete_location')(delete_location)

# profile form
app.route('/create_profile', methods=['POST'], endpoint='create_profile')(create_profile)
app.route('/get_profile', methods=['GET'], endpoint='get_profile')(get_profile)
app.route('/update_profile', methods=['PUT'], endpoint='update_profile')(update_profile)
app.route('/delete_profile', methods=['DELETE'], endpoint='delete_profile')(delete_profile)

# team form
app.route('/create_team', methods=['POST'], endpoint='create_team')(create_team)
app.route('/get_team', methods=['GET'], endpoint='get_team')(get_team)
app.route('/update_team', methods=['PUT'], endpoint='update_team')(update_team)
app.route('/delete_team', methods=['DELETE'], endpoint='delete_team')(delete_team)

# registration form CRUD operations
app.route('/create_registration_user', methods=['POST'], endpoint='create_registration_user')(create_registration_user)
app.route('/get_registration_user', methods=['GET'], endpoint='get_registration_user')(get_registration_user)
app.route('/update_registration_user', methods=['PUT'], endpoint='update_registration_user')(update_registration_user)
app.route('/delete_registration_user', methods=['DELETE'], endpoint='delete_registration_user')(delete_registration_user)

# team user form CRUD operations
app.route('/create_team_user', methods=['POST'], endpoint='create_team_user')(create_team_user)
app.route('/get_team_user', methods=['GET'], endpoint='get_team_user')(get_team_user)
app.route('/update_team_user', methods=['PUT'], endpoint='update_team_user')(update_team_user)
app.route('/delete_team_user', methods=['DELETE'], endpoint='delete_team_user')(delete_team_user)

# login 
app.route('/login', methods=['POST'], endpoint='login')(login)

# email OTP generation
app.route('/send-otp', methods=['POST'], endpoint='send_otp')(send_otp_route)
app.route('/verify-otp', methods=['POST'], endpoint='verify_otp')(verify_otp_route)

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
