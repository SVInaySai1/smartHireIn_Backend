from flask import Flask
from schemas.all_db import initialize_database
from flask_cors import CORS

from routes.login import login

from email_otp_generation import send_otp_route, verify_otp_route

from routes.basic_info_form import create_basic_info, get_basic_info, update_basic_info, delete_basic_info
from routes.company import create_company, get_company, update_company, delete_company
from routes.location_form import create_location, get_location, update_location, delete_location
from routes.profile_form import create_profile, get_profile, update_profile, delete_profile
from routes.registration_form import create_user, get_user, update_user, delete_user
from routes.team_form import create_team, get_team, update_team, delete_team
#from routes.user_form import create_user, get_user, update_user, delete_user


app = Flask(__name__)
CORS(app)

# basic info form 
app.route('/create_basic_info', methods=['POST'])(create_basic_info)
app.route('/get_basic_info', methods=['GET'])(get_basic_info)
app.route('/update_basic_info', methods=['PUT'])(update_basic_info)
app.route('/delete_basic_info', methods=['DELETE'])(delete_basic_info)

#company
app.route('/create_company', methods=['POST'])(create_company)
app.route('/get_company', methods=['GET'])(get_company)
app.route('/update_company', methods=['PUT'])(update_company)
app.route('/delete_company', methods=['DELETE'])(delete_company)

#location
app.route('/create_location', methods=['POST'])(create_location)
app.route('/get_location', methods=['GET'])(get_location)
app.route('/update_location', methods=['PUT'])(update_location)
app.route('/delete_location', methods=['DELETE'])(delete_location)

#profile form
app.route('/create_profile', methods=['POST'])(create_profile)
app.route('/get_profile', methods=['GET'])(get_profile)
app.route('/update_profile', methods=['PUT'])(update_profile)
app.route('/delete_profile', methods=['DELETE'])(delete_profile)

#team form
app.route('/create_team', methods=['POST'])(create_team)
app.route('/get_team', methods=['GET'])(get_team)
app.route('/update_team', methods=['PUT'])(update_team)
app.route('/delete_team', methods=['DELETE'])(delete_team)


#registration form crud operations
app.route('/create_user', methods=['POST'])(create_user)
app.route('/get_user', methods=['GET'])(get_user)
app.route('/update_user', methods=['PUT'])(update_user)
app.route('/delete_user', methods=['DELETE'])(delete_user)

# login 
app.route('/login', methods=['POST'])(login)


#email generation
app.route('/send-otp', methods=['POST'])(send_otp_route)
app.route('/verify-otp', methods=['POST'])(verify_otp_route)




if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
