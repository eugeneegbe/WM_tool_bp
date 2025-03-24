import json

from flask import flash, Blueprint, redirect, request, session, url_for, make_response, jsonify
from flask_login import current_user, login_user, logout_user
import mwoauth

from tool import app, config, db
from tool.models import User
from tool.main.utils import is_commit_successfull
from tool.users.utils import generate_random_token
from flask_login import current_user, login_user, logout_user


users = Blueprint('users', __name__)


users.route('/api/set-login-url', methods=['POST', 'GET'])
def setLoginUrl():
    session['next_url'] = request.args.get('url')
    return "success"


@users.route('/login')
def login():
    """Initiate an OAuth login.

    Call the MediaWiki server to get request secrets and then redirect the
    user to the MediaWiki server to sign the request.
    """
    if current_user.is_authenticated:
        print(current_user.is_authenticated)
        return redirect(url_for('main.home'))
    else:
        consumer_token = mwoauth.ConsumerToken(
            config['CONSUMER_KEY'], config['CONSUMER_SECRET'])
        try:
            redirect_string, request_token = mwoauth.initiate(
                config['OAUTH_MWURI'], consumer_token)
        except Exception:
            app.logger.exception('mwoauth.initiate failed')
            return redirect(url_for('main.home'))
        else:
            session['request_token'] = dict(zip(
                request_token._fields, request_token))
            user = User.query.filter_by(username=session.get('username', None)).first()
            if user and user.username is not None:
                login_user(user)
            return redirect(redirect_string)


@users.route('/oauth-callback')
def oauth_callback():
    """OAuth handshake callback."""
    if 'request_token' not in session:
        flash('OAuth callback failed. Are cookies disabled?')
        return redirect(url_for('main.home'))

    consumer_token = mwoauth.ConsumerToken(
        config['CONSUMER_KEY'], config['CONSUMER_SECRET'])

    try:
        access_token = mwoauth.complete(
            config['OAUTH_MWURI'],
            consumer_token,
            mwoauth.RequestToken(**session['request_token']),
            request.query_string)
        identity = mwoauth.identify(
            config['OAUTH_MWURI'], consumer_token, access_token)
    except Exception:
        app.logger.exception('OAuth authentication failed')
    else:
        session['access_token'] = dict(zip(
            access_token._fields, access_token))
        session['username'] = identity['username']
        
        # Add current user to database if they don't exist
        user = User.query.filter_by(username=session.get('username')).first()
        if not user:
            new_user = User(username = session['username'])
            db.session.add(new_user)

            if is_commit_successfull():

                if session.get('next_url'):
                    next_url = session.get('next_url')
                    session.pop('next_url', None)
                    return redirect(next_url)
                return redirect(url_for('main.home'))

            else:
                return {
                    'message': 'Adding user to database faile',
                    'status': 'failure'
                    }, 403
        else:
            return redirect(url_for('main.home'))
            

@users.route('/logout')
def logout():
    """Log the user out by clearing their session."""
    logout_user()
    session.clear()
    flash('See you next time!', 'info')
    return redirect(url_for('main.home'))


@users.route('/api/v1/current_user', methods=['GET'])
def get_current_user_info():
    try:
        user_infomration = {}
        user_info_obj = {}
        user_info_obj['username'] = session['username']
        user_infomration['user'] = user_info_obj
        response = make_response(user_infomration)
    except Exception as e:
        return {
                'message': 'User not logged in',
                'status': 'failure'
                }, 403

    return response
