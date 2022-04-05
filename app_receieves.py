from flask import Blueprint, request, redirect
import os

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

@receieves.route("/receive")
def receive():
    node = request.args.get("node")
    command = Rscript + snaPath + "snaRank10.R " + node
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/snaRank10.html')


@receieves.route("/closenessReceive")
def closenessreceive():
    node = request.args.get("node")
    command = Rscript + snaPath + "sna_closeness.R " + node
    print(command)
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/closeness.html')


@receieves.route("/degreeReceive")
def degreereceive():
    node = request.args.get("node")
    command = Rscript + snaPath + "sna_degree.R " + node
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/degree.html')


@receieves.route("/overallReceive")
def overallreceive():
    command = Rscript + snaPath + "sna_all.R "
    res = os.system(command)
    print(res)
    return redirect('sna_graph/overall.html')


@receieves.route("/factorRankReceive")
def factorreceive():
    node = request.args.get("node")
    command = Rscript + snaPath + "snaRank10.R " + node
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/snaRank10.html')


@receieves.route("/layerReceive")
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


@receieves.route("/resultReceive")
def resultreceive():
    node = request.args.get("node")
    rank = request.args.get("rank")
    command = Rscript + snaPath + "sna_result.R " + node + " " + rank
    res = os.system(command)
    print(res)
    print(node)
    return redirect('sna_graph/result.html')

@receieves.route("/isolationReceive")
def isolationreceive():
    node = request.args.get("node")
    command = Rscript + snaPath + "sna_isolation.R " + node
    res = os.system(command)
    return redirect('sna_graph/isolation.html')
