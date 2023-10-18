from flask import Flask, request, jsonify
import os
from dbFunctionsItem import db_get_items_expiring_in_next_7_days, db_get_items_expiring_today
import sqlite3
from datetime import datetime

app = Flask(__name__)
# Define the directory where the images will be stored
UPLOAD_FOLDER = 'item_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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

# -----------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)