from flask import Blueprint, request, jsonify
import pandas as pd
import json

csv_apis = Blueprint('csv_apis', __name__)


@csv_apis.route("/factorRankcsv")
def factorcsv():
    csv = pd.read_csv("rankTable.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))


@csv_apis.route("/degreecsv")
def degreecsv():
    csv = pd.read_csv("degree_table.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))


@csv_apis.route("/closenesscsv")
def closenesscsv():
    csv = pd.read_csv("closeness_table.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))


@csv_apis.route("/layercsv")
def layercsv():
    csv = pd.read_csv("layertable.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))

@csv_apis.route("/isolationcsv")
def isolationcsv():
    csv = pd.read_csv("isolation_table.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))


@csv_apis.route("/resultcsv")
def resultcsv():
    csv = pd.read_csv("result_table.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))
