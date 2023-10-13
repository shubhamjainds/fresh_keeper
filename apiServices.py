from flask import Flask, request, jsonify
import os
from dbFunctions import get_item_details
from imageProcessing import scan_image_and_get_expiry_date
import sqlite3
from datetime import datetime

# with sqlite3.connect('fresh_keeper') as conn: # Connect to or create a new database
#     cursor = conn.cursor() # Create a cursor object to execute SQL queries

app = Flask(__name__)



# Define the directory where the images will be stored
UPLOAD_FOLDER = 'item_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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

# -----------------------------------------------------------------   send image and expiry date of one item
@app.route('/api/get_item_information', methods=['GET'])
def send_data():
    print('Entered into the get_item_information API.')
    user_id = request.args.get('id')
    print('user_id', user_id, 'has been collected.')
    with sqlite3.connect('fresh_keeper') as conn:       # Connect to or create a new database
        cursor = conn.cursor()                          # Create a cursor object to execute SQL queries
    print('Going to Call function')
    expiry_date = get_item_details(cursor, user_id)
    print('1',expiry_date)
    conn.commit() # Commit the changes

    conn.close() # Close the connection   
    print(expiry_date)
    return jsonify({"message": expiry_date}), 201
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

# -----------------------------------------------------------------
