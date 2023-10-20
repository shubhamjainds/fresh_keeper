# Import all required directries
from datetime import datetime

# Setting up few variables
today = datetime.today().date()

# ------------------------------------------------------------ INSERT
# insert the collected item data into the database table
def add_item(cursor, user_id, front_image_path, back_image_path, expiry_date):
    cursor.execute('''INSERT INTO items (user_id, front_image_path, back_image_path, expiry_date, created_date, last_modified_date, is_notified, is_expired, is_removed, is_archived)
        VALUES (?, ?, ?, ?, ?, ?, 0, 0, 0, 0)''',
                       (
                        user_id,
                        front_image_path,
                        back_image_path,
                        expiry_date,
                        today,  # created_date_value
                        today   # updated_date_value
                        ))     
    print('Item added into the items table.')

# ------------------------------------------------------------ SELECT
def db_get_item_id(cursor, back_image_path):
    print('Entered into Get Item ID')
    cursor.execute('''SELECT id FROM items where back_image_path = ? LIMIT 1;''', (back_image_path,))
    get_item_id_value = cursor.fetchone()[0]  # Use fetchone() to get a single result
    print('got item id', get_item_id_value)
    return get_item_id_value

def db_get_items_expiring_today(cursor, user_id):
    cursor.execute('''SELECT front_image_path, back_image_path, expiry_date, created_date, id FROM items WHERE expiry_date = date('now') and is_removed = 0 and user_id =?;''', (user_id,))
    return cursor.fetchall()

def db_get_items_expiring_in_next_7_days(cursor, user_id):
    cursor.execute('''SELECT front_image_path, back_image_path, expiry_date, created_date, id FROM items WHERE expiry_date > date('now', '-7 days') and is_removed = 0 and user_id =?;''', (user_id,))
    return cursor.fetchall()

def get_all_unexpired_items(cursor):
    cursor.execute('''SELECT * FROM items WHERE expiry_date > date('now', '-7 days') and is_notified = 0  and is_expired = 0;''')
    return cursor.fetchall()

def get_all_items(cursor):
    cursor.execute('''SELECT CASE WHEN front_image_path IS NULL THEN back_image_path ELSE front_image_path END AS front_image_path, expiry_date, created_date, id FROM items;''')
    return cursor.fetchall()

def get_expired_items(cursor):
    cursor.execute('''SELECT id FROM items WHERE is_expired = 1  and is_removed = 0;''')
    return cursor.fetchall()

def get_item_details(cursor, item_id):
    cursor.execute('''SELECT expiry_date FROM items WHERE id =?''', (item_id,))
    expiry_date = cursor.fetchall()
    print('Item s expiry date is ',expiry_date)
    return expiry_date


# ------------------------------------------------------------ UPDATE
def db_set_expiry_date(cursor, user_id, item_id, expiry_date):
    cursor.execute('''UPDATE items SET expiry_date = ? WHERE id =? and user_id = ?''', (expiry_date, item_id, user_id,))
    print('Item ',item_id,' has been updated with expiry_date as ?.', (item_id, expiry_date,))

def db_set_item_removed(cursor, item_id):
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