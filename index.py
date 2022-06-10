from flask import Flask, jsonify, request
import utils

app = Flask(__name__)


@app.route("/categories", methods=["GET"])
def get_categories():
    rows = utils.get_all("SELECT * FROM category")
    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "name": r[1],
            "url": r[2]
        })

    return jsonify({"categories": data})


@app.route("/news/all", methods=["GET"])
def get_news():
    rows = utils.get_all("SELECT * FROM news")
    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "subject": r[1],
            "description": r[2],
            "image": r[3],
            "original_url": r[4]
        })

    return jsonify({"new": data})


@app.route("/news", methods=["GET"])
def test():
    pageindex = request.args.get("pageindex")
    pagesize = request.args.get("pagesize")
    print(pageindex)
    rows = utils.test2(pageindex, pagesize)
    data = []
    for r in rows:
        data.append({
            "ROWNUMBER": r[0],
            "TOTALNUMBERCOUNT": r[1],
            "id": r[2],
            "subject": r[3],
            "description": r[4],
            "image": r[5],
            "original_url": r[6]
        })

    return jsonify({"news": data})


@app.route("/news/add", methods=["POST"])
def insert_news():
    pass


if __name__ == "__main__":
    app.run()
