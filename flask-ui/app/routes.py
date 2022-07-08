from flask import render_template, redirect, url_for, send_from_directory, request
from app import app

@app.route('/')
def index():
    return render_template("base.html")

#Route for storing static items
def static_dir(path):
    return send_from_directory('static', path)