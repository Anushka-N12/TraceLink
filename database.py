# Script to access local database
# Importing required packages
import pymysql as ps
import pandas as pd
import os
from dotenv import load_dotenv

# Loading environment variables
load_dotenv('.env')

# Function used by app.py to authenticate user during login
def authenticate(company, id, pw):
    try:
        con = ps.connect(host = 'localhost',
                        user = 'root', 
                        password = os.getenv('pw'),
                        db= 'pde2101')
        cur = con.cursor()
        cur.execute(f'select * from c{company} where id="{id}"')
        rs = cur.fetchone()
        df = pd.DataFrame (rs)[0]
        if pw == df[1]:
            return True
        else: 
            return False
    except: 
        return False
    
# Function used by app.py to get company email
def getemail(company):
    try:
        con = ps.connect(host = 'localhost',
                        user = 'root', 
                        password = os.getenv('pw'),
                        db= 'pde2101')
        cur = con.cursor()
        cur.execute(f'select email from tl_companies where id="{company}"')
        rs = cur.fetchone()
        df = pd.DataFrame (rs)[0][0]
        return df
    except:
        return ''

# Test to execute only if this file is executed directly    
if __name__ == '__main__':
    print(authenticate('11', 'anushka.2003', 'Abc123'))
    print(authenticate('11', 'anushka.2003', 'abc12'))
    print(getemail('11'))