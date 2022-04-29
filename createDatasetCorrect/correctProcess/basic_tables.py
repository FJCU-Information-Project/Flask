#attribute, node, result_attribute, result
import mysql.connector as conn
from mysql.connector import Error
import pandas as pd

#確認需不需要create(attribute, node, result_attribute, result)
def check_tables(cursor, user_id):
    SQL_table_name = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE `TABLE_SCHEMA` = '%s' ORDER BY TABLE_NAME"%(user_id)
    cursor.execute(SQL_table_name)
    tables = cursor.fetchall()
    for i in tables:
        if i[0] == 'attribute' or i[0] == 'node' or i[0] == 'result_attribute' or i[0] == 'result':
            return 1
        else:
            return 0

def read_csv(file): #讀取檔案
    if __name__ == '__main__':
        data = pd.read_csv('../temp/%s'%(file))
    else:
        data = pd.read_csv('../temp/%s'%(file))
        # data = pd.read_csv('database/correctProcess/%s.csv'%(file))
    df = pd.DataFrame(data)
    df = df.astype(object).where(pd.notnull(df), None) #處理空值
    
    return df

#整理資料(屬性)
def data_arrange_attribute(dataset_id, attribute_file):
    df = read_csv(attribute_file)
    attr_len_name = 0
    attr_len_enname = 0
    lst_attr = []
    for row in df.itertuples():
        attr_id = int(row.id)
        attr_name = str(row.name)
        attr_enname = str(row.en_name)
        
        #將所有資料放進串列中以便後續insert
        values = (dataset_id, attr_id, attr_name, attr_enname)
        if values not in lst_attr:
            lst_attr.append(values)
       
        #找出最長字串的長度，建立table時使用
        if len(attr_name) > attr_len_name:
            attr_len_name = len(attr_name)
        if len(attr_enname) > attr_len_enname:
            attr_len_enname = len(attr_enname)
            
    return lst_attr, attr_len_name, attr_len_enname

#INSERT INTO `attribute`
def insert_into_attribute(cursor, user_id, dataset_id, lst):
    item = lst.pop()
    insert_attribute = f"insert into `{user_id}`.`attribute` values ({item[0]}, {item[1]}, '{item[2]}', '{item[3]}')"
    for i in lst:
        insert_attribute += f",({i[0]}, {i[1]}, '{i[2]}', '{i[3]}')"
        #insert_attribute = "INSERT INTO `" + user_id + "`.`attribute` VALUES(%s, %s, %s, %s)"
        # INSERT INTO `" + user_id + "`.`attribute` VALUES(%s, %s, %s, %s),(%s, %s, %s, %s)
    try:     
        print(insert_attribute)   
        cursor.execute(insert_attribute)
    except Error as e:
        print(e)
    
#整理資料(節點)
def data_arrange_node(dataset_id, node_file):
    df = read_csv(node_file)
    node_len_name = 0
    lst_node = []
    new_node_id = 0
    for row in df.itertuples():
        new_node_id += 1
        node_id = int(row.id)
        node_name = str(row.name)
        node_attr = int(row.attribute)
        
        #將所有資料放進串列中以便後續insert
        values = (dataset_id, node_attr, new_node_id, node_id, node_name)
        if values not in lst_node:
            lst_node.append(values)
        
        #找出最長字串的長度，建立table時使用
        if len(node_name) > node_len_name:
            node_len_name = len(node_name)
            
    return lst_node, node_len_name
    
#INSERT INTO `node`
def insert_into_node(cursor, user_id, dataset_id, lst):
    item = lst.pop()
    insert_node = f"insert into `{user_id}`.`node` values ({item[0]}, {item[1]}, {item[2]}, {item[3]}, '{item[4]}')"
    for i in lst:
        insert_node += f",({i[0]}, {i[1]}, {i[2]}, {i[3]}, '{i[4]}')"
        #insert_attribute = "INSERT INTO `" + user_id + "`.`attribute` VALUES(%s, %s, %s, %s)"
        # INSERT INTO `" + user_id + "`.`attribute` VALUES(%s, %s, %s, %s),(%s, %s, %s, %s)
    try:     
        print(insert_node)   
        cursor.execute(insert_node)
    except Error as e:
        print(e)
    # insert_attribute = "INSERT INTO `" + user_id + "`.`node` VALUES(%s, %s, %s, %s, %s)"
    # cursor.executemany(insert_attribute, lst)
    
#整理資料(result_attribute)    
def data_arrange_result_attribute(dataset_id, result_attribute_file):
    df = read_csv(result_attribute_file)
    result_attr_len_name = 0
    result_attr_len_enname = 0
    lst_result_attr = []
    for row in df.itertuples():
        result_attr_id = int(row.id)
        result_attr_name = str(row.name)
        result_attr_enname = str(row.enname)
        
        #將所有資料放進串列中以便後續insert
        values = (dataset_id, result_attr_id, result_attr_name, result_attr_enname)
        if values not in lst_result_attr:
            lst_result_attr.append(values)
       
        #找出最長字串的長度，建立table時使用
        if len(result_attr_name) > result_attr_len_name:
            result_attr_len_name = len(result_attr_name)
        if len(result_attr_enname) > result_attr_len_enname:
            result_attr_len_enname = len(result_attr_enname)
    
    return lst_result_attr, result_attr_len_name, result_attr_len_enname
    
#INSERT INTO `result_attribute`
def insert_into_result_attribute(cursor, user_id, dataset_id, lst):
    item = lst.pop()
    insert_result_attribute = f"insert into `{user_id}`.`result_attribute` values ({item[0]}, {item[1]}, '{item[2]}', '{item[3]}')"
    for i in lst:
        insert_result_attribute += f",({i[0]}, {i[1]}, '{i[2]}', '{i[3]}')"
        #insert_attribute = "INSERT INTO `" + user_id + "`.`attribute` VALUES(%s, %s, %s, %s)"
        # INSERT INTO `" + user_id + "`.`attribute` VALUES(%s, %s, %s, %s),(%s, %s, %s, %s)
    try:     
        print(insert_result_attribute)   
        cursor.execute(insert_result_attribute)
    except Error as e:
        print(e)
    # insert_result_attribute = "INSERT INTO `" + user_id + "`.`result_attribute` VALUES(%s, %s, %s, %s)"
    # cursor.executemany(insert_result_attribute, lst)
    
#整理資料(肇事結果)
def data_arrange_result(dataset_id, result_file):
    df = read_csv(result_file)
    result_len_name = 0
    lst_result = []
    new_result_id = 0
    for row in df.itertuples():
        new_result_id += 1
        result_id = int(row.id)
        result_name = str(row.name)
        result_attr = int(row.attribute)
        
        #將所有資料放進串列中以便後續insert
        values = (dataset_id, result_attr, new_result_id, result_id, result_name)
        if values not in lst_result:
            lst_result.append(values)
       
        #找出最長字串的長度，建立table時使用
        if len(result_name) > result_len_name:
            result_len_name = len(result_name)
            
    return lst_result, result_len_name
    
#INSERT INTO `result`
def insert_into_result(cursor, user_id, dataset_id, lst):
    print(23)
    item = lst.pop()
    insert_result = f"insert into `{user_id}`.`result` values ({item[0]}, {item[1]}, {item[2]}, {item[3]}, '{item[4]}')"
    for i in lst:
        insert_result += f",({i[0]}, {i[1]}, {i[2]}, {i[3]}, '{item[4]}')"
        #insert_attribute = "INSERT INTO `" + user_id + "`.`attribute` VALUES(%s, %s, %s, %s)"
        # INSERT INTO `" + user_id + "`.`attribute` VALUES(%s, %s, %s, %s),(%s, %s, %s, %s)
    try:     
        print(insert_result)   
        cursor.execute(insert_result)
    except Error as e:
        print(e)
    
def create_tables(cursor, user_id, dataset_id, attribute_file, node_file, result_attribute_file, result_file):
    #attribute
    attr_len_name = data_arrange_attribute(dataset_id, attribute_file)[1]
    print(324238)
    attr_len_enname = data_arrange_attribute(dataset_id, attribute_file)[2]
    
    print('attribute') #確認執行至此            
    #建立屬性(attribute) table
    create_attribute = """ CREATE TABLE `%s`.`attribute`(
    `dataset` SMALLINT(3),
    `id` TINYINT(3),
    `name` VARCHAR(%s),
    `enname` VARCHAR(%s),
    PRIMARY KEY(`dataset`, `id`),
    FOREIGN KEY(`dataset`) REFERENCES `dataset`(`id`)
    )""" %(user_id, attr_len_name, attr_len_enname)
    print(create_attribute)
    cursor.execute(create_attribute)
    print("Successfully CREATE attribute") #確認執行至此
    
#node
    node_len_name = data_arrange_node(dataset_id, node_file)[1]
    
    #建立節點(node) table
    create_node = """ CREATE TABLE `%s`.`node`(
    `dataset` SMALLINT(3),
    `attribute` TINYINT(3),
    `id` SMALLINT(3),
    `original_id` TINYINT(3),
    `name` VARCHAR(%s),
    PRIMARY KEY(`dataset`, `attribute`, `id`),
    FOREIGN KEY(`dataset`, `attribute`) REFERENCES `attribute`(`dataset`, `id`)
    )""" %(user_id, node_len_name)
    cursor.execute(create_node)
    print("Successfully CREATE node")#確認執行至此    
#result_attribute
    result_attr_len_name = data_arrange_result_attribute(dataset_id, result_attribute_file)[1]
    result_attr_len_enname = data_arrange_result_attribute(dataset_id, result_attribute_file)[2]
    
    #建立肇事結果屬性(result_attribute) table
    create_result_attribute = """ CREATE TABLE `%s`.`result_attribute`(
    `dataset` SMALLINT(3),
    `id` TINYINT(2),
    `name` VARCHAR(%s),
    `enname` VARCHAR(%s),
    PRIMARY KEY(`dataset`, `id`),
    FOREIGN KEY(`dataset`) REFERENCES `dataset`(`id`)
    )""" %(user_id, result_attr_len_name, result_attr_len_enname)
    cursor.execute(create_result_attribute)
    print("Successfully CREATE result_attribute")

#result
    result_len_name = data_arrange_result(dataset_id, result_file)[1]
    
    #建立肇事結果(result) table
    create_result = """ CREATE TABLE `%s`.`result`(
    `dataset` SMALLINT(3),
    `attribute` TINYINT(2),
    `id` TINYINT(3),
    `original_id` TINYINT(3),
    `name` VARCHAR(%s),
    PRIMARY KEY(`dataset`, `attribute`, `id`),
    FOREIGN KEY(`dataset`, `attribute`) REFERENCES `result_attribute`(`dataset`, `id`)
    )""" %(user_id, result_len_name)
    cursor.execute(create_result)
    print("Successfully CREATE result") #確認執行至此

def create_other_table(cursor, user_id):
    #case
    create = """CREATE TABLE `%s`.`case`(
                `dataset` SMALLINT(3),
                `id` MEDIUMINT(7),
                PRIMARY KEY(`dataset`, `id`), 
                FOREIGN KEY(`dataset`) REFERENCES `file`(`dataset`)
                )"""%(user_id)
    cursor.execute(create)
    print("Successfully CREATE case") #確認執行至此
    
    get_attribute = f"SELECT `enname` FROM `{user_id}`.`attribute`"
    cursor.execute(get_attribute)
    attribute = cursor.fetchall()
    for i in range(len(attribute)):
        add = "ALTER TABLE `%s`.`case` ADD COLUMN `"%(user_id)+str(attribute[i][0])+"` SMALLINT(3)"
        cursor.execute(add)
    print("Successfully alter case factor") #確認執行至此
    
    get_result_attribute = f"SELECT `enname` FROM `{user_id}`.`result_attribute`"
    cursor.execute(get_result_attribute)
    result_attribute = cursor.fetchall()
    for i in range(len(result_attribute)):
        add = "ALTER TABLE `%s`.`case` ADD COLUMN `"%(user_id)+str(result_attribute[i][0])+"` SMALLINT(3)"
        cursor.execute(add)
    print("Successfully alter case result") #確認執行至此
    #result_weight
    create = """CREATE TABLE `%s`.`result_weight`(
                `dataset` SMALLINT(3),
                `from_id` SMALLINT(3),
                `to_id` SMALLINT(3),
                `result` TINYINT(3),
                `total` MEDIUMINT(6) DEFAULT 0,
                PRIMARY KEY(`dataset`, `from_id`, `to_id`, `result`),
                FOREIGN KEY(`dataset`) REFERENCES `dataset`(`id`)
                )"""%(user_id)
    cursor.execute(create)
    print("Successfully create result_weight") #確認執行至此

    #weight
    create = """CREATE TABLE `%s`.`weight`(
                `dataset` SMALLINT(3),
                `from_id` SMALLINT(3),
                `to_id` SMALLINT(3),
                `total` MEDIUMINT(6) DEFAULT 0,
                PRIMARY KEY(`dataset`, `from_id`, `to_id`),
                FOREIGN KEY(`dataset`) REFERENCES `dataset`(`id`)
                )"""%(user_id)
    cursor.execute(create)
    print("Successfully create weight") #確認執行至此

    #relationship
    create = """CREATE TABLE `%s`.`relationship`(
                `dataset` SMALLINT(3),
                `case` MEDIUMINT(7),
                `from_id` SMALLINT(3),
                `to_id` SMALLINT(3),
                PRIMARY KEY(`dataset`, `case`, `from_id`, `to_id`),
                FOREIGN KEY(`dataset`, `case`) REFERENCES `case`(`dataset`, `id`)
                )"""%(user_id)
    cursor.execute(create)
    print("Successfully create relationship") #確認執行至此

def insert_into_tables(cursor, user_id, dataset_id, attribute_file, node_file, result_attribute_file, result_file):
#attribute
    lst = data_arrange_attribute(dataset_id, attribute_file)[0]          
    insert_into_attribute(cursor, user_id, dataset_id, lst) #insert into attribute
    print("attribute") #確認執行至此

#node
    lst = data_arrange_node(dataset_id, node_file)[0]
    insert_into_node(cursor, user_id, dataset_id, lst) #insert into node
    print("node") #確認執行至此

#result_attribute
    lst = data_arrange_result_attribute(dataset_id, result_attribute_file)[0]
    insert_into_result_attribute(cursor, user_id, dataset_id, lst)
    print("result_attribute") #確認執行至此

#result
    lst = data_arrange_result(dataset_id, result_file)[0]
    insert_into_result(cursor, user_id, dataset_id, lst) #insert into result
    print("result") #確認執行至此

def insert_file(connection, cursor, user_id, dataset_id, file_lst):
    print(dataset_id, 335
    )
    for file in file_lst:
        #找最後一個id
        max_id = "SELECT MAX(`id`) FROM `%s`.`file` WHERE `dataset` = %s"%(user_id, dataset_id)
        cursor.execute(max_id)
        auto_id = cursor.fetchall()
        if auto_id[0][0] == None:
            auto_id = 0
        else:
            auto_id = int(auto_id[0][0])
        
        auto_id += 1
        if type(file) == type(""):
            insert = "INSERT INTO `" + user_id + "`.`file`(`dataset`, `id`, `name`) VALUES(%s, %d, '%s')"%(dataset_id, auto_id, file)
        else:
            insert = "INSERT INTO `" + user_id + "`.`file`(`dataset`, `id`, `name`) VALUES(%s, %d, '%s')"%(dataset_id, auto_id, file[0])
        print(insert)
        cursor.execute(insert)
        connection.commit()

#新增案件   
def insert_case(cursor, user_id, dataset_id, file_lst):
    for file in range(1):
    # for file in file_lst:
        df = pd.read_csv('../temp/%s'%(file_lst))
        df = df.astype(object).where(pd.notnull(df), None) #處理空值
        max_id = f"select max(`id`) from `{user_id}`.`case` where dataset = {dataset_id}"
        #找最後一個id

        #max_id = "SELECT MAX(`id`) FROM `" + user_id + "`.`case` WHERE `dataset` = '" + dataset_id + "'"
        print(max_id)
        cursor.execute(max_id)
        auto_id = cursor.fetchall()
        if auto_id[0][0] == None:
            auto_id = 0
        else:
            auto_id = int(auto_id[0][0])

        #計算result_attribute
        SQL = f"select count(`id`) from `{user_id}`.`result_attribute` where dataset = {dataset_id}"
        # SQL = "SELECT COUNT(`id`) FROM `%s`.`result_attribute` WHERE `dataset` = %s"%(user_id, dataset_id)
        print(SQL)
        cursor.execute(SQL)
        count = cursor.fetchall()[0][0]
        
        #node新舊id對照的串列(new_id, original_id, attribute)
        SQL = f"select `id`, `original_id`, `attribute` from `{user_id}`.`node` where dataset = {dataset_id}"
        # SQL_ids = "SELECT `id`, `original_id`, `attribute` FROM `%s`.`node` WHERE `dataset` = %s"%(user_id, dataset_id)
        print(SQL)
        cursor.execute(SQL)
        ids_lst = cursor.fetchall()
        id_dic = []
        for i in range(len(ids_lst)):
            id_dic.append(ids_lst[i])
        
        #result新舊id對照的串列(new_id, original_id, attribute)
        SQL = f"select `id`, `original_id`, `attribute` from `{user_id}`.`result` where dataset = {dataset_id}"
        # SQL_ids = "SELECT `id`, `original_id`, `attribute` FROM `%s`.`result` WHERE `dataset` = %s"%(user_id, dataset_id)
        print(SQL)
        cursor.execute(SQL)
        result_ids_lst = cursor.fetchall()
        result_id_dic = []
        for i in range(len(result_ids_lst)):
            result_id_dic.append(result_ids_lst[i])
    
        #看case有幾個欄位，建立SQL語法
        SQL = f"select COUNT(*) FROM information_schema.COLUMNS WHERE table_schema= {user_id} AND table_name='case'"
        # SQL = "SELECT COUNT(*) FROM information_schema.COLUMNS WHERE table_schema= '%s' AND table_name='case'"%(user_id)
        print(SQL)
        cursor.execute(SQL)
        columns = cursor.fetchall()[0][0]
        SQL = f"INSERT INTO `{user_id}`.`case` VALUES ("
        for i in range(columns):
            if i != columns-1:
                SQL += '%s, '
            else:
                SQL += '%s)'  
        print(SQL)
        lst = []
        for each in df.values:
            auto_id += 1
            data = [dataset_id, auto_id]
            for i in range(len(each)-count):
                #node的部分
                if each[i] is None:
                    data.append(None)
                else:
                    #將original_id 轉換為node的id, id_dic = (new_id, original_id, attribute_id)
                    for j in range(len(id_dic)): 
                        if int(each[i]) == id_dic[j][1] and i+1 == id_dic[j][2]:
                            data.append(id_dic[j][0])
            
            flag = 0
            for i in range(len(each)-count, len(each)):
                flag += 1
                #result的部分
                if each[i] is None:
                    data.append(None)
                else:
                    #將original_id 轉換為result的id, result_id_dic = (new_id, original_id, attribute_id)
                    for j in range(len(result_id_dic)):
                        if int(each[i]) == result_id_dic[j][1] and flag == result_id_dic[j][2]:
                            data.append(result_id_dic[j][0])
            data = tuple(data)
            lst.append(data)
            #print(auto_id)
        cursor.executemany(SQL, lst)

def main(user_id, dataset_id, attribute, node, result_attribute, result, file):
    try:
        #資料庫連線
        connection = conn.connect(
            host='140.136.155.121',
            user='root',
            password='IM39project',
            port='50306')
        print("資料庫連線成功 in main")
        cursor = connection.cursor()
        flag = check_tables(cursor, user_id) # 1: 有四張表了, 0: 還沒有四張表
        print(flag)
        if flag == 0: #需CREATE TABLE
            print("CREATE TABLE")
            create_tables(cursor, user_id, dataset_id, attribute, node, result_attribute, result)
            insert_into_tables(cursor, user_id, dataset_id, attribute, node, result_attribute, result)
            connection.commit()
            SQL = "SELECT `id`, `name` FROM `%s`.`node` WHERE `dataset` = %s"%(user_id, dataset_id)
            print(SQL)
            cursor.execute(SQL)
            lst = cursor.fetchall()
            create_other_table(cursor, user_id)
            # insert_file(connection, cursor, user_id, dataset_id, file)
            insert_case(cursor, user_id, dataset_id, file)
    
        else:
            insert_into_tables(cursor, user_id, dataset_id, attribute, node, result_attribute, result)
            connection.commit()
            SQL = "SELECT `id`, `name` FROM `%s`.`node` WHERE `dataset` = %s"%(user_id, dataset_id)
            cursor.execute(SQL)
            lst = cursor.fetchall()
            # print(lst)
            # insert_file(connection, cursor, user_id, dataset_id, file)
            insert_case(cursor, user_id, dataset_id, file)
            connection.commit()
            print("Successfully insert %s into case"%file) #確認執行至此
            
        connection.commit() #最後一定要commit上去
    except Error as e:
        print("資料庫連接失敗：", e)
    except Exception as e:
        print("其他錯誤", e)
    cursor.close()
    connection.close()


if __name__ == '__main__':
    file_lst = ['11002', '11003', '11005', '11006']
    main('test0429', 1, 'attribute', 'node', 'result_attribute', 'result', file_lst)
    #main(user_id, dataset_id, attribute, node, result_attribute, result, file)   