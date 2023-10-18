from flask import Flask, request, jsonify
import os
from dbFunctionsItem import db_set_expiry_date, db_set_item_removed
from dbFuntionsUser import db_check_email_availability, db_check_phone_number_availability, db_create_user, db_get_user_id_from_email_address
import sqlite3
from datetime import datetime
app = Flask(__name__)

# Define the directory where the images will be stored
UPLOAD_FOLDER = './item_images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# ----------------------------------------------------------------- create_user_account
@app.route('/api/create_user_account', methods=['POST'])
def api_create_user_account():
    print('Enter into API front_and_back_image.')
    with sqlite3.connect('fresh_keeper') as conn:
                cursor = conn.cursor()
    first_name = request.args.get('firstName')
    last_name = request.args.get('lastName')
    email_address = request.args.get('emailAddress')
    phone_number = request.args.get('phoneNumber')
    password = request.args.get('password')
    print('Parameters Recieved.', first_name, last_name, email_address, phone_number, password)
    print('Calling db_check_email_availability')
    if not db_check_email_availability(cursor, email_address):
        conn.commit()
        conn.close()  
        return jsonify({"Status": "Email address already used"}), 201 
    print('Calling db_check_phone_number_availability')
    if not db_check_phone_number_availability(cursor, phone_number):
        conn.commit()
        conn.close()  
        return jsonify({"Status": "Phone number already used."}), 201 
    print('Calling db_create_user')
    db_create_user(cursor, first_name, last_name, email_address, phone_number, password)
    print('Calling db_get_user_id_from_email_address')
    user_id = db_get_user_id_from_email_address(cursor, email_address)
    conn.commit()
    conn.close()  
    return jsonify({"user id": user_id}), 200 


# -----------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
