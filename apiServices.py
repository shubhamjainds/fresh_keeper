import random
from flask import Flask, request, jsonify
import os
from SMTP import SMTP_send_email
from apiSetRequestsItem import set_front_and_back_image
from apiSetRequestsUser import create_user_account
from dbFunctionsItem import db_get_items_expiring_in_next_7_days, db_get_items_expiring_today, db_set_expiry_date, db_set_item_removed, get_item_details
from dbFuntionsUser import db_check_email_availability, db_check_phone_number_availability
from imageProcessing import scan_image_and_get_expiry_date
import sqlite3
from datetime import datetime
import time

app = Flask(__name__)

# Define the directory where the images will be stored
UPLOAD_FOLDER = './item_images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# ===================================================================================================================Items
# ======================================================================================================Items-GET
# -----------------------------------------------------------------   send image and expiry date of one item
@app.route('/api/get_items_expiring_today', methods=['GET'])
def api_get_items_expiring_today():
    print('Entered into the api_get_items_expiring_today API.')
    user_id = request.args.get('id')
    print('user_id', user_id, 'has been collected.')
    with sqlite3.connect('fresh_keeper') as conn:
        cursor = conn.cursor()
    print('Going to Call function db_get_items_expiring_today')
    data_items_expiring_today = db_get_items_expiring_today(cursor, user_id)
    print('Returned from function db_get_items_expiring_today')
    print(data_items_expiring_today)
    items_expiring_today = []
    for row in data_items_expiring_today:
        front_image_path, back_image_path, expiry_date, created_date, id = row
        updated_row = {
                    'front_image_path': front_image_path,
                    'back_image_path': back_image_path,
                    'expiry_date': expiry_date,
                    'created_date': created_date,
                    'item_id': id
        }
        items_expiring_today.append(updated_row)
    print('items_expiring_today: ',items_expiring_today)
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
    print('Going to Call function db_get_items_expiring_in_next_7_days')
    data_items_expiring_in_next_7_days = db_get_items_expiring_in_next_7_days(cursor, user_id)
    print('Returned from function db_get_items_expiring_in_next_7_days')
    print(data_items_expiring_in_next_7_days)
    items_expiring_in_next_7_days = []
    for row in data_items_expiring_in_next_7_days:
        front_image_path, back_image_path, expiry_date, created_date, id = row
        updated_row = {
                    'front_image_path': front_image_path,
                    'back_image_path': back_image_path,
                    'expiry_date': expiry_date,
                    'created_date': created_date,
                    'item_id': id
        }
        items_expiring_in_next_7_days.append(updated_row)
    print('data_items_expiring_in_next_7_days: ',items_expiring_in_next_7_days)
    conn.commit()
    conn.close()
    return jsonify({"items": items_expiring_in_next_7_days}), 200
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
    print('Parameters Recieved.', user_id)
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
    item_id = request.args.get('itemId')
    print('item_id', item_id, 'has been collected.')
    expiry_date = request.args.get('itemId')
    print('expiry_date', expiry_date, 'has been collected.')
    with sqlite3.connect('fresh_keeper') as conn:
        cursor = conn.cursor()
    print('Calling function db_set_expiry_date.')
    try:
        db_set_expiry_date(cursor, user_id, item_id, expiry_date)
        print('Returned from function db_set_expiry_date.')
        conn.commit()
        conn.close()
        return jsonify({"Status": "Success"}), 200 
    except:
        return jsonify({"Status": "Failed"}), 200 
# ----------------------------------------------------------------- Remove the item from the lists
@app.route('/api/set_item_removed', methods=['POST'])
def api_set_item_removed():
    print('Enter into set_item_removed.')
    user_id = request.args.get('id')
    print('user_id', user_id, 'has been collected.')
    item_id = request.args.get('itemId')
    print('item_id', item_id, 'has been collected.')
    with sqlite3.connect('fresh_keeper') as conn:
        cursor = conn.cursor()
    print('Calling function db_set_item_removed.')
    try:
        db_set_item_removed(cursor, user_id, item_id)
        print('Returned from function db_set_item_removed.')
        conn.commit()
        conn.close()
        return jsonify({"Status": "Success"}), 200 
    except:
        return jsonify({"Status": "Failed"}), 200 
# ===================================================================================================================User
# ======================================================================================================User-GET
# ----------------------------------------------------------------- get_and_send_email_passcode
@app.route('/api/get_and_send_email_passcode', methods=['GET'])
def api_get_and_send_email_passcode():
    print('Enter into API get_and_send_email_passcode.')
    email_address = request.args.get('emailAddress')
    passcode = random.randint(1000, 9999)
    print('Passcode: ', passcode, 'for', email_address)
    subject = 'Verification Code for Fresh Keeper'
    body = 'Your verification code is: ' + passcode + '.'
    print('Calling SMTP_send_email')
    SMTP_send_email(email_address, subject, body)
    print('Returned form SMTP_send_email')
    return jsonify({"passcode": passcode}), 200 
# ----------------------------------------------------------------- check_email_address_availability
@app.route('/api/check_email_address_availability', methods=['GET'])
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
# ======================================================================================================User-SET
# ----------------------------------------------------------------- create_user_account
@app.route('/api/create_user_account', methods=['POST'])
def api_create_user_account():
    print('Enter into API front_and_back_image.')
    first_name = request.args.get('firstName')
    last_name = request.args.get('lastName')
    email_address = request.args.get('emailAddress')
    phone_number = request.args.get('phoneNumber')
    password = request.args.get('password')
    print('Parameters Recieved.', first_name, last_name, email_address, phone_number, password)
    user_id = create_user_account(first_name, last_name, email_address, phone_number, password)
    print('User ID: ', user_id)
    return jsonify({"user id": user_id}), 200 








# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------





# =====================================================================================
# ----------------------------------------------------------------- Get image and send expiry date
@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    
    Expiry_date = ""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], (file.filename))
        file.save(filename)
        back_image_path = './item_images/image.jpeg'
        try:
            with sqlite3.connect('fresh_keeper') as conn: # Connect to or create a new database
                cursor = conn.cursor() # Create a cursor object to execute SQL queries
            front_image_path = None
            Expiry_date = scan_image_and_get_expiry_date(front_image_path, back_image_path, cursor)
            print('came back from scan_image_and_get_expiry_date')
            if not Expiry_date:
                conn.commit() # Commit the changes
                return jsonify({"message": "No result found"}), 201
            else:
                conn.commit() # Commit the changes
                return jsonify({"message": Expiry_date}), 201
            
        except Exception as e:
            print(f"An error occurred: {e}")
            # conn.rollback()  # Roll back the transaction in case of an error
        finally:           
            conn.close() # Close the connection   

# ----------------------------------------------------------------- Get image and send expiry date
@app.route('/api/front_and_back_image', methods=['POST'])
def api_front_and_back_image():
    print('Enter into API front_and_back_image')
    expiry_date = ""
    if 'fileFront' not in request.files:
        return jsonify({"error": "No file part"}), 400
    front_image_file = request.files['fileFront']
    print('got front')
    back_image_file = request.files['fileBack']
    print('got back')
    user_id = request.args.get('userId')
    print('got userid')
    if back_image_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if back_image_file:
        # filename = os.path.join(app.config['UPLOAD_FOLDER'], (back_image_file.filename))
        current_timestamp = str(datetime.timestamp(datetime.now()))
        front_image_path = UPLOAD_FOLDER + user_id + '_' + current_timestamp + '_front' + '.jpeg'
        front_image_file.save(front_image_path)
        print(front_image_path)
        back_image_path = UPLOAD_FOLDER + user_id + '_' + current_timestamp + '_back' + '.jpeg'
        back_image_file.save(back_image_path)
        print(back_image_path)
        
        try:
            with sqlite3.connect('fresh_keeper') as conn: # Connect to or create a new database
                cursor = conn.cursor() # Create a cursor object to execute SQL queries
            print('Going to call scan_image_and_get_expiry_date')
            expiry_date, item_id = scan_image_and_get_expiry_date(front_image_path, back_image_path, cursor)
            print('Came back from scan_image_and_get_expiry_date')
            print(item_id)
            print(expiry_date)
            print('the max date')
            return_obj ={
                'expiry_date': expiry_date,
                'item_id': item_id,
            }
            conn.commit() # Commit the changes
            return jsonify({"message": return_obj}), 201


            # if not Expiry_date:
            #     conn.commit() # Commit the changes
            #     return jsonify({"message": "No result found"}), 201
            # else:
            #     conn.commit() # Commit the changes
            #     return jsonify({"message": Expiry_date}), 201
            
        except Exception as e:
            print(f"An error occurred: {e}")
            # conn.rollback()  # Roll back the transaction in case of an error
        finally:           
            conn.close() # Close the connection   

# -----------------------------------------------------------------   send expiry date of one item
@app.route('/api/get_data', methods=['GET'])
def send_data():
    print('entered into the api')
    user_id = request.args.get('id')
    print('user_id has been collected')
    print(user_id)
    with sqlite3.connect('fresh_keeper') as conn: # Connect to or create a new database
        cursor = conn.cursor() # Create a cursor object to execute SQL queries
    print('going to call the get_item_details function')
    expiry_date = get_item_details(cursor, user_id)
    print('1',expiry_date)
    conn.commit() # Commit the changes

    conn.close() # Close the connection   
    print(expiry_date)
    return jsonify({"message": expiry_date}), 201


# -----------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


