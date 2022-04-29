from flask import Blueprint, request, redirect, jsonify
import os
from app_db import db_methods,getTokenId

receieves = Blueprint('receieves', __name__)

# Define Rscipt Path
Rscript = "E:\\R-4.1.2\\bin\\Rscript.exe "
#Rscript = "Rscript "
#Rscript = "/usr/local/bin/Rscript "
snaPath = ".." + os.sep + "sna" + os.sep
dbPath = ".." + os.sep + "database" + os.sep
# Define-------------
print("Rscript Path:",Rscript)
print("sna Path:",snaPath)
print("db Path:",dbPath)

@receieves.route("/receive",methods=['GET','OPTIONS','POST'])
def receive():
    userToken, datasetID = getTokenId(request)
    if not userToken or not datasetID:
        return jsonify({"Auth":"ERROR"}),401

    node = request.args.get("node")
    command = Rscript + snaPath + "snaRank10.R " + node + " " + userToken + " " + datasetID
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/snaRank10.html')


@receieves.route("/closenessReceive",methods=['GET','OPTIONS','POST'])
def closenessreceive():
    userToken, datasetID = getTokenId(request)
    if not userToken or not datasetID:
        return jsonify({"Auth":"ERROR"}),401

    # TO CHECK: Rscript參數名稱及需要兩個參數
    node = request.args.get("node")
    command = Rscript + snaPath + "sna_closeness.R " + node
    print(command)
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/closeness.html')


@receieves.route("/degreeReceive",methods=['GET','OPTIONS','POST'])
def degreereceive():
    userToken, datasetID = getTokenId(request)
    if not userToken or not datasetID:
        return jsonify({"Auth":"ERROR"}),401

    # TO CHECK:Rscript參數名稱要有兩個吧
    node = request.args.get("node")
    command = Rscript + snaPath + "sna_degree.R " + node
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/degree.html')


@receieves.route("/overallReceive",methods=['GET','OPTIONS','POST'])
def overallreceive():
    userToken, datasetID = getTokenId(request)
    if not userToken or not datasetID:
        return jsonify({"Auth":"ERROR"}),401
        
    
    command = Rscript + snaPath + "sna_all.R " + " " + userToken + " " + datasetID
    res = os.system(command)
    print(res)
    return redirect('sna_graph/overall.html')


@receieves.route("/factorRankReceive",methods=['GET','OPTIONS','POST'])
def factorreceive():
    userToken, datasetID = getTokenId(request)
    if not userToken or not datasetID:
        return jsonify({"Auth":"ERROR"}),401

    node = request.args.get("node")
    command = Rscript + snaPath + "snaRank10.R " + node  + " " + userToken + " " + datasetID
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/snaRank10.html')


@receieves.route("/layerReceive",methods=['GET','OPTIONS','POST'])
def layerreceive():
    userToken, datasetID = getTokenId(request)
    if not userToken or not datasetID:
        return jsonify({"Auth":"ERROR"}),401

    node = request.args.get("node")
    print("Layer Receive :", node)
    
    # PROBLEM 參數現在是直接寫死的
    csv_command = " python " + snaPath + "layer.py " + str(node)
    print("csv_command:",csv_command)
    graph_command = Rscript + snaPath + "sna_layer.R " + str(node)
    print("graph_command:",graph_command)
    csv_res = os.system(csv_command)
    print("csv_res:",csv_res)
    graph_res = os.system(graph_command)
    print("graph_res:",graph_res)
    return redirect('sna_graph/layer.html')


@receieves.route("/resultReceive",methods=['GET','OPTIONS','POST'])
def resultreceive():
    userToken, datasetID = getTokenId(request)
    if not userToken or not datasetID:
        return jsonify({"Auth":"ERROR"}),401

    node = request.args.get("node")
    rank = request.args.get("rank")
    # TOCHECK: rank在 rscript裡面沒有對應的參數
    command = Rscript + snaPath + "sna_result.R " + node + " " + rank  + " " + userToken + " " + datasetID
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/result.html')

@receieves.route("/basicReceive",methods=['GET','OPTIONS','POST'])
def basicreceive():
    userToken, datasetID = getTokenId(request)
    if not userToken or not datasetID:
        return jsonify({"Auth":"ERROR"}),401

    node = request.args.get("node")
    # TOCHECK: rank在 rscript裡面沒有對應的參數
    command = Rscript + snaPath + "sna_basic.R " + node + " " + userToken + " " + datasetID
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/result.html')

@receieves.route("/isolationReceive",methods=['GET','OPTIONS','POST'])
def isolationreceive():
    userToken, datasetID = getTokenId(request)
    if not userToken or not datasetID:
        return jsonify({"Auth":"ERROR"}),401

    node = request.args.get("node")
    command = Rscript + snaPath + "sna_isolation.R " + node  + " " + userToken + " " + datasetID
    res = os.system(command)
    return redirect('sna_graph/isolation.html')