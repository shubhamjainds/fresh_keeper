from flask import Flask, request, jsonify
import os
from dbFunctions import db_set_expiry_date
from imageProcessing import scan_image_and_get_expiry_date
import sqlite3
from datetime import datetime
app = Flask(__name__)

# Define the directory where the images will be stored
UPLOAD_FOLDER = './item_images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# ----------------------------------------------------------------- Get image and send expiry date
@app.route('/api/set_front_and_back_image', methods=['POST'])
def api_set_front_and_back_image():
    print('Enter into API front_and_back_image.')
    if 'fileFront' not in request.files:
        return jsonify({"error": "No file part"}), 400
    front_image_file = request.files['fileFront']
    print('Front image recieved.')
    back_image_file = request.files['fileBack']
    print('Back image recieved.')
    user_id = request.args.get('userId')
    print('Userid Recieved.')
    if back_image_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if back_image_file:
        current_timestamp = str(datetime.timestamp(datetime.now()))
        front_image_path = UPLOAD_FOLDER + user_id + '_' + current_timestamp + '_front' + '.jpeg'
        front_image_file.save(front_image_path)
        print(front_image_path)
        back_image_path = UPLOAD_FOLDER + user_id + '_' + current_timestamp + '_back' + '.jpeg'
        back_image_file.save(back_image_path)
        print(back_image_path)
        try:
            with sqlite3.connect('fresh_keeper') as conn:
                cursor = conn.cursor()
            print('Calling function scan_image_and_get_expiry_date')
            expiry_date, item_id = scan_image_and_get_expiry_date(cursor, user_id, front_image_path, back_image_path)
            print('Returned from function scan_image_and_get_expiry_date')
            print(item_id)
            print(expiry_date)
            return_obj ={
                'expiry_date': expiry_date,
                'item_id': item_id,
            }
            conn.commit()
            return jsonify({"message": return_obj}), 201   
        except Exception as e:
            print(f"An error occurred: {e}")
            # conn.rollback()  # Roll back the transaction in case of an error
        finally:           
            conn.close()  

# ----------------------------------------------------------------- Get image and send expiry date
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
    print('Going to Call function db_set_expiry_date.')
    db_set_expiry_date(cursor, user_id, item_id, expiry_date)
    print('Returned from function db_set_expiry_date.')
    conn.commit()
    conn.close()
    return jsonify({"items": "Success"}), 200 

# -----------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


