import os
import markdown
import sqlite3
from flask import render_template, render_template_string, Blueprint, redirect, g, request
from .models import Writeup
from sqlalchemy import desc

app = Blueprint('app', __name__)

def db_connect():
    conn = sqlite3.connect('instance/database.db')
    return conn

from flask import request, render_template
from sqlalchemy import desc, asc

@app.route('/', methods=['GET'])
def home():
    writeups_query = Writeup.query

    selected_difficulties = request.args.getlist('difficulty')
    selected_platforms = request.args.getlist('platform')

    if selected_difficulties:
        writeups_query = writeups_query.filter(Writeup.difficulty.in_(selected_difficulties))

    if selected_platforms:
        writeups_query = writeups_query.filter(Writeup.platform.in_(selected_platforms))

    posted = request.args.get('posted')
    created = request.args.get('created')

    if posted == 'newest':
        writeups_query = writeups_query.order_by(desc(Writeup.posted))
    elif posted == 'oldest':
        writeups_query = writeups_query.order_by(asc(Writeup.posted))

    if created == 'newest':
        writeups_query = writeups_query.order_by(desc(Writeup.created))
    elif created == 'oldest':
        writeups_query = writeups_query.order_by(asc(Writeup.created))

    writeups = writeups_query.order_by(Writeup.posted.desc()).all()

    return render_template("home.html", writeups=writeups, 
                           selected_difficulties=selected_difficulties, 
                           selected_platforms=selected_platforms,
                           posted=posted,
                           created=created)


@app.route('/about')
def about():
    return render_template("about.html")

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