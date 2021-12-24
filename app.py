from flask import Flask, render_template, request
from flask_cors import CORS
# import os
import pymysql
import json

app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": "*"}})

@app.route("/")
def index():
    name = request.args.get("name")
    return render_template("index.html", name=name)

@app.route("/attributes")
def attributes():
    conn = pymysql.connect(host='140.136.155.121', port=50306, user='root', passwd='IM39project', db='trans')

    attribute_cursor = conn.cursor()
    attribute_cursor.execute("select * from attribute")
    attribute = attribute_cursor.fetchall()

    attributeData = []
    for i in attribute:
        result = {}
        result["id"] = i[0]
        result["attribute"] = i[1]
        result["attribute_eng"] = i[3]
        attributeData.append(result)
        
    print(json.dumps(attributeData, ensure_ascii=False))
        # return json.dumps(attributeData, ensure_ascii=False)

    conn.commit()
    attribute_cursor.close()
    conn.close()
    return json.dumps(attributeData,ensure_ascii=False)

@app.route("/nodes")
def nodes():
    conn = pymysql.connect(host='140.136.155.121', port=50306, user='root', passwd='IM39project', db='trans')
    cursor = conn.cursor()
    cursor.execute("select * from node")
    row = cursor.fetchall()

    jsonData = []

    for i in row:
        result = {}    # temp store one jsonObject
        result["id"] = i[0]# 将row中的每个元素，追加到字典中。　
        result["node"] = i[1]
        jsonData.append(result)

    conn.commit()
    cursor.close()
    conn.close()
    return json.dumps(jsonData,ensure_ascii=False)

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
    app.debug = True
    # 正式環境註解上面這行
    app.run()