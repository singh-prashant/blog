from app import application as app
from flask import render_template, request
@app.route('/')
def homepage():
    list_group_item = [{'url': "/indianeconomy", 'title': 'Indian Economy'},{'url':"banking-awareness", 'title': 'Banking Awareness'}, {'url':'/ifsc-locator','title':'IFSC Locator'}, {'url':'/micr-locator','title':'MICR Locator'}]
    name = request.args.get('name')
    number = request.args.get('number')
    return render_template("homepage.html", name=name, number=number, list_group_item=list_group_item )

@app.route('/banking-awareness')
def banking_awareness():
    return "This page is for Banking Awareness."

@app.route('/indianeconomy')
def indian_economy():
    return "This page is for Indian Economy."