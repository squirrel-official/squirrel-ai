from flask import Flask, request, jsonify

app = Flask(__name__)


@app.get("/countries")
def get_countries():
    return jsonify("hello")
