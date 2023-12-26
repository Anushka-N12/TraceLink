import pymysql as ps
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv('.env')

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
    
if __name__ == '__main__':
    print(authenticate('11', 'anushka.2003', 'abc123'))
    print(authenticate('11', 'anushka.2003', 'abc12'))