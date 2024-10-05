from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash

login_route = Blueprint('login',__name__)



@login_route.route('/')
def login_template():
    return render_template('indexL.html')


