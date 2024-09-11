import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta

def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key(local_state_path):
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    
    key = key[5:]
    # return decrypted key that was originally encrypted
    # using a session key derived from current user's logon credentials
    
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        # get the initialization vector
        iv = password[3:15]
        password = password[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # not supported
            return ""

def main():
    # specify the paths to the `Login Data` and `Local State` files
    login_data_path = r"path\to\your\Login Data"
    local_state_path = r"path\to\your\Local State"
    
    # get the AES key
    key = get_encryption_key(local_state_path)
    
    # copy the `Login Data` file to another location
    # as the database will be locked if chrome is currently running
    filename = "ChromeData.db"
    shutil.copyfile(login_data_path, filename)
    
    # connect to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # `logins` table has the data we need
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    
    with open("login_data.txt", "w", encoding="utf-8") as file:
        # iterate over all rows
        for row in cursor.fetchall():
            origin_url = row[0]
            action_url = row[1]
            username = row[2]
            password = decrypt_password(row[3], key)
            date_created = row[4]
            date_last_used = row[5]        
            if username or password:
                file.write(f"Origin URL: {origin_url}\n")
                file.write(f"Action URL: {action_url}\n")
                file.write(f"Username: {username}\n")
                file.write(f"Password: {password}\n")
            else:
                continue
            if date_created != 86400000000 and date_created:
                file.write(f"Creation date: {str(get_chrome_datetime(date_created))}\n")
            if date_last_used != 86400000000 and date_last_used:
                file.write(f"Last Used: {str(get_chrome_datetime(date_last_used))}\n")
            file.write("="*50 + "\n")
    
    cursor.close()
    db.close()
    try:
        # try to remove the copied db file
        os.remove(filename)
    except:
        pass

if __name__ == "__main__":
    main()
