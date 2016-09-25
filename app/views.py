from app import application as app
from forms import LoginForm
from flask_login import login_user, logout_user, login_required
from app import login_manager
from flask import render_template, request,flash, redirect, url_for


@app.route('/')
def homepage():
    list_group_item = [{'url': "/indianeconomy", 'title': 'Indian Economy'},{'url':"banking-awareness", 'title': 'Banking Awareness'}, {'url':'/ifsc-locator','title':'IFSC Locator'}, {'url':'/micr-locator','title':'MICR Locator'}]
    name = request.args.get('name')
    number = request.args.get('number')
    return render_template("homepage.html", name=name, number=number, list_group_item=list_group_item )


@app.route("/login/", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            login_user(form.user, remember=form.remember_me.data)
            flash('Successfully logged in as %s'%form.user.email, "success")
            return redirect(request.args.get("next") or url_for("homepage"))

    return render_template("login.html", form=form, title="Log in")


@app.route("/logout/")
def logout():
    logout_user()
    flash("You have successfully log out", "success")
    return redirect(request.args.get('next') or url_for('homepage'))



@app.route('/banking-awareness')
def banking_awareness():
    return "This page is for Banking Awareness."

@app.route('/indianeconomy')
def indian_economy():
    return "This page is for Indian Economy."