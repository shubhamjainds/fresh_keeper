# Import all required directries
import sqlite3
from imageProcessing import scan_image_and_get_expiry_date
from dbFunctions import db_get_items_expiring_in_next_7_days, db_get_items_expiring_today, get_expired_items, set_item_notified, set_item_removed

with sqlite3.connect('fresh_keeper') as conn: # Connect to or create a new database
    cursor = conn.cursor() # Create a cursor object to execute SQL queries

# ------------------------------image processing
# front_image_path = None
# back_image_path = './item_images/k2.jpeg'

# Expiry_date = scan_image_and_get_expiry_date(front_image_path, back_image_path, cursor)

# if not Expiry_date:
#         print("Sorry, we could not found any date in the image. Please enter the Expiry date manually.")
# else: 
#     print("Expiry Date: ", Expiry_date)


# ------------------------------db_get_items_expiring_today
# user_id = 1
# data = db_get_items_expiring_today(cursor, user_id)
# for item in data:
#      print(item)

# ------------------------------db_get_items_expiring_in_next_7_days
# user_id = 1
# data = db_get_items_expiring_in_next_7_days(cursor, user_id)
# for item in data:
#      print(item)

# ------------------------------

conn.commit() # Commit the changes
conn.close() # Close the connection

# --------------------------------------