from flask import render_template
from . import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/returns')
def returns():
    return render_template('returns.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/bookclub')
def bookclub():
    return render_template('bookclub.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
