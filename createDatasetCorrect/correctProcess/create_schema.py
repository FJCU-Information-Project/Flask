#建立schema、建立dataset, file table
import mysql.connector as conn
from mysql.connector import Error

def check_schema(cursor, user_id):
    SQL_schema = "SHOW DATABASES"
    cursor.execute(SQL_schema)
    schemas = cursor.fetchall()
    flag = 0
    for i in schemas:
        if i[0] == user_id:
            flag = 1
    return flag


def create_basic_tables(cursor, user_id):
    #建立一個schema
    create_schema = "CREATE SCHEMA `%s` DEFAULT CHARACTER SET utf8"%(user_id)
    cursor.execute(create_schema)

    #建立資料集(dataset) table 預設為不公開
    create_dataset = """CREATE TABLE `%s`.`dataset`(
    `id` SMALLINT(3) AUTO_INCREMENT,
    `name` VARCHAR(30),
    `unit` VARCHAR(20),
    `period_start` DATE,
    `period_end` DATE,
    `note` VARCHAR(100),
    `upload_date` DATE,
    `is_public` TINYINT(1) DEFAULT 0,
    PRIMARY KEY(`id`))"""%(user_id)
    cursor.execute(create_dataset)

    #建立檔案(file) table
    create_file = """ CREATE TABLE `%s`.`file`(
    `dataset` SMALLINT(3),
    `id` TINYINT(2),
    `name` VARCHAR(20),
    PRIMARY KEY(`dataset`, `id`),
    FOREIGN KEY(`dataset`) REFERENCES `dataset`(`id`)
    )"""%(user_id)
    cursor.execute(create_file)
def main(user_id):    
    try:
        #資料庫連線
        connection = conn.connect(
            host='140.136.155.121',
            user='root',
            password='IM39project',
            port='50306')
        if connection.is_connected():
            print("資料庫連線成功")
            cursor = connection.cursor()
            
            flag = check_schema(cursor, user_id)
            if flag == 0:
                create_basic_tables(cursor, user_id)
                print("Succefully Create schema, dataset, file!") #確認執行至此
                connection.commit()
            else:
                print("Schema already existed!")
    except Error as e:
        print("資料庫連接失敗：", e)
    cursor.close()
    connection.close()
if __name__ == '__main__':
    main('test0429')
