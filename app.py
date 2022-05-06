
from flask import Flask, render_template, request, jsonify, Blueprint
from flask_cors import CORS, cross_origin
from email.policy import HTTP
from werkzeug.utils import secure_filename
import pymysql
import datetime
from mysql.connector import Error

from app_receieves import receieves
from app_csv import csv_apis
from app_db import db_methods,getTokenId
from app_history import history

import smtplib
from email.mime.text import MIMEText
from email.header import Header

from IMGlobal import USER_ID

#import database.rank

app = Flask(__name__
            ,static_url_path="/trans"
            ,static_folder = "../trans/docs")
            # 用來設定說
app.register_blueprint(receieves)
app.register_blueprint(csv_apis)
app.register_blueprint(db_methods)
app.register_blueprint(history)

CORS(app, resources={"/.*": {
    "origins": "*",
    "methods": "*",
    "headers": "*",
    "allow_headers": "*",
    "supports_credentials": True,
}})

# Constant----
#USER_ID = "304u39481-20"
#USER_ID = "5678"
#USER_ID = "9840-menqwk"
#DATASET_ID = 1
DATASET_ID = 1
UPLOAD_FOLDER = "../temp"
tokens = [
    "12345678",
    "ABCDEFGH"
]
# ------------

connection = pymysql.connect(host='140.136.155.121', port=50306,
                    user='root', passwd='IM39project')



@app.route("/")
def index():
    name = request.args.get("name")
    return render_template("index.html", name=name)

@app.route("/attributes",methods=['GET','OPTIONS','POST'])
def attributes():
    userToken, datasetID = getTokenId(request)
    print(type(userToken), type(datasetID))
    if not userToken or not datasetID:
        return jsonify({"Auth":"ERROR"}),401
    
    sql = "SELECT * FROM `" + userToken + "`.`attribute` WHERE dataset = " + datasetID
    print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    attributes = cursor.fetchall()

    attributeData = []
    for i in attributes:
        attribute = {}
        attribute["value"] = i[1]
        attribute["label"] = i[2]
        sql = "select * from `" + userToken + "`.`node` where attribute = " + str(i[1]) + " and dataset = " + datasetID
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
    connection.commit()
    # print(jsonify(attributeData))
    return jsonify(attributeData)


@app.route("/resultAttributes",methods=['GET','OPTIONS','POST'])
def resultattributes():
    userToken, datasetID = getTokenId(request)
    print(userToken, datasetID)
    if not userToken or not datasetID:
        return jsonify({"Auth":"ERROR"}),401
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `"+userToken+"`.`result_attribute` WHERE dataset = " + datasetID)
    resultAttributes = cursor.fetchall()
    print(resultAttributes)
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
    connection.commit()
    print(jsonify(resultAttributeData))
    return jsonify(resultAttributeData)

@app.route("/nodes",methods=['GET','OPTIONS','POST'])
def nodes():
    userToken, datasetID = getTokenId(request)
    print(userToken, datasetID)
    if not userToken or not datasetID:
        return jsonify({"Auth":"ERROR"}),401
    
    cursor = connection.cursor()
    cursor.execute("select * from `" + userToken + "`.`node` where dataset = " + datasetID)
    row = cursor.fetchall()

    jsonData = []
    for i in row:
        result = {}    # temp store one jsonObject
        result["id"] = i[0]  # 将row中的每个元素，追加到字典中。　
        result["node"] = i[1]
        jsonData.append(result)

    connection.commit()
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

@app.route("/user",methods=['POST'])
def user():
    userToken = request.form.get('token', False)
    sql = f"SELECT * FROM trans.user WHERE id = {userToken}"
    print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    users = cursor.fetchone()
    return jsonify(users)

@app.route("/auth", methods=['OPTIONS','POST'])
def auth():
    userToken, datasetID = getTokenId(request)
    if not userToken:
        return jsonify({"Auth":"ERROR"}),401
    connection.ping(reconnect=True)
    auth_cursor = connection.cursor()
    res = {"valid": None}
    data = request.get_json()
    sql = f"select * from `trans`.`user` where id = '{userToken}'"
    print(sql)
    auth_cursor.execute(sql)
    connection.commit()
    user = list(auth_cursor.fetchall())
    print(user)

    if user:
        res["valid"] = True
        USER_ID = userToken
    else:
        res["valid"] = False
    # data = request.get_json()
    # res = {"valid": None}
    # res["valid"] = True if data["token"] in tokens else False
    return jsonify(res)


@app.route("/token", methods=['GET'])
def token():
    link = "https://prod.liveshare.vsengsaas.visualstudio.com/join?B69307148D8336C7491A3DE0E7422A5176BD"
    return "<a href='"+link+"'>"+link+"</a>"

@app.route("/exampleTable", methods=['GET'])
def exampleTable():
    connection.ping(reconnect=True)
    sql = "select * from `trans`.user"
    print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    users = cursor.fetchall()
    
    exampleDatasets = []
    for user in users:
        try:
            sql = "select * from `" + str(user[0]) + "`.`dataset` WHERE is_public = 1"
            cursor.execute(sql)
            userDatasets = cursor.fetchall()
            userDatasets = list(userDatasets)
            
            for userDataset in userDatasets:
                exampleTablesTags = [
                    "datasetId",
                    "datasetName",
                    "datasetUnit",
                    "datasetStart",
                    "datasetEnd",
                    "datasetNote",
                    "datasetAddDate",
                    "datasetPublic"
                ]
                exampleTableData = {}
                for i in range(len(exampleTablesTags)):
                    exampleTableData[exampleTablesTags[i]] = userDataset[i]
                exampleTableData['user'] = str(user[0])
                exampleDatasets.append(exampleTableData)
        except Exception as e:
            print(e)
            print("But still good~")
    connection.commit()
    print("exampleTable")
    return jsonify(exampleDatasets)

@app.route("/customizeTable", methods=['OPTIONS','POST'])
def customizeTable():
    cursor = connection.cursor()
    userToken, datasetID = getTokenId(request)
    if not userToken:
        return jsonify({"Auth":"ERROR"}),401
    connection.ping(reconnect=True)
    sql = f"select * from `{userToken}`.`dataset`"
    try:
        cursor.execute(sql)
    except Error:
        print(Error)
    customizeDatas = list(cursor.fetchall())

    customizeDataset = []
    for customizeData in customizeDatas:
        customizeTableTags = [
            "datasetID",
            "datasetName",
            "datasetUnit",
            "datasetStart",
            "datasetEnd",
            "datasetNote",
            "datasetAddDate",
            "datasetPublic"
        ]
        customizeTableDatas = {}
        for i in range(len(customizeTableTags)):
            customizeTableDatas[customizeTableTags[i]]= customizeData[i]
        customizeDataset.append(customizeTableDatas)
        print(customizeDataset)
    return jsonify(customizeDataset)

@app.route("/sendMail")
def sendMail():
    userToken, datasetID = getTokenId(request)
    if not userToken and not datasetID:
        return jsonify({"Auth":"ERROR"}),401
    
    import smtplib

    gmail_user = 'subjecttrans@gmail.com'
    gmail_password = 'im39project'

    sent_from = gmail_user
    to = ['joannechen912@gmail.com']
    subject = 'Lorem ipsum dolor sit amet'
    body = 'consectetur adipiscing elit'

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)
        
@app.route("/contact", methods=['OPTIONS','POST'])
def contact():
    cursor = connection.cursor()
    email = request.form.get('email', False)
    name = request.form.get('name', False)
    topic = request.form.get('topic', False)
    messege = request.form.get('messege', 'NULL')
    if not email or not name or not topic:
        return jsonify({"status":"Data not complete"}),401

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = f"INSERT INTO `trans`.`contact_info` (name, email, topic, message, datetime) values ('{name}','{email}','{topic}','{messege}','{now}')"
    print(sql)
    cursor.execute(sql)
    connection.commit()

    return jsonify({"status":"success"})
    
if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.debug = True
    # 正式環境註解上面這行
    if connection:
        print("conneted")
    else:
        print("Connect ERROR")
    app.run(host="0.0.0.0", port="50000")
