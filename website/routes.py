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

from flask import request, render_template
from math import ceil

@app.route('/', methods=['GET'])
def home():
    writeups_query = Writeup.query

    selected_difficulties = request.args.getlist('difficulty')
    selected_platforms = request.args.getlist('platform')

    if selected_difficulties:
        writeups_query = writeups_query.filter(Writeup.difficulty.in_(selected_difficulties))

    if selected_platforms:
        writeups_query = writeups_query.filter(Writeup.platform.in_(selected_platforms))

    sort = request.args.get('sort')

    if sort == 'posted_new':
        writeups_query = writeups_query.order_by(desc(Writeup.posted))
    elif sort == 'posted_old':
        writeups_query = writeups_query.order_by(asc(Writeup.posted))
    elif sort == 'created_new':
        writeups_query = writeups_query.order_by(desc(Writeup.created))
    elif sort == 'created_old':
        writeups_query = writeups_query.order_by(asc(Writeup.created))

    per_page = 12
    page = request.args.get('page', 1, type=int)
    total_writeups = writeups_query.count()
    total_pages = ceil(total_writeups / per_page)

    writeups = writeups_query.order_by(Writeup.posted.desc()).offset((page - 1) * per_page).limit(per_page).all()

    pages = range(1, total_pages + 1)

    return render_template("home.html", writeups=writeups, 
                       selected_difficulties=selected_difficulties, 
                       selected_platforms=selected_platforms,
                       sort=sort,
                       pages=pages,
                       current_page=page,
                       total_pages=total_pages,)

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

    latest_writeups = Writeup.query.order_by(Writeup.posted.desc()).limit(5).all()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "static", "writeups", writeup.url, "writeup.md")

    with open(file_path, 'r') as md_file:
        content = md_file.read()

    rendered_content = render_template_string(content)

    html_content = markdown.markdown(rendered_content)

    return render_template("writeup.html", writeup=writeup, html_content=html_content, latest_writeups=latest_writeups)

@app.route('/search', methods=['POST', 'GET'])
def search():
    value = request.form.get('writeup_name')
    writeups_query = Writeup.query

    if value:
        writeups_query = writeups_query.filter(Writeup.name.ilike(f"%{value}%"))
    else:
        writeups_query = writeups_query.order_by(Writeup.posted.desc())

    selected_difficulties = request.args.getlist('difficulty')
    if selected_difficulties:
        writeups_query = writeups_query.filter(Writeup.difficulty.in_(selected_difficulties))

    selected_platforms = request.args.getlist('platform')
    if selected_platforms:
        writeups_query = writeups_query.filter(Writeup.platform.in_(selected_platforms))

    sort = request.args.get('sort')
    if sort == 'posted_new':
        writeups_query = writeups_query.order_by(desc(Writeup.posted))
    elif sort == 'posted_old':
        writeups_query = writeups_query.order_by(asc(Writeup.posted))
    elif sort == 'created_new':
        writeups_query = writeups_query.order_by(desc(Writeup.created))
    elif sort == 'created_old':
        writeups_query = writeups_query.order_by(asc(Writeup.created))

    per_page = 12
    page = request.args.get('page', 1, type=int)
    total_writeups = writeups_query.count()
    total_pages = ceil(total_writeups / per_page)

    writeups = writeups_query.offset((page - 1) * per_page).limit(per_page).all()

    pages = range(1, total_pages + 1)

    return render_template(
        "home.html",
        writeups=writeups,
        selected_difficulties=selected_difficulties,
        selected_platforms=selected_platforms,
        sort=sort,
        pages=pages,
        current_page=page,
        total_pages=total_pages,
        search_query=value,
    )
