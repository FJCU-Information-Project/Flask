#跑關聯，算權重
import mysql.connector as conn
from mysql.connector import Error

def relationship(cursor, user_id, dataset_id):
    #讀取attribute的id 跟enname，並建立詞典
    SQL_attribute = f"SELECT `id`, `enname` FROM `{user_id}`.`attribute` WHERE `dataset` = {dataset_id}"
    print(SQL_attribute)
    cursor.execute(SQL_attribute)
    attribute = cursor.fetchall()

    #建立SQL語法用的字串(SELECT case的所有屬性的資料)、id_lst
    attr_string = ''
    attr_id_lst = []
    for i in range(len(attribute)):
        attr_id_lst.append(attribute[i][0])
        if i != len(attribute)-1:
            attr_string += ("`" + str(attribute[i][1]) + "`, ")
        else:
            attr_string += ("`" + str(attribute[i][1]) + "`")

    #算有幾個case
    SQL = "SELECT COUNT(`id`) FROM `%s`.`case` WHERE `dataset` = %s"%(user_id, dataset_id)
    print(SQL)
    cursor.execute(SQL)
    rounds = cursor.fetchone()
    rounds = rounds[0]

    #讀取result，讓SQL語法可以變數加入
    SQL_result = "SELECT `enname` FROM `%s`.`result_attribute` WHERE `dataset` = %s"%(user_id, dataset_id)
    print(SQL_result)
    cursor.execute(SQL_result)
    result_attribute = cursor.fetchall()
    sql_string = ''
    for i in range(len(result_attribute)):
        if i != len(result_attribute)-1:
            sql_string += ("`" + str(result_attribute[i][0]) + "` OR ")
        else:
            sql_string += ("`" + str(result_attribute[i][0]) + "`")

    #過濾掉case中沒有結果紀錄的
    SQL_pass = "SELECT `id` FROM `%s`.`case` WHERE `dataset` = %s AND "%(user_id, dataset_id)+sql_string+" IS NOT NULL"
    print(SQL_pass)
    cursor.execute(SQL_pass)
    pass_id_lst = cursor.fetchall()

    #抓出案件資料
    id_string = ''
    for i in range(len(pass_id_lst)):
        if i != len(pass_id_lst)-1:
            id_string += str(pass_id_lst[i][0]) + ', ' 
        else:
            id_string += str(pass_id_lst[i][0])
    SQL_case = "SELECT `id`, "+attr_string+" FROM `%s`.`case` WHERE `dataset` = %s AND `id` IN ("%(user_id, dataset_id)+id_string+")"
    print(SQL_case)
    cursor.execute(SQL_case)
    case_lst = cursor.fetchall()

    for i in range(len(case_lst)):
        for key_from in attr_id_lst:
            lst = []
            for key_to in attr_id_lst:
                if key_from < key_to:
                    from_id = case_lst[i][key_from]
                    to_id = case_lst[i][key_to]
                    if from_id != None and to_id != None:
                        values = (dataset_id, case_lst[i][0], from_id, to_id)
                        if values not in lst:
                            lst.append(values)
                        else:
                            continue

                    else:
                        continue

            #insert_result = f"insert into `{user_id}`.`result` values ({i[0]}, {i[1]}, {i[2]}, {i[3]})"
            SQL = "INSERT INTO `"+user_id+"`.`relationship` VALUES (%s, %s, %s, %s)"
            cursor.executemany(SQL, lst)
        print(case_lst[i][0])

def main(user_id, dataset_id):
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
            #user_id = 'test'
            #dataset_id = 1
            relationship(cursor, user_id, dataset_id)
            connection.commit()
    except Error as e:
        print("資料庫連接失敗：", e)
    cursor.close()
    connection.close()
