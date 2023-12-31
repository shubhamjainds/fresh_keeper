# Import all required directries
from datetime import date
from email.utils import formatdate
import sqlite3
from dbFuntionsUser import db_check_email_availability, db_check_phone_number_availability, db_create_user, db_delete_user, db_reset_password
from imageProcessing import scan_image_and_get_expiry_date
from dbFunctionsItem import db_get_items_expiring_in_next_7_days, db_get_items_expiring_today, get_expired_items, set_item_notified
from textprocessing import get_dates

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


# # ------------------------------db_get_items_expiring_today
# user_id = 1
# data = db_get_items_expiring_today(cursor, user_id)
# for item in data:
#      print(item)

# ------------------------------db_get_items_expiring_in_next_7_days
# user_id = 1
# data = db_get_items_expiring_in_next_7_days(cursor, user_id)
# for item in data:
#      print(item)

# ------------------------------db_create_user
# db_create_user(cursor, 'Sakshi', 'Jain', 'defdsdasf@gmail.com', '1234567890', 'newpassword')

# today = date.today()
# formatted_date = today.strftime("%Y-%m-%d")

# print(formatted_date)
# ------------------------------db_delete_user
# user_id = '3'
# db_delete_user(cursor, user_id)

# ------------------------------email address availability
# email_address = 'shubhamdpj@gmail.com'
# status = db_check_email_availability(cursor, email_address)
# print(status)

# ------------------------------ phone number availability

# phone_number = 123456789
# status = db_check_phone_number_availability(cursor, phone_number)
# print(status)


# user_id = db_login_check(cursor, 'def@gmail.com', 'newpassword')
# print(user_id)

# -------------------------------RESET PASSWORD
email_address= 'shubham17398@gmail.com'
password = '2345'
userid = db_reset_password(cursor, email_address, password)
print('final ', userid)

# ------------------------------

conn.commit() # Commit the changes
conn.close() # Close the connection

# --------------------------------------