from flask import Blueprint, request, jsonify
from flask_cors import CORS
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
    timestr = 'Thu Apr 28 2022 00:00:00 GMT+0800 (台灣標準時間)'
    timestr = timestr.split()
    print(timestr)
    now2 = dt.datetime(time.strftime(timestr,"%a %b %d %Y %H:%M:%S GMT+0800 (CST)"))
    now = dt.datetime.now()
    print(now2)
    print(now)
    cursor = connection.cursor()
    sql = f"insert into `trans`.history values ('{userToken}', '{owner}', {datasetID}, '{now}')"
    print(sql)
    cursor.execute(sql)
    connection.commit()
    
    return jsonify({'status': 'success'})

@history.route('/historyRead', methods=['OPTIONS','POST'])
def historyRead():
    userToken = request.form.get('token',False)
    if not userToken:
        return jsonify({"Auth":"ERROR"}),401

    cursor = connection.cursor()
    sql = f"select * from `trans`.history where id = '{userToken}'"
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
