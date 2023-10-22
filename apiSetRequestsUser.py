
import os
from dbFunctionsItem import db_set_expiry_date, db_set_item_removed
from dbFuntionsUser import db_check_email_availability, db_check_phone_number_availability, db_create_user, db_get_user_id_from_email_address
import sqlite3
from datetime import datetime

# ----------------------------------------------------------------- create_user_account
def create_user_account(first_name, last_name, email_address, phone_number, password):
    print('Enter into API create_user_account.')
    with sqlite3.connect('fresh_keeper') as conn:
                cursor = conn.cursor()
    print('Calling db_create_user')
    db_create_user(cursor, first_name, last_name, email_address, phone_number, password)
    conn.commit()
    conn.close()  
    with sqlite3.connect('fresh_keeper') as conn:
                cursor = conn.cursor()
    print('Calling db_get_user_id_from_email_address')
    try:
        user_id = db_get_user_id_from_email_address(cursor, email_address)
    except:
        print('Something went wrong with db_get_user_id_from_email_address')
    conn.commit()
    conn.close()  
    return user_id


# -----------------------------------------------------------------

