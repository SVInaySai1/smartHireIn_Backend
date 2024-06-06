from schemas.basic_info_form_db import initialize_database_basic
from schemas.registration_form_db import initialize_database_registration
from schemas.company_db import initialize_database_company
from schemas.location_form_db import initialize_database_location
from schemas.profile_form_db import initialize_database_profile
from schemas.team_form_db import initialize_database_team
from schemas.user_form_db import initialize_database_user_form


def initialize_database():
    initialize_database_basic()
    initialize_database_registration()
    initialize_database_company()
    initialize_database_location()
    initialize_database_profile()
    initialize_database_team()
    initialize_database_user_form()