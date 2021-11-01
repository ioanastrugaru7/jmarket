from market import app
from flask import render_template, redirect, url_for, flash, request
from flask import request
import os
import json
from market.modules import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

     

@app.route("/login", methods=['GET', 'POST'])
def user_login_route():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Login successful! Welcome {attempted_user.username}', category='success')
            return redirect(url_for('market_route'))
        else: 
            flash('Incorrect username or password, please try again!', category='danger')
    return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def user_register_route():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, 
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'Account {user_to_create.username} has been successfully created', category='success')
        return redirect(url_for('market_route'))
    if form.errors != {}: 
        for err_msg in form.errors.values():
            flash(f'Error was encountered while trying to create your account {err_msg}', category='danger')
    return render_template('register.html', form=form) 


@app.route("/logout", methods=['GET', 'POST'])
def user_logout_route():
    logout_user()
    flash("Logout successful!", category='info')
    return redirect(url_for('home_route')) 

@app.route("/", methods=['GET', 'POST'])
def default_route():
    return render_template('home.html') 

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route("/home", methods=['GET', 'POST'])
def home_route():
    return  render_template('home.html')

@app.route("/market", methods=['GET', 'POST'])
@login_required
def market_route():
    purchase_form=PurchaseItemForm()
    selling_form=SellItemForm()
    if request.method == "POST":
        #Purchase Item
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash("Purchase successful!", category='success')
            else:
                flash(f"Not enough money in your wallet for purchasing {p_item_object.name}", category='danger')
        #Sell Item
        sold_item = request.form.get('sold_item')
        s_item_object= Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash("Sell is successfully completed!", category='success')
            else:
                flash(f"Selling {p_item_object.name} cannot be processed", category='danger')
        return redirect(url_for('market_route'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items=Item.query.filter_by(owner=current_user.id)
        return  render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


