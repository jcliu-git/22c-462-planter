from flask import Flask, request, g
import sys
import json
import sqlite3

sys.path.append("../")
import contract.contract as contract

DATABASE = ":memory:"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


app = Flask(__name__)

state = contract.DefaultHubState


@app.route("/fetch", methods=["GET"])
def fetch():
    ret = json.dumps(state, cls=contract.ContractEncoder)
    return ret


@app.route("/update", methods=["POST"])
def update():
    message = request.get_json()
    state = message
    return True
