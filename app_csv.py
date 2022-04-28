from flask import Blueprint, request, jsonify
import pandas as pd
import json
from app_db import db_methods,getTokenId


csv_apis = Blueprint('csv_apis', __name__)


@csv_apis.route("/factorRankcsv",methods=['GET','OPTIONS','POST'])
def factorcsv():
    csv = pd.read_csv("rankTable.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))


@csv_apis.route("/degreecsv",methods=['GET','OPTIONS','POST'])
def degreecsv():
    csv = pd.read_csv("degree_table.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))


@csv_apis.route("/closenesscsv",methods=['GET','OPTIONS','POST'])
def closenesscsv():
    csv = pd.read_csv("closeness_table.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))


@csv_apis.route("/layercsv",methods=['GET','OPTIONS','POST'])
def layercsv():
    csv = pd.read_csv("layertable.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))

@csv_apis.route("/isolationcsv",methods=['GET','OPTIONS','POST'])
def isolationcsv():
    csv = pd.read_csv("isolation_table.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))


@csv_apis.route("/resultcsv",methods=['GET','OPTIONS','POST'])
def resultcsv():
    csv = pd.read_csv("result_table.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))

@csv_apis.route("/basiccsv",methods=['GET','OPTIONS','POST'])
def basiccsv():
    csv = pd.read_csv("basic_table.csv")
    print(csv)
    jdata = csv.to_json(orient="records")
    return jsonify(json.loads(jdata))
