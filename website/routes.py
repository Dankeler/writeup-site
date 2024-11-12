import os
from flask import render_template, render_template_string, Blueprint, redirect
from .models import Writeup
import markdown

app = Blueprint('app', __name__)


@app.route('/')
def home():
    writeups = Writeup.query.all()

    return render_template("home.html", writeups=writeups)

@app.route('/writeup')
def writeups():
    return redirect("/")

@app.route('/writeup/<string:name>')
def writeup(name):
    writeup = Writeup.query.get_or_404(name)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "writeups", writeup.name, writeup.md_file)

    with open(file_path, 'r') as md_file:
        content = md_file.read()

    rendered_content = render_template_string(content)

    html_content = markdown.markdown(rendered_content)

    return render_template("writeup.html", writeup=writeup, html_content=html_content)
        

