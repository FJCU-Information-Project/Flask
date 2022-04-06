from flask import Flask, render_template, request, jsonify, Blueprint
from flask_cors import CORS
from email.policy import HTTP
from werkzeug.utils import secure_filename
import pymysql
from mysql.connector import Error

from app_receieves import receieves
from app_csv import csv_apis
from app_db import db_methods
#import database.rank

app = Flask(__name__
            ,static_url_path="/trans"
            ,static_folder = "../trans/docs")
            # 用來設定說
app.register_blueprint(receieves)
app.register_blueprint(csv_apis)
app.register_blueprint(db_methods)

# CORS(app, resources={"/*": {"origins": "*"}})
CORS(app)

# Constant----
#USER_ID = "304u39481-20"
#USER_ID = "5678"
#USER_ID = "9840-menqwk"
USER_ID = "3654"
#DATASET_ID = 1
DATASET_ID = 1
UPLOAD_FOLDER = "../temp"
tokens = [
    "12345678",
    "ABCDEFGH"
]
# ------------

conn = pymysql.connect(host='140.136.155.121', port=50306,
                    user='root', passwd='IM39project')
cursor = conn.cursor()



@app.route("/")
def index():
    name = request.args.get("name")
    return render_template("index.html", name=name)

@app.route("/attributes")
def attributes():
    sql = "SELECT * FROM `" + USER_ID + "`.`attribute` WHERE dataset = " + str(DATASET_ID)
    print(sql)
    cursor.execute(sql)
    attributes = cursor.fetchall()

    attributeData = []
    for i in attributes:
        attribute = {}
        attribute["value"] = i[1]
        attribute["label"] = i[2]
        sql = "select * from `" + USER_ID + "`.`node` where attribute = " + str(i[1])
        print(sql)
        cursor.execute(sql)
        nodes = cursor.fetchall()
        attribute["children"] = []
        for j in nodes:
            node = {}
            node["value"] = j[2]
            node["label"] = j[4]
            attribute["children"].append(node)

        attributeData.append(attribute)
    # print(nodes)
    conn.commit()
    # print(jsonify(attributeData))
    return jsonify(attributeData)


@app.route("/resultAttributes")
def resultattributes():
    cursor.execute("SELECT * FROM `"+USER_ID+"`.`result_attribute`")
    resultAttributes = cursor.fetchall()

    resultAttributeData = []
    for i in resultAttributes:
        resultAttribute = {}
        resultAttribute["value"] = i[1]
        resultAttribute["label"] = i[2]

        cursor.execute("select * from `"+USER_ID+"`.`result` where attribute =" + str(i[1]))
        results = cursor.fetchall()
        resultAttribute["children"] = []
        for j in results:
            result = {}
            result["value"] = j[2]
            result["label"] = j[4]
            resultAttribute["children"].append(result)

        resultAttributeData.append(resultAttribute)
    print(resultAttribute)
    conn.commit()
    print(jsonify(resultAttributeData))
    return jsonify(resultAttributeData)

@app.route("/nodes")
def nodes():
    cursor.execute("select * from `" + USER_ID + "`.`node`")
    row = cursor.fetchall()

    jsonData = []
    for i in row:
        result = {}    # temp store one jsonObject
        result["id"] = i[0]  # 将row中的每个元素，追加到字典中。　
        result["node"] = i[1]
        jsonData.append(result)

    conn.commit()
    print(jsonify(jsonData))
    return jsonify(jsonData)

@app.route("/sna_graph/<filename>")
def sna_graph_f(filename):
    print(filename)
    return render_template(filename)

@app.route("/sna_graph/<folder>/<paths>/<filenames>")
def sna_graph_f_p_f(folder, paths, filenames):
    print(folder)
    print(paths)
    print(filenames)
    string = folder + "/" + paths + "/" + filenames
    try:
        return render_template(string)
    except:
        return "File not exist"

@app.route("/auth", methods=['POST'])
def auth():
    global USER_ID
    conn.ping(reconnect=True)
    auth_cursor = conn.cursor()
    res = {"valid": None}
    data = request.get_json()
    sql = "select * from `trans`.`user` where id =" + str(data["token"])
    print(sql)
    auth_cursor.execute(sql)
    conn.commit()
    user = list(auth_cursor.fetchall())
    print(user)

    if user:
        res["valid"] = True
        USER_ID = data["token"]
    else:
        res["valid"] = False
    # data = request.get_json()
    # res = {"valid": None}
    # res["valid"] = True if data["token"] in tokens else False
    return jsonify(res)



@app.route("/token")
def token():
    link = "https://prod.liveshare.vsengsaas.visualstudio.com/join?CDFC380F8E1D911410EC7EF63BE355C2EDAE"
    return "<a href='"+link+"'>"+link+"</a>"

@app.route("/exampleTable")
def exampleTable():
    conn.ping(reconnect=True)
    sql = "select * from `trans`.`user`"
    print(sql)
    cursor.execute(sql)
    users = cursor.fetchall()
    
    exampleDatasets = []
    for user in users:
        sql = "select * from `" + str(user[0]) + "`.`dataset` WHERE is_public = 1"
        cursor.execute(sql)
        userDatasets = cursor.fetchall()
        userDatasets = list(userDatasets)
        
        for userDataset in userDatasets:
            exampleTablesTags = [
                "datasetName",
                "datasetUnit",
                "datasetStart",
                "datasetEnd",
                "datasetNote",
                "datasetPublic",
            ]
            exampleTableData = {}
            for i in range(len(exampleTablesTags)):
                exampleTableData[exampleTablesTags[i]] = userDataset[i+1]
            exampleDatasets.append(exampleTableData)

    conn.commit()
    print("exampleTable")
    return jsonify(exampleDatasets)

@app.route("/customizeTable")
def customizeTable():
    conn.ping(reconnect=True)
    sql = "select * from `" + USER_ID + "`.`dataset`"
    try:
        cursor.execute(sql)
    except Error:
        print(Error)
    customizeDatas = list(cursor.fetchall())

    customizeDataset = []
    for customizeData in customizeDatas:
        customizeTableTags = [
            "datasetName",
            "datasetUnit",
            "datasetStart",
            "datasetEnd",
            "datasetNote",
            "datasetPublic",
        ]
        customizeTableDatas = {}
        for i in range(len(customizeTableTags)):
            customizeTableDatas[customizeTableTags[i]]= customizeData[i+1]
        customizeDataset.append(customizeTableDatas)

    return jsonify(customizeDataset)

if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.debug = True
    # 正式環境註解上面這行
    if conn:
        print("conneted")
    else:
        print("Connect ERROR")
    app.run(host="0.0.0.0", port="50000")
