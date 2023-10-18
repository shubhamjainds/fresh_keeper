from flask import Flask, request, jsonify
import os
from dbFunctionsItem import db_get_items_expiring_today, get_all_items, get_item_details
from imageProcessing import get_image, get_image_base64, scan_image_and_get_expiry_date
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
def get_items_expiring_today():
    print('Entered into the get_items_expiring_today API.')
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
    conn.commit() # Commit the changes
    conn.close() # Close the connection   
    return jsonify({"items": items_expiring_today}), 200


# -----------------------------------------------------------------
# -----------------------------------------------------------------   send image path and expiry date of all item
@app.route('/api/get_all_items', methods=['GET'])
def send_all_item_data():
    print('Entered into the get_all_items API.')
    user_id = request.args.get('id')
    print('user_id', user_id, 'has been collected.')
    with sqlite3.connect('fresh_keeper') as conn:       # Connect to or create a new database
        cursor = conn.cursor()                          # Create a cursor object to execute SQL queries
    print('Going to Call function to get all items')
    data = get_all_items(cursor)
    items = []
    for row in data:        # Iterate through the data and replace front_image_path with actual image data
        back_image_path, expiry_date, created_date, id = row
        updated_row = {
                    'expiry_date': expiry_date,
                    'created_date': created_date,
                    'back_image_path': back_image_path[1:],
                    'item_id': id
        }
        items.append(updated_row)
    print('1',items)
    conn.commit() # Commit the changes
    conn.close() # Close the connection   
    print(expiry_date)
    return jsonify({"items": items}), 200


# -----------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)