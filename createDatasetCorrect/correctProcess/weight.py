#預先計算權重
import mysql.connector as conn
from mysql.connector import Error
def main(user_id, dataset_id):
    print(67)
    try:
        #資料庫連線
        connection = conn.connect(
            host='140.136.155.121',
            user='root',
            password='IM39project',
            port='50306')
        print("資料庫連線成功")
        cursor = connection.cursor()

        #attribute
        SQL = "SELECT `id` FROM `%s`.`attribute` WHERE `dataset` = %s ORDER BY `id`"%(user_id, dataset_id)
        cursor.execute(SQL)
        attribute = cursor.fetchall()
        
        #node = [(id, attribute)]
        SQL = "SELECT `id`, `attribute` FROM `%s`.`node` WHERE `dataset` = %s ORDER BY `attribute`, `id`"%(user_id, dataset_id)
        cursor.execute(SQL)
        node = cursor.fetchall()
        
        #預先計算count = [(from_id, to_id, total)]
        select_count = "SELECT `from_id`, `to_id`, COUNT(`case`) FROM `%s`.`relationship` WHERE `dataset` = %s GROUP BY `from_id`, `to_id`"%(user_id, dataset_id)
        cursor.execute(select_count)
        relationship_lst = cursor.fetchall()
        
        
        
#weight
        for key_from in range(len(attribute)):
            from_attr_id = attribute[key_from][0]
            for key_to in range(len(attribute)):
                to_attr_id = attribute[key_to][0]
                if from_attr_id < to_attr_id:
                    from_lst = []
                    to_lst = []
                    for i in range(len(node)):    #node = [(id, attribute)] 
                        if node[i][1] == from_attr_id:
                            from_lst.append(node[i][0])
                        elif node[i][1] == to_attr_id:
                            to_lst.append(node[i][0])
                    lst = []
                    for j in range(len(from_lst)):
                        from_id = from_lst[j]
                        for k in range(len(to_lst)):
                            to_id = to_lst[k]
                            total = 0
                            for m in range(len(relationship_lst)): #count = [(from_id, to_id, count)]
                                if relationship_lst[m][0] == from_id and relationship_lst[m][1] == to_id:
                                    total = relationship_lst[m][2]
                                    break
                            values = (dataset_id, from_id, to_id, total)
                            print(values)
                            lst.append(values)
                    insert = "INSERT INTO `"+user_id+"`.`weight` (`dataset`, `from_id`, `to_id`, `total`) VALUES (%s, %s, %s, %s)"
                    cursor.executemany(insert, lst)
                    connection.commit()
                    print("Successfully INSERT INTO weight")#確認執行至此      

                else:
                    continue
                    
#result_weight 

        #result = [(id, attribute_id, attribute_name)]
        SQL = """SELECT r.`id`, r.`attribute`, ar.`enname` 
                FROM `%s`.`result` r, `%s`.`result_attribute` ar 
                WHERE r.`dataset` = %s AND ar.`dataset` = %s 
                AND r.`attribute` = ar.`id` ORDER BY r.`id`
                """%(user_id, user_id, dataset_id, dataset_id)
        cursor.execute(SQL)
        result = cursor.fetchall()
                
        for i in range(len(result)):
            result_id = result[i][0]
            
            result_attribute_name = result[i][2]
            SQL_count = """SELECT `from_id`, `to_id`, COUNT(`case`) 
                            FROM `%s`.`relationship` 
                            WHERE `dataset` = %s AND 
                            `case` IN (SELECT `id` FROM `%s`.`case` 
                                    WHERE `dataset` = %s AND `%s` = %s) 
                            GROUP BY `from_id`, `to_id`
                        """%(user_id, dataset_id, user_id, dataset_id, result_attribute_name, result_id)
            cursor.execute(SQL_count)
            relationship_lst = cursor.fetchall() #[(from_id, to_id, total)]
            
            for key_from in range(len(attribute)):
                from_attr_id = attribute[key_from][0]
                for key_to in range(len(attribute)):
                    to_attr_id = attribute[key_to][0]
                    if from_attr_id < to_attr_id:
                        from_lst = []
                        to_lst = []
                        for j in range(len(node)):    #node = [(id, attribute)] 
                            if node[j][1] == from_attr_id:
                                from_lst.append(node[j][0])
                            elif node[j][1] == to_attr_id:
                                to_lst.append(node[j][0])
                        lst = []
                        for j in range(len(from_lst)):
                            from_id = from_lst[j]
                            for k in range(len(to_lst)):
                                to_id = to_lst[k]
                                total = 0
                                for m in range(len(relationship_lst)): #count = [(from_id, to_id, count)]
                                    if relationship_lst[m][0] == from_id and relationship_lst[m][1] == to_id:
                                        total = relationship_lst[m][2]
                                        break
                                values = (dataset_id, from_id, to_id, result_id, total)
                                print(values)
                                lst.append(values)
                        insert = "INSERT INTO `"+user_id+"`.`result_weight` (`dataset`, `from_id`, `to_id`, `result`, `total`) VALUES (%s, %s, %s, %s, %s)"
                        cursor.executemany(insert, lst)
                        connection.commit()
                        print("Successfully INSERT INTO result weight")#確認執行至此      
    
                    else:
                        continue
    except Error as e:
        print("資料庫連接失敗：", e)
    cursor.close()
    connection.close()
if __name__ == '__main__':
    main('test','1')
