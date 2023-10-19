import random
from flask import Flask, request, jsonify
import os
from SMTP import SMTP_send_email
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

# ----------------------------------------------------------------- check_email_address_availability
# @app.route('/api/check_email_address_availability', methods=['GET'])
# def api_check_email_address_availability():
#     print('Enter into API check_email_address_availability.')
#     with sqlite3.connect('fresh_keeper') as conn:
#                 cursor = conn.cursor()
#     email_address = request.args.get('emailAddress')
#     print('Parameters Recieved.', email_address)
#     print('Calling db_check_email_availability')
#     db_check_email_availability_value = db_check_email_availability(cursor, email_address)
#     print('Return from db_check_email_availability with value: ', db_check_email_availability_value)
#     conn.commit()
#     conn.close()  
#     return jsonify({"isEmailAddress": db_check_email_availability_value}), 200 

# # ----------------------------------------------------------------- check_email_address_availability
# @app.route('/api/check_phone_number_availability', methods=['GET'])
# def api_check_phone_number_availability():
#     print('Enter into API check_phone_number_availability.')
#     with sqlite3.connect('fresh_keeper') as conn:
#                 cursor = conn.cursor()
#     phone_number = request.args.get('phoneNumber')
#     print('Parameters Recieved.', phone_number)
#     print('Calling db_phone_number_availability')
#     db_check_phone_number_availability_value = db_check_phone_number_availability(cursor, phone_number)
#     print('Return from db_check_email_availability with value: ', db_check_phone_number_availability_value)
#     conn.commit()
#     conn.close()  
#     return jsonify({"isPhoneNumber": db_check_phone_number_availability_value}), 200 

# # ----------------------------------------------------------------- get_and_send_email_passcode
# @app.route('/api/get_and_send_email_passcode', methods=['GET'])
# def api_get_and_send_email_passcode():
#     print('Enter into API get_and_send_email_passcode.')
#     email_address = request.args.get('emailAddress')
#     passcode = random.randint(1000, 9999)
#     print('Passcode: ', passcode, 'for', email_address)
#     subject = 'Verification Code for Fresh Keeper'
#     body = 'Your verification code is: ' + passcode + '.'
#     print('Calling SMTP_send_email')
#     SMTP_send_email(email_address, subject, body)
#     print('Returned form SMTP_send_email')
#     return jsonify({"passcode": passcode}), 200 

# -----------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
