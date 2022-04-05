from flask import Blueprint, request, jsonify
import threading
from werkzeug.utils import secure_filename
import os
import threading

db_methods = Blueprint('db_methods', __name__)

# user_id = "304u39481-20"
# dataset_id = 1
# threads = []

#USER_ID = "304u39481-20"
USER_ID = "9840-menqwk"
DATASET_ID = 1
ALLOWED_EXTENSIONS = set(['csv'])
UPLOAD_FOLDER = "../temp"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@db_methods.route("/uploadDatasets", methods=['POST'])
def uploadDatasets():
    allRet = []
    nameLists = ["nodeFileName","attributeFileName","resultFileName","resultAttributeFileName"]
    
    for nameOfUploadFile in nameLists:
        ret = {
            "status": "No File"
        }
        try:
            uploadFile = request.files[nameOfUploadFile]
            print("ewifoefniwef")
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

@db_methods.route("/uploadFile", methods = ['POST'])
def uploadFile():
    all_ret = []

    ret = {
        "status" : "No file"
    }

    try:
        datasetFiles = request.files['caseFile']
    except:
        all_ret.append(ret)

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

@db_methods.route("/deleteDataset")
def deleteDataset():
    return "success"

@db_methods.route("/createTable")
def createTable():
    try:
        import database.correctProcess.create_tables
        return "sucess"
    except:
        return "ERROR by DB"

@db_methods.route("/addDataset")
def addDataset():
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
    return ret

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
