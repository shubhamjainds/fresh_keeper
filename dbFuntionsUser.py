def db_create_user(cursor, first_name, last_name, email_address, phone_number, password):
    print('Entered into db_create_user')
    cursor.execute('''INSERT INTO users (First_name, Last_name, Email_address, Phone_number, password, is_email_verified, Is_phone_verified, All_notifications, Notify_expiring_7_days, Notify_expiring_today)
        VALUES (?, ?, ?, ?, ?, 1, 0, 1, 1, 1)''',
                        (
                        first_name,
                        last_name,
                        email_address,
                        phone_number,
                        password,
                        ))    
    print('User ',first_name, last_name, ' added into the users table.')

# ----------------------------------------
def db_login_check_credential(cursor, email_address, password):
    cursor.execute('''SELECT id FROM users WHERE email_address = ?  and password = ? LIMIT 1;''', (email_address, password))
    return cursor.fetchone()[0]

# ----------------------------------------
def db_delete_user(cursor, user_id):
    cursor.execute('''DELETE FROM users WHERE id = ?''',
                        (user_id))     
    print('User ID ',user_id, ' has been deleted.')

# ----------------------------------------
def db_check_email_availability(cursor, email_address):
    print('Entered into db_check_email_availability')
    cursor.execute('''SELECT COUNT(*) AS usercount FROM users where Email_address = ? LIMIT 1;''', (email_address,))
    user_count = cursor.fetchone()[0]  # Use fetchone() to get a single result
    print('User count: ', user_count)
    if user_count == 0:
        return True
    else:
        return False

# ----------------------------------------
def db_check_phone_number_availability(cursor, phone_number):
    print('Entered into db_check_phone_number_availability')
    cursor.execute('''SELECT COUNT(*) AS usercount FROM users where Phone_number = ? LIMIT 1;''', (phone_number,))
    user_count = cursor.fetchone()[0]  # Use fetchone() to get a single result
    print('User count: ', user_count)
    if user_count == 0:
        return True
    else:
        return False
    
# ----------------------------------------
def db_get_user_id_from_email_address(cursor, email_address):
    print('Entered into db_get_user_id_from_email_address')
    cursor.execute('''SELECT id FROM users where Email_address = ? LIMIT 1;''', (email_address,))
    user_id = cursor.fetchone()[0]  # Use fetchone() to get a single result
    print('User Id', user_id, 'from', email_address )
    return user_id

# ---------------------------------------- Reset Password
def db_reset_password(cursor, email_address, password):
    cursor.execute('''UPDATE users SET password = ? WHERE email_address = ?;''', (password, email_address))
    print('Password updaet for user', email_address)
    cursor.execute('''SELECT id FROM users where Email_address = ? LIMIT 1;''', (email_address,))
    user_id = cursor.fetchone()[0]  # Use fetchone() to get a single result
    print('User Id', user_id, 'from', email_address )
    return user_id