from flask import Flask, request, jsonify
import os
from dbFunctionsItem import db_set_expiry_date, db_set_item_removed
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
def set_front_and_back_image(front_image_file, back_image_file, user_id):
    print('Enter into API front_and_back_image.')
    current_timestamp = str(datetime.timestamp(datetime.now()))
    front_image_path = UPLOAD_FOLDER + user_id + '_' + current_timestamp + '_front' + '.jpeg'
    front_image_file.save(front_image_path)
    back_image_path = UPLOAD_FOLDER + user_id + '_' + current_timestamp + '_back' + '.jpeg'
    back_image_file.save(back_image_path)
    with sqlite3.connect('fresh_keeper') as conn:
        cursor = conn.cursor()
    print('[',user_id,']','Calling function scan_image_and_get_expiry_date')
    try:
        expiry_date, item_id = scan_image_and_get_expiry_date(cursor, user_id, front_image_path, back_image_path)
        print('[',user_id,']','Returned from function scan_image_and_get_expiry_date with:', "item id: ", item_id, "expiry date: ", expiry_date)
        return_obj ={
            'expiry_date': expiry_date,
            'item_id': item_id,
        }
        conn.commit()
        conn.close()  
        return return_obj
    except: 
        return "Error"
    
# # ----------------------------------------------------------------- Update the expiry date of item
# @app.route('/api/set_expiry_date', methods=['POST'])
# def api_set_expiry_date():
#     print('Enter into api_set_expiry_date.')
#     user_id = request.args.get('id')
#     print('user_id', user_id, 'has been collected.')
#     item_id = request.args.get('itemId')
#     print('item_id', item_id, 'has been collected.')
#     expiry_date = request.args.get('itemId')
#     print('expiry_date', expiry_date, 'has been collected.')
#     with sqlite3.connect('fresh_keeper') as conn:
#         cursor = conn.cursor()
#     print('Calling function db_set_expiry_date.')
#     try:
#         db_set_expiry_date(cursor, user_id, item_id, expiry_date)
#         print('Returned from function db_set_expiry_date.')
#         conn.commit()
#         conn.close()
#         return jsonify({"Status": "Success"}), 200 
#     except:
#         return jsonify({"Status": "Failed"}), 200 

# # ----------------------------------------------------------------- Remove the item from the lists
# @app.route('/api/set_item_removed', methods=['POST'])
# def api_set_item_removed():
#     print('Enter into set_item_removed.')
#     user_id = request.args.get('id')
#     print('user_id', user_id, 'has been collected.')
#     item_id = request.args.get('itemId')
#     print('item_id', item_id, 'has been collected.')
#     with sqlite3.connect('fresh_keeper') as conn:
#         cursor = conn.cursor()
#     print('Calling function db_set_item_removed.')
#     try:
#         db_set_item_removed(cursor, user_id, item_id)
#         print('Returned from function db_set_item_removed.')
#         conn.commit()
#         conn.close()
#         return jsonify({"Status": "Success"}), 200 
#     except:
#         return jsonify({"Status": "Failed"}), 200 

# -----------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


