import random
import sqlite3
import os
from flask import Flask, request, jsonify
from SMTP import SMTP_send_email
from datetime import datetime
from apiSetRequestsItem import set_front_and_back_image
from apiSetRequestsUser import create_user_account
from dbFunctionsItem import db_get_all_items_unremoved, db_get_items_expiring_in_next_7_days, db_get_items_expiring_today, db_set_expiry_date, db_set_item_removed, get_item_details
from dbFuntionsUser import db_check_email_availability, db_check_phone_number_availability, db_login_check_credential, db_reset_password
from imageProcessing import scan_image_and_get_expiry_date

app = Flask(__name__)

# Define the directory where the images will be stored
UPLOAD_FOLDER = './item_images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# ===================================================================================================================Items
# ======================================================================================================Items-GET
# -----------------------------------------------------------------   get items expiring today
@app.route('/api/get_items_expiring_today', methods=['GET'])
def api_get_items_expiring_today():
    print('Entered into the api_get_items_expiring_today API.')
    user_id = request.args.get('id')
    print('user_id', user_id, 'has been collected.')
    with sqlite3.connect('fresh_keeper') as conn:
        cursor = conn.cursor()
    print('[',user_id,']','Going to Call function db_get_items_expiring_today')
    data_items_expiring_today = db_get_items_expiring_today(cursor, user_id)
    print('[',user_id,']','Returned from function db_get_items_expiring_today')
    # print(data_items_expiring_today)
    items_expiring_today = []
    for row in data_items_expiring_today:
        front_image_path, back_image_path, expiry_date, created_date, id = row
        updated_row = {
                    'front_image_path': front_image_path[1:],
                    'back_image_path': back_image_path,
                    'expiry_date': expiry_date,
                    'created_date': created_date,
                    'item_id': id
        }
        items_expiring_today.append(updated_row)
    # print('[',user_id,']','items_expiring_today: ',items_expiring_today)
    print('[',user_id,']','Returning from db_get_items_expiring_today API.')
    conn.commit()
    conn.close()
    return jsonify({"items": items_expiring_today}), 200


# -----------------------------------------------------------------
@app.route('/api/get_items_expiring_in_next_7_days', methods=['GET'])
def api_get_items_expiring_in_next_7_days():
    print('Entered into the api_get_items_expiring_in_next_7_days API.')
    user_id = request.args.get('id')
    print('user_id', user_id, 'has been collected.')
    with sqlite3.connect('fresh_keeper') as conn:
        cursor = conn.cursor()
    print('[',user_id,']','Going to Call function db_get_items_expiring_in_next_7_days')
    data_items_expiring_in_next_7_days = db_get_items_expiring_in_next_7_days(cursor, user_id)
    print('[',user_id,']','Returned from function db_get_items_expiring_in_next_7_days')
    # print(data_items_expiring_in_next_7_days)
    items_expiring_in_next_7_days = []
    for row in data_items_expiring_in_next_7_days:
        front_image_path, back_image_path, expiry_date, created_date, id = row
        updated_row = {
                    'front_image_path': front_image_path[1:],
                    'back_image_path': back_image_path,
                    'expiry_date': expiry_date,
                    'created_date': created_date,
                    'item_id': id
        }
        items_expiring_in_next_7_days.append(updated_row)
    # print('[',user_id,']','data_items_expiring_in_next_7_days: ',items_expiring_in_next_7_days)
    print('[',user_id,']','Returning from api_get_items_expiring_in_next_7_days API.')
    conn.commit()
    conn.close()
    return jsonify({"items": items_expiring_in_next_7_days}), 200
# -----------------------------------------------------------------   get all items unremoved
@app.route('/api/get_all_items_unremoved', methods=['GET'])
def api_get_all_items_unremoved():
    print('Entered into the api_get_all_items_unremoved API.')
    user_id = request.args.get('id')
    print('user_id', user_id, 'has been collected.')
    with sqlite3.connect('fresh_keeper') as conn:
        cursor = conn.cursor()
    print('[',user_id,']','Going to Call function db_get_all_items_unremoved')
    data_all_items_unremoved = db_get_all_items_unremoved(cursor, user_id)
    print('[',user_id,']','Returned from function db_get_all_items_unremoved')
    # print(data_all_items_unremoved)
    all_items_unremoved = []
    for row in data_all_items_unremoved:
        front_image_path, back_image_path, expiry_date, created_date, id = row
        updated_row = {
                    'front_image_path': front_image_path[1:],
                    'back_image_path': back_image_path,
                    'expiry_date': expiry_date,
                    'created_date': created_date,
                    'item_id': id
        }
        all_items_unremoved.append(updated_row)
    # print('[',user_id,']','all_items_unremoved: ',all_items_unremoved)
    print('[',user_id,']','Returning from api_get_all_items_unremoved API.')
    conn.commit()
    conn.close()
    return jsonify({"items": all_items_unremoved}), 200


# ======================================================================================================Items-SET
# ----------------------------------------------------------------- Get image and send expiry date
@app.route('/api/set_front_and_back_image', methods=['POST'])
def api_set_front_and_back_image():
    print('Enter into API front_and_back_image.')
    if 'fileFront' not in request.files:
        return jsonify({"error": "No file part"}), 400
    front_image_file = request.files['fileFront']
    back_image_file = request.files['fileBack']
    user_id = request.args.get('userId')
    print('[',user_id,']','Parameters Recieved.', user_id)
    return_obj = set_front_and_back_image(front_image_file, back_image_file, user_id)
    if return_obj == "Error":
        return jsonify({"message": "Error"}), 201
    else:
        return jsonify({"message": return_obj}), 201
# ----------------------------------------------------------------- Update the expiry date of item
@app.route('/api/set_expiry_date', methods=['POST'])
def api_set_expiry_date():
    print('Enter into api_set_expiry_date.')
    user_id = request.args.get('id')
    print('user_id', user_id, 'has been collected.')
    item_id = request.form.get('itemId')
    print('[',user_id,']','item_id', item_id, 'has been collected.')
    expiry_date = request.form.get('expiryDate')
    print('[',user_id,']','expiry_date', expiry_date, 'has been collected.')  
    with sqlite3.connect('fresh_keeper') as conn:
        cursor = conn.cursor()
    print('[',user_id,']','Calling function db_set_expiry_date.')
    try:
        db_set_expiry_date(cursor, user_id, item_id, expiry_date)
        print('[',user_id,']','Returned from function db_set_expiry_date.')
        conn.commit()
        conn.close()
        return jsonify({"Status": "Success"}), 200 
    except:
        return jsonify({"Status": "Failed"}), 200 
# ----------------------------------------------------------------- Remove the item from the lists
@app.route('/api/set_item_removed', methods=['POST'])
def api_set_item_removed():
    print('Enter into set_item_removed.')
    user_id = request.form.get('userId')
    print('user_id', user_id, 'has been collected.')
    item_id = request.form.get('itemId')
    print('[',user_id,']','item_id', item_id, 'has been collected.')
    with sqlite3.connect('fresh_keeper') as conn:
        cursor = conn.cursor()
    print('[',user_id,']','Calling function db_set_item_removed.')
    try:
        db_set_item_removed(cursor, user_id, item_id)
        print('[',user_id,']','Returned from function db_set_item_removed.')
        conn.commit()
        conn.close()
        return jsonify({"Status": "Success"}), 200 
    except:
        return jsonify({"Status": "Failed"}), 200 
# ===================================================================================================================User
# ======================================================================================================User-GET
# ----------------------------------------------------------------- get_and_send_email_passcode
@app.route('/api/get_and_send_email_passcode', methods=['POST'])
def api_get_and_send_email_passcode():
    print('Enter into API get_and_send_email_passcode.')
    email_address = request.args.get('emailAddress')
    passcode = random.randint(1000, 9999)
    print('Passcode: ', passcode, 'for', email_address)
    subject = 'Verification Code for Fresh Keeper'
    body = 'Your verification code is: ' + str(passcode) + '.'
    print('Calling SMTP_send_email')
    SMTP_send_email(email_address, subject, body)
    print('Returned form SMTP_send_email')
    return jsonify({"passcode": passcode}), 200 
# ----------------------------------------------------------------- check_email_address_availability
@app.route('/api/check_email_address_availability', methods=['POST'])
def api_check_email_address_availability():
    print('Enter into API check_email_address_availability.')
    with sqlite3.connect('fresh_keeper') as conn:
                cursor = conn.cursor()
    email_address = request.args.get('emailAddress')
    print('Parameters Recieved.', email_address)
    print('Calling db_check_email_availability')
    db_check_email_availability_value = db_check_email_availability(cursor, email_address)
    print('Return from db_check_email_availability with value: ', db_check_email_availability_value)
    conn.commit()
    conn.close()  
    return jsonify({"isEmailAddress": db_check_email_availability_value}), 200 

# ----------------------------------------------------------------- check_email_address_availability
@app.route('/api/check_phone_number_availability', methods=['GET'])
def api_check_phone_number_availability():
    print('Enter into API check_phone_number_availability.')
    with sqlite3.connect('fresh_keeper') as conn:
                cursor = conn.cursor()
    phone_number = request.args.get('phoneNumber')
    print('Parameters Recieved.', phone_number)
    print('Calling db_phone_number_availability')
    db_check_phone_number_availability_value = db_check_phone_number_availability(cursor, phone_number)
    print('Return from db_check_email_availability with value: ', db_check_phone_number_availability_value)
    conn.commit()
    conn.close()  
    return jsonify({"isPhoneNumber": db_check_phone_number_availability_value}), 200 

# ----------------------------------------------------------------- login check
@app.route('/api/check_login_credential', methods=['POST'])
def api_check_login_credential():
    print('Enter into API check_login_credential.')
    with sqlite3.connect('fresh_keeper') as conn:
                cursor = conn.cursor()
    email_address = request.form.get('emailAddress')
    password = request.form.get('password')
    print('Parameters Recieved.', email_address, password)
    try:
        user_id = db_login_check_credential(cursor, email_address, password)
        print('Return from db_check_email_availability with value: ', user_id)
        user_available_flag = True
    except:
        user_id = 0
        user_available_flag = False
    return_obj = {
                    'userId': user_id,
                    'isUser': user_available_flag
        }
    conn.commit()
    conn.close()  
    return jsonify({"result": return_obj}), 200 
# ======================================================================================================User-SET
# ----------------------------------------------------------------- create_user_account
@app.route('/api/create_user_account', methods=['POST'])
def api_create_user_account():
    print('Enter into API create_user_account.')
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    email_address = request.form.get('emailAddress')
    phone_number = request.form.get('phoneNumber')
    password = request.form.get('password')
    print('Parameters Recieved.', first_name, last_name, email_address, phone_number, password)
    user_id = create_user_account(first_name, last_name, email_address, phone_number, password)
    print('User ID: ', user_id)
    return jsonify({"userId": user_id}), 200 

# ----------------------------------------------------------------- reset password
@app.route('/api/reset_password', methods=['POST'])
def api_reset_password():
    print('Enter into API reset_password.')
    email_address = request.form.get('emailAddress')
    password = request.form.get('password')
    print('Parameters Recieved.', email_address, password)
    with sqlite3.connect('fresh_keeper') as conn:
                cursor = conn.cursor()
    print('Calling db_reset_password')
    user_id = db_reset_password(cursor, email_address, password)
    print('Returning from  API reset_password with', user_id)
    return jsonify({"userId": user_id}), 200 








# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------




# -----------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


