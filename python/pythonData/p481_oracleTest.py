import cx_Oracle
import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series

cx_Oracle.init_oracle_client(lib_dir="/usr/local/OracleXE/instantclient_19_26")

plt.rcParams['font.family'] = 'NanumBarunGothic'

conn = None
cur = None

try:
    loginfo = 'hr/1234@192.168.1.131:1521/xe'
    conn = cx_Oracle.connect(loginfo)
    cur = conn.cursor()

    sql = 'select * from country_summary_top_10'
    cur.execute(sql)

    for item in cur:
        print(item)

except Exception as err:
    print(err)

finally:
    if cur != None:
        cur.close()

    if conn != None:
        conn.close()

print("finished...")