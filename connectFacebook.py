# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 00:24:23 2016

@author: strider
"""
import os
from flask import Flask, render_template, send_from_directory
from flask import url_for, request, session, redirect
from flask_oauth import OAuth

FACEBOOK_APP_ID = '224610534627665'
FACEBOOK_APP_SECRET = '24152411e6be858151ddf3d3f2673af4'

oauth = OAuth()
app = Flask(__name__)

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': ('email, ')}
)

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)

@app.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    return redirect(next_url)

@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('index'))
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.secret_key = 'super secret key'

    #sess.init_app(app)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
