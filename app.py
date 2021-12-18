from flask import Flask, render_template
import os

app = Flask("__name__");

@app.route("/")
def index():
    name = request.args.get("name")
    return render_template("index.html", name=name)

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