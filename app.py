from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
# import os
import pymysql

app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": "*"}})


conn = pymysql.connect(host='140.136.155.121', port=50306, user='root', passwd='IM39project', db='trans')
cursor = conn.cursor()

@app.route("/")
def index():
    name = request.args.get("name")
    return render_template("index.html", name=name)

@app.route("/attributes")
def attributes():
    cursor.execute("select * from attribute")
    attribute = cursor.fetchall()

    attributeData = []
    for i in attribute:
        result = {}
        result["id"] = i[0]
        result["attribute"] = i[1]
        result["attribute_eng"] = i[3]
        attributeData.append(result)
        
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

@app.route("/sna_graph")
def sna():
    return render_template("1113_test_1.html")

# @app.route("/csv",method="post")
# def csv():
#     max = 1
#     os.system("e:/dsd/ds/Rscrippt.exe sna.R " + max)
#     ret.status = "OK"
#     ret.data = "data"
#     return jsontify(ret)



if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.debug = True
    # 正式環境註解上面這行
    app.run()