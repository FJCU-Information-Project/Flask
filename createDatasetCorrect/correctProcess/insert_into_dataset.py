#新增資料集基本資料
import mysql.connector as conn
from mysql.connector import Error

# is_public =  # 1: 公開, 0: 非公開(預設)
def main(user_id,name,unit,period_start,period_end,note,is_public):
    try:
        #資料庫連線
        connection = conn.connect(
            host='140.136.155.121',
            user='root',
            password='IM39project',
            port='50306')
        print("資料庫連線成功")
        cursor = connection.cursor()

        values = (name, unit, period_start, period_end, note, is_public)
        
        insert_dataset = """INSERT INTO `"""+user_id + """`.`dataset` 
                        (`name`, `unit`, `period_start`, `period_end`, `note`, `upload_date`, `is_public`)
                        VALUES(%s, %s, %s, %s, %s, CURDATE(), %s)"""
        print(insert_dataset)
        cursor.execute(insert_dataset, values)
        connection.commit() #最後一定要commit上去
        print('Insert into dataset!')
        sel_dataset_id = "SELECT MAX(`id`) FROM `%s`.`dataset`"%(user_id)
        cursor.execute(sel_dataset_id)
        datasetIDs = cursor.fetchall()
        return datasetIDs[0][0]
    except Error as e:
        print("資料庫連接失敗：", e)
        return False
    cursor.close()
    connection.close()

if __name__ == '__main__':
    main('test0429','測試用2','測試用2','2021-01-01','2021-06-30','test',0)
