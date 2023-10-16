# Import all required directries
from datetime import datetime

# Setting up few variables
today = datetime.today().date()

# ------------------------------------------------------------
# insert the collected item data into the database table
def add_item(expiry_date, cursor, front_image_path, back_image_path):
    # cursor.execute('''SELECT * FROM items WHERE expiry_date > date('now', '-7 days') and is_notified = 0  and is_expired = 0;''')
    # expired_items = cursor.fetchall()
    # for item in expired_items:
    #     print(item)
    userid = 1
    cursor.execute('''INSERT INTO items (user_id, front_image_path, back_image_path, expiry_date, created_date, last_modified_date, is_notified, is_expired, is_removed, is_archived)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (
                        userid,
                        front_image_path,
                        back_image_path,
                        expiry_date,
                        today,  # created_date_value
                        today,  # updated_date_value
                        0,      # is_notified
                        0,      # is_expired
                        0,      # is_removed
                        0))     # is_archived
    print('Item added into the items table.')

# def add_item(expiry_date, cursor, front_image_path, back_image_path):
#     cursor.execute('''INSERT INTO items (
#                         created_date, expiry_date, updated_date, image_path, item_state, is_expired, is_removed, is_notified) 
#                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
#                        (today,  # created_date_value
#                         expiry_date,
#                         today,  # updated_date_value
#                         front_image_path,
#                         'Fresh',
#                         0,      # is_expired
#                         0,      # is_removed
#                         0))     # is_deleted
#     print('Item added into the items table.')    

# ------------------------------------------------------------ SELECT
def get_items_expiring_today(cursor, user_id):
    cursor.execute('''SELECT back_image_path, expiry_date, created_date, id FROM items WHERE expiry_date = date('now') and ?;''', user_id)
    return cursor.fetchall()

def get_items_expiring_in_next_7_days(cursor):
    cursor.execute('''SELECT * FROM items WHERE expiry_date > date('now', '-7 days') and is_notified = 0  and is_expired = 0;''')
    return cursor.fetchall()

def get_all_unexpired_items(cursor):
    cursor.execute('''SELECT * FROM items WHERE expiry_date > date('now', '-7 days') and is_notified = 0  and is_expired = 0;''')
    return cursor.fetchall()

def get_all_items(cursor):
    cursor.execute('''SELECT back_image_path, expiry_date, created_date, id  FROM items;''')
    return cursor.fetchall()

def get_item_id(cursor, back_image_path):
    print('Entered into Get Item ID')
    cursor.execute('''SELECT id FROM items where back_image_path = ? LIMIT 1;''', (back_image_path,))
    get_item_id_value = cursor.fetchone()  # Use fetchone() to get a single result
    print('got item id', get_item_id_value)
    return get_item_id_value

def get_expired_items(cursor):
    cursor.execute('''SELECT id FROM items WHERE is_expired = 1  and is_removed = 0;''')
    return cursor.fetchall()

def get_item_details(cursor, item_id):
    cursor.execute('''SELECT expiry_date FROM items WHERE id =?''', (item_id,))
    expiry_date = cursor.fetchall()
    print('Item s expiry date is ',expiry_date)
    return expiry_date

# ------------------------------------------------------------ UPDATE
def set_item_removed(cursor, item_id):
    cursor.execute('''UPDATE items SET is_removed = 1 WHERE id =?''', (item_id,))
    print('Item ',item_id,' has been removed.')

def set_item_notified(cursor, item_id):
    cursor.execute('''UPDATE items SET is_notified = 1 WHERE id =?''', (item_id,))
    print('Item ',item_id,' has been notified.')

def delete_removed_items(cursor):
    cursor.execute('''DELETE FROM items WHERE is_removed = 1;''')
    print('Removed Flaged items are delete from the database.')
# ------------------------------------------------------------
# needs to scheduled 
def set_item_expired(cursor):
    cursor.execute('''UPDATE items SET is_expired = 1 WHERE expiry_date < date('now');''')
    print('Is Expired Flag has been updated for items')