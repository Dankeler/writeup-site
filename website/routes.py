import os
from flask import render_template, render_template_string, Blueprint, redirect, g, request
from .models import Writeup
import markdown
import sqlite3

app = Blueprint('app', __name__)

def db_connect():
    conn = sqlite3.connect('instance/database.db')
    return conn

@app.route('/', methods=['GET', 'POST'])
def home():
    writeups = Writeup.query.order_by(Writeup.posted.desc()).all()
    selected_difficulties = request.form.getlist('difficulty') if request.method == 'POST' else []

    if selected_difficulties:
        writeups = Writeup.query.filter(Writeup.difficulty.in_(selected_difficulties)).all()

    return render_template("home.html", writeups=writeups)

@app.route('/writeup')
def writeups():
    return redirect("/")

@app.route('/writeup/')
def redirect_home():
    return redirect('/')

@app.route('/writeup/<string:url>')
def writeup(url):
    writeup = Writeup.query.get_or_404(url)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "static", "writeups", writeup.url, "writeup.md")

    with open(file_path, 'r') as md_file:
        content = md_file.read()

    rendered_content = render_template_string(content)

    html_content = markdown.markdown(rendered_content)

    return render_template("writeup.html", writeup=writeup, html_content=html_content)

@app.route('/search', methods=["POST"])
def search():
    value = request.form.get('writeup_name')
    connection = db_connect()

    query = "SELECT * FROM writeup WHERE name LIKE ?"
    results = connection.execute(query, ('%' + value + '%',))

    column_names = [description[0] for description in results.description]

    writeups = [dict(zip(column_names, row)) for row in results.fetchall()]

    connection.close()
    
    return render_template("home.html", writeups=writeups)

