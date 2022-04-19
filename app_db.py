from flask import Blueprint, request, jsonify
from flask_cors import CORS
import threading
from werkzeug.utils import secure_filename
import os
import threading
import mysql.connector as conn

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

def getTokenId(r):
    userToken = r.form.get('token', False)
    datasetID = r.form.get('dataset', False)
    return userToken, datasetID

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@db_methods.route("/uploadDatasets", methods=['POST'])
def uploadDatasets():
    allRet = []
    nameLists = ["nodeFileName","attributeFileName","resultFileName","resultAttributeFileName"]
    
    userToken, datasetID = getTokenId(request)
    if not userToken or not datasetID:
        return jsonify({"Auth":"ERROR"}),401
    
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
            print("Upload File")
            ret["status"] = "Upload"
        else:
            print("No file and format error")
            ret["status"] = "No file and format error"
        allRet.append(ret)
    
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
    try:
        import database.correctProcess.create_tables
        return "sucess"
    except:
        return "ERROR by DB"

@db_methods.route("/addDataset",methods=['GET','OPTIONS','POST'])
def addDataset():
    # userToken, datasetID = getTokenId(request)
    # if not userToken or not datasetID:
    #     return jsonify({"Auth":"ERROR"}),401

    datasetInfo = ["datasetName", "datasetUnit", "datasetPeriodStart", "datasetPeriodEnd", "datasetNote", "datasetPublic"]
    dataset = {}
    for item in datasetInfo:
        dataset[item] = request.form.get(item)

    #user_id = "304u39481-20"

    import database.correctProcess.create_schema as create_db
    ret = create_db.main(USER_ID)
    print("create scheme ",ret)
    
    import database.correctProcess.create_tables as insert_dataset_info
    datasetOfValues = list(dataset.values())
    print(datasetOfValues)
    ret = insert_dataset_info.main(USER_ID, datasetOfValues)
    print(ret)
    return jsonify(ret)

@db_methods.route("/insertFile")
def insertFile():
    #user_id = "304u39481-20"
    #dataset_id = 1
    # try:
    import database.correctProcess.insert_into_case as insertCase
    insertCase.main(USER_ID, DATASET_ID)
    return "sucess"
    #except:
        #return "ERROR by DB"

@db_methods.route("/relationship")
def relationship():
    user_id = "304u39481-20"
    dataset_id = 1
    threads = []
    try:
        import database.correctProcess.relationship as relationship
        relationship.main(USER_ID, DATASET_ID)
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
        import database.correctProcess.weight as weight
        weight.main(USER_ID, DATASET_ID)
        return "sucess"
    except:
        return "ERROR by DB"
