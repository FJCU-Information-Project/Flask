from flask import Blueprint, request, jsonify
from flask_cors import CORS,cross_origin
from app_db import getTokenId
import mysql.connector as conn
import datetime as dt
import time

history = Blueprint('history', __name__)

connection = conn.connect(
            host='140.136.155.121',
            user='root',
            password='IM39project',
            port='50306')

CORS(history, resources={"/.*": {
    "origins": "*",
    "methods": "*",
    "headers": "*",
    "allow_headers": "*",
    "supports_credentials": True,
}})


@history.route('/historyCreate', methods=['OPTIONS','POST'])
def historyCreate():
    userToken, datasetID = getTokenId(request)
    if not userToken:
        return jsonify({"Auth":"ERROR"}),401
      
    owner = request.form.get('owner',False)
    if not owner or not datasetID:
        return jsonify({"User":"Empty"}),401
    
    # 或是使用 
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # now = dt.date.today()
    # print(now2)
    print(now)
    cursor = connection.cursor()
    sql = f"insert into `trans`.`history` (`id`,`owner`,`dataset`,`view_time`) values ('{userToken}', '{owner}', {datasetID}, '{now}') on duplicate key update `view_time` = '{now}'"
    print(sql)
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    
    return jsonify({'status': 'success create history'}),200

@history.route('/historyRead', methods=['OPTIONS','POST'])
def historyRead():
    userToken = request.form.get('token',False)
    print(userToken)
    if not userToken:
        return jsonify({"Auth":"ERROR"}),401

    cursor = connection.cursor()
    sql = f"select * from `trans`.`history` where id = '{userToken}'"
    print(sql)
    cursor.execute(sql)
    datas = list(cursor.fetchall())
    print(datas)
    
    retData = []
    for data in datas:
        historyData = {}
        historyData["dataset"] = data[2]
        historyData["time"] = data[3]
        
        sql = f'select * from `{data[1]}`.dataset where id = "{historyData["dataset"]}"'
        print(sql)
        cursor.execute(sql)
        datasetDatas = list(list(cursor.fetchall())[0])
        print(datasetDatas)

        historyData["datasetName"] = datasetDatas[1]
        historyData["owner"] = datasetDatas[2]
        historyData["datasetPublic"] = datasetDatas[6]
        
        print(historyData)
        retData.append(historyData)
    print(retData)
    return jsonify(retData)
