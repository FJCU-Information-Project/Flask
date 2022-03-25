from email.policy import HTTP
from flask import Flask, render_template, request, jsonify, redirect, template_rendered
from flask_cors import CORS
import os
import pymysql
import pandas as pd
import json
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename

tokens = [
    "12345678",
    "ABCDEFGH"
]

app = Flask(__name__
            ,static_url_path="/trans"
            ,static_folder = "../trans/docs")
            # 用來設定說
            
auth = HTTPBasicAuth()
api = Api(app)
# CORS(app, resources={"/*": {"origins": "*"}})
CORS(app)

UPLOAD_FOLDER = "../temp"
ALLOWED_EXTENSIONS = set(['csv'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Define Rscipt Path
Rscript = "E:\\R-4.1.2\\bin\\Rscript.exe "
#Rscript = "Rscript "
#Rscript = "/usr/local/bin/Rscript "
snaPath = ".." + os.sep + "sna" + os.sep
# Define-------------
print("Rscript Path:",Rscript)
print("sna Path:",snaPath)

conn = pymysql.connect(host='140.136.155.121', port=50306,
                    user='root', passwd='IM39project', db='trans')
cursor = conn.cursor()


@app.route("/")
def index():
    name = request.args.get("name")
    return render_template("index.html", name=name)


@app.route("/receive")
def receive():
    node = request.args.get("node")
    command = Rscript + snaPath + "snaRank10.R " + node
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/snaRank10.html')


@app.route("/closenessReceive")
def closenessreceive():
    node = request.args.get("node")
    command = Rscript + snaPath + "sna_closeness.R " + node
    print(command)
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/closeness.html')


@app.route("/degreeReceive")
def degreereceive():
    node = request.args.get("node")
    command = Rscript + snaPath + "sna_degree.R " + node
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/degree.html')


@app.route("/overallReceive")
def overallreceive():
    command = Rscript + snaPath + "sna_all.R "
    res = os.system(command)
    print(res)
    return redirect('sna_graph/overall.html')


@app.route("/factorRankReceive")
def factorreceive():
    node = request.args.get("node")
    command = Rscript + snaPath + "snaRank10.R " + node
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/snaRank10.html')


@app.route("/layerReceive")
def layerreceive():
    node = request.args.get("node")
    print("Layer Receive :", node)
    csv_command = " python " + snaPath + "layer.py " + str(node)
    print("csv_command:",csv_command)
    graph_command = Rscript + snaPath + "sna_layer.R " + str(node)
    print("graph_command:",graph_command)
    csv_res = os.system(csv_command)
    print("csv_res:",csv_res)
    graph_res = os.system(graph_command)
    print("graph_res:",graph_res)
    return redirect('sna_graph/layer.html')


@app.route("/resultReceive")
def resultreceive():
    node = request.args.get("node")
    rank = request.args.get("rank")
    command = Rscript + snaPath + "sna_result.R " + node + " " + rank
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/result.html')

@app.route("/isolationReceive")
def isolationreceive():
    node = request.args.get("node")
    command = Rscript + snaPath + "sna_isolation.R " + node
    res = os.system(command)
    return redirect('sna_graph/isolation.html')


@app.route("/attributes")
def attributes():
    cursor.execute("select * from attribute")
    attributes = cursor.fetchall()

    attributeData = []
    for i in attributes:
        attribute = {}
        attribute["value"] = i[0]
        attribute["label"] = i[1]

        cursor.execute("select * from node where attribute =" + str(i[0]))
        nodes = cursor.fetchall()
        attribute["children"] = []
        for j in nodes:
            node = {}
            node["value"] = j[0]
            node["label"] = j[1]
            attribute["children"].append(node)
        attributeData.append(attribute)

    conn.commit()
    print(jsonify(attributeData))
    return jsonify(attributeData)


@app.route("/resultAttributes")
def resultattributes():
    cursor.execute("SELECT * FROM trans.injury_level;")
    resultAttributes = cursor.fetchall()

    resultAttributeData = []
    for i in resultAttributes:
        resultAttribute = {}
        resultAttribute["value"] = i[0]
        resultAttribute["label"] = i[1]

        resultAttributeData.append(resultAttribute)

    conn.commit()
    print(jsonify(resultAttributeData))
    return jsonify(resultAttributeData)


@app.route("/nodes")
def nodes():
    cursor.execute("select * from node")
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


@app.route("/factorRankcsv")
def factorcsv():
    csv = pd.read_csv("rankTable.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))


@app.route("/degreecsv")
def degreecsv():
    csv = pd.read_csv("degree_table.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))


@app.route("/closenesscsv")
def closenesscsv():
    csv = pd.read_csv("closeness_table.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))


@app.route("/layercsv")
def layercsv():
    csv = pd.read_csv("layer_table.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))

@app.route("/isolationcsv")
def isolationcsv():
    csv = pd.read_csv("isolation_table.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))


@app.route("/resultcsv")
def resultcsv():
    csv = pd.read_csv("result_table.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))

@app.route("/auth", methods=['POST'])
def auth():
    data = request.get_json()
    res = {"valid": None}
    res["valid"] = True if data["token"] in tokens else False
    return jsonify(res)

@app.route("/token")
def token():
    link = "https://prod.liveshare.vsengsaas.visualstudio.com/join?7EEB108A1D38E961642A6D6AA362C14F03BC"
    return "<a href='"+link+"'>"+link+"</a>"

@app.route("/uploadDatasets", methods=['POST'])
def uploadDatasets():
    allRet = []
    nameLists = ["nodeFileName","attributeFileName","resultFileName","resultAttributeFileName"]
    
    for nameOfUplaodFile in nameLists:
        ret = {
            "status": "No File"
        }
        try:
            uploadFile = request.files[nameOfUplaodFile]
        except:
            allRet.append(ret)
            continue
        if uploadFile and allowed_file(uploadFile.filename):
            print("File name:",uploadFile.filename)
            ret["filename"] = uploadFile.filename
            uploadFile.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(uploadFile.filename)))
            print("Upload File")
            ret["status"] = "Upload"
        else:
            print("No file and format error")
            ret["status"] = "No file and format error"
        allRet.append(ret)
    
    return jsonify(allRet)

@app.route("/uploadDatasetInfo")
def uploadDatasetInfo():
    all_dataset = []

    dataset = {
        "datasetName": "",
        "datasetUnit": "",
        "datasetPeriod": "",
        "datasetNote": "",
        "datasetPublic": ""
    }
    datasetInfo = ["datasetName", "datasetUnit", "datasetPeriod", "datasetNote", "datasetPublic"]

    for i in range(len(datasetInfo)):
        dataset[datasetInfo[i]] = request.form.get(datasetInfo[i])

    #for i in dataset:
    #    cursor.execute("INSERT INTO dataset VALUES ()")
    

    all_dataset.append(dataset)
    return jsonify(all_dataset)

@app.route("/addDataset")
def addDataset():
    # import ../database/correct process/crate table.py
    return "Null"
    # 先不要把syntax用壞
    # 我要修小羊的東西
    # 喔喔喔好喔

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
