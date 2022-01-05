
from flask import Flask, render_template, request, jsonify, redirect
from flask_cors import CORS
import os
import pymysql
import pandas as pd
import json

app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": "*"}})


conn = pymysql.connect(host='140.136.155.121', port=50306, user='root', passwd='IM39project', db='trans')
cursor = conn.cursor()

@app.route("/")
def index():
    name = request.args.get("name")
    return render_template("index.html", name=name)

@app.route("/receive")
def receive():
    node = request.args.get("node")
    # node+=node
    command = "E:\\R-4.1.2\\bin\\Rscript.exe E:\\GitHub\\sna\\snaRank10.R " + node
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/snaRank10.html')

@app.route("/closenessReceive")
def closenessreceive():
    node = request.args.get("node")
    # node+=node
    command = "E:\\R-4.1.2\\bin\\Rscript.exe E:\\GitHub\\sna\\sna_closeness.R " + node
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/closeness.html')

@app.route("/degreeReceive")
def degreereceive():
    node = request.args.get("node")
    # node+=node
    command = "E:\\R-4.1.2\\bin\\Rscript.exe E:\\GitHub\\sna\\sna_degree.R " + node
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/degree.html')

@app.route("/overallReceive")
def overallreceive():
    command = "E:\\R-4.1.2\\bin\\Rscript.exe E:\\GitHub\\sna\\sna_all.R "
    res = os.system(command)
    print(res)
    return redirect('sna_graph/overall.html')

@app.route("/factorRankReceive")
def factorreceive():
    node = request.args.get("node")
    # node+=node
    command = "E:\\R-4.1.2\\bin\\Rscript.exe E:\\GitHub\\sna\\snaRank10.R " + node
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/snaRank10.html')


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

@app.route("/nodes")
def nodes():
    cursor.execute("select * from node")
    row = cursor.fetchall()

    jsonData = []
    for i in row:
        result = {}    # temp store one jsonObject
        result["id"] = i[0]# 将row中的每个元素，追加到字典中。　
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
def sna_graph_f_p_f(folder,paths,filenames):
    print(folder)
    print(paths)
    print(filenames)
    string = folder + "/" + paths + "/" + filenames
    return render_template(string)

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

if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.debug = True
    # 正式環境註解上面這行
    app.run(host="0.0.0.0",port="5000")

