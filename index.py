# Import all required directries
import sqlite3
from imageProcessing import scan_image_and_get_expiry_date
from dbFunctions import get_items_expiring_in_next_7_days, get_items_expiring_today, get_expired_items, set_item_notified, set_item_removed

with sqlite3.connect('fresh_keeper') as conn: # Connect to or create a new database
    cursor = conn.cursor() # Create a cursor object to execute SQL queries

# ------------------------------image processing
front_image_path = None
back_image_path = './item_images/k2.jpeg'

Expiry_date = scan_image_and_get_expiry_date(front_image_path, back_image_path, cursor)

if not Expiry_date:
        print("Sorry, we could not found any date in the image. Please enter the Expiry date manually.")
else: 
    print("Expiry Date: ", Expiry_date)
# ------------------------------get data
# expired_items = get_items_expiring_in_next_7_days(cursor)
# for item in expired_items:
#     print(item)
# ------------------------------set data
# set_item_removed(cursor, 15)
# ------------------------------bar code reader
# Expiry_date = detect_barcode(image_path)
# ------------------------------

conn.commit() # Commit the changes
conn.close() # Close the connection

# --------------------------------------