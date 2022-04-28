from flask import Blueprint, request, jsonify
from flask_cors import CORS
import threading
from werkzeug.utils import secure_filename
import os
import threading
import mysql.connector as conn
import createDataset.correctProcess.insert_into_dataset as insert_dataset_info
import createDataset.correctProcess.create_schema as create_db
import createDataset.correctProcess.basic_tables as basic_tables

from IMGlobal import USER_ID

db_methods = Blueprint('db_methods', __name__)

connection = conn.connect(
            host='140.136.155.121',
            user='root',
            password='IM39project',
            port='50306')

CORS(db_methods, resources={"/.*": {
    "origins": "*",
    "methods": "*",
    "headers": "*",
    "allow_headers": "*",
    "supports_credentials": True,
}})

# user_id = "304u39481-20"
# dataset_id = 1
# threads = []

#USER_ID = "304u39481-20"
#USER_ID = "9840-menqwk"
DATASET_ID = 1
ALLOWED_EXTENSIONS = set(['csv'])
UPLOAD_FOLDER = "../temp"
# UPLOAD_FOLDER = "createDataset/correctProcess"

def getTokenId(r):
    userToken = r.form.get('token', False)
    datasetID = r.form.get('dataset', False)
    return userToken, datasetID

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@db_methods.route("/uploadDatasets", methods=['POST'])
def uploadDatasets():
    allRet = []
    nameLists = ["nodeFileName","attributeFileName","resultFileName","resultAttributeFileName", "caseFileName"]
    
    # 前端按鈕尚未連接
    # userToken, datasetID = getTokenId(request)
    # print(userToken, datasetID)
    # if not userToken or not datasetID:
    #     return jsonify({"Auth":"ERROR"}),401
    cursor = connection.cursor()
    file_lst = []
    for nameOfUploadFile in nameLists:
        ret = {
            "status": "No File"
        }
        try:
            uploadFile = request.files[nameOfUploadFile]
        except:
            allRet.append(ret)
            continue
        if uploadFile and allowed_file(uploadFile.filename):
            print("File name:",uploadFile.filename)
            ret["filename"] = uploadFile.filename
            uploadFile.save(os.path.join(UPLOAD_FOLDER,secure_filename(uploadFile.filename)))
            file_lst.append(uploadFile.filename)
            print("Upload File")
            ret["status"] = "Upload"
        else:
            print("No file and format error")
            ret["status"] = "No file and format error"
        allRet.append(ret)
    # userToken, datasetID需要前端傳送
    basic_tables.insert_file(connection, cursor, "9860", 1, file_lst)
    print(file_lst)
    return jsonify(allRet)

@db_methods.route("/uploadFile",methods=['OPTIONS','POST'])
def uploadFile():

    if request.method == 'POST':
        all_ret = []

        ret = {
            "status" : "No file"
        }

        # try:
        datasetFiles = request.files['caseFile']
        # except:
            # all_ret.append(ret)

        if datasetFiles and allowed_file(datasetFiles.filename):
            print("File name:",datasetFiles.filename)
            ret["filename"] = datasetFiles.filename
            datasetFiles.save(os.path.join(UPLOAD_FOLDER,secure_filename(datasetFiles.filename)))
            print("Upload File")
            ret["status"] = "Upload"
        else:
            print("No flie and format error")
            ret["status"] = "No file and format error"
        all_ret.append(ret)
        
        return jsonify(all_ret)
    return "Not POST"

@db_methods.route("/deleteDataset",methods=['OPTIONS','POST'])
def deleteDataset():
    cursor = connection.cursor()
    userToken, datasetID = getTokenId(request)
    if not userToken or not datasetID:
        return jsonify({"Auth":"ERROR"}),401
    
    sqlTable = ["dataset", "attribute", "case", "file", "node", "relationship", "result", "result_attribute", "result_weight", "weight"]

    for i in sqlTable:
        if i == "dataset":
            sql = f"delete from `{userToken}`.{i} where id = {datasetID}"
        else:
            sql = f"delete from `{userToken}`.{i} where dataset = {datasetID}"

        print(sql)
        cursor.execute(sql)
        connection.commit()

    return "success"

@db_methods.route("/createTable")
def createTable():
    cursor = connection.cursor()
    userToken = 9860
    datasetID = 1
    # userToken, datasetID = getTokenId(request)
    # if not userToken or not datasetID:
    #     return jsonify({"Auth":"ERROR"}),401
    
    sql = f"select * from `{userToken}`.file where dataset = {datasetID}"
    print(sql)
    cursor.execute(sql)
    file = cursor.fetchall()
    print(file)

    for fileData in range(len(file)):
        #fileData = list(fileData)
        node = file[0][2]
        attribute = file[1][2]
        result = file[2][2]
        result_attribute = file[3][2]
        case = file[4][2]
    
    print(node)
    try:
        basic_tables.main(userToken, datasetID, attribute, node, result_attribute, result, case)
        return "sucess"
    except:
        return "ERROR by DB"

@db_methods.route("/addDataset",methods=['GET','OPTIONS','POST'])
def addDataset():
    userToken, datasetID = getTokenId(request)
    if not userToken or not datasetID:
        return jsonify({"Auth":"ERROR"}),401

    datasetInfo = ["datasetName", "datasetUnit", "datasetPeriodStart", "datasetPeriodEnd", "datasetNote", "datasetPublic"]
    dataset = {}
    for item in datasetInfo:
        dataset[item] = request.form.get(item)

    # user_id = "304u39481-20"
    
    ret = create_db.main(userToken)
    print("create scheme ",ret)
    
    datasetOfValues = list(dataset.values())
    print(datasetOfValues)

    # ToDo: startDate, endDate日期格式轉換
    name = datasetOfValues[0]
    unit = datasetOfValues[1]
    startDate = datasetOfValues[2]
    endDate = datasetOfValues[3]
    note = datasetOfValues[4]
    public = datasetOfValues[5]
    ret = insert_dataset_info.main(userToken, name, unit, startDate, endDate, note, public)
    print(ret)
    print("success")
    return jsonify({"datasetId":ret})

@db_methods.route("/insertCase")
def insertFile():
    cursor = connection.cursor()
    userToken, datasetID = getTokenId(request)
    if not userToken or not datasetID:
        return jsonify({"Auth":"ERROR"}),401
    #user_id = "304u39481-20"
    #dataset_id = 1
    # try:
    basic_tables.insert_case(cursor, USER_ID, DATASET_ID)
    return "sucess"
    #except:
        #return "ERROR by DB"

@db_methods.route("/relationship")
def relationship():
    user_id = "304u39481-20"
    dataset_id = 1
    threads = []
    try:
        import createDataset.correctProcess.relationship as weight
        relationship.relationship(USER_ID, DATASET_ID)
        t = threading.Thread(target = relationship.main, args = [USER_ID, DATASET_ID])
        t.start()
        threads.append(t)
        
        return "sucess (wait for thread)" + len(threads)
    except:
        return "ERROR by thread"

@db_methods.route("/relationshipStatus")
def relationsshipStatus():
    return 0

@db_methods.route("/resultWeight")
def weight():
    try:
        #user_id = "304u39481-20"
        #dataset_id = 1

        import createDataset.correctProcess.weight as weight
        weight.main(USER_ID, DATASET_ID)
        return "sucess"
    except:
        return "ERROR by DB"
