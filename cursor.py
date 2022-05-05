#跑關聯，算權重
import mysql.connector as conn
from mysql.connector import Error

def main():
    try:
        #資料庫連線
        connection = conn.connect(
            host='140.136.155.121',
            user='root',
            password='IM39project',
            port='50306')
        print("資料庫連線成功")
        cursor = connection.cursor()

        connection.commit()
    except Error as e:
        print("資料庫連接失敗：", e)
    cursor.close()

    connection.close()
main()
