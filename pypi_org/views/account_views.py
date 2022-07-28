import flask

# Serve model as a flask application

import pickle
import numpy as np
from flask import Flask, request

model = None

def load_model():
    global model
    # model variable refers to the global variable
    #with open('iris_trained_model.pkl', 'rb') as f:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)


# from pypi_org.infrastructure import request_dict
from pypi_org.infrastructure.view_modifiers import response

# from pypi_org.services import user_service
# import pypi_org.infrastructure.cookie_auth as cookie_auth

blueprint = flask.Blueprint('account', __name__, template_folder='templates')


# ################### INDEX #################################


@blueprint.route('/account')
@response(template_file='account/index.html')
def index():
    # user_id = cookie_auth.get_user_id_via_auth_cookie(flask.request)
    # if user_id is None:
    #     return flask.redirect('/account/login')
    #
    # user = user_service.find_user_by_id(user_id)
    # if not user:
    #     return flask.redirect('/account/login')
    #

    if model == None:
        load_model()  # load model at the beginning once only
    else:
        print("model already loaded")

    #data = request.get_json()  # Get data posted as a json
    data = [1,2,3,4,5,6,7,8,9]
    data = [51.519424, -0.019948, 0.2, 2.0, 1.0, 11, 20220630, 4.0, 37]
    # Price: 330000.0
    data = np.array(data)[np.newaxis, :]  # converts shape from (4,) to (1, 4)
    prediction = model.predict(data)  # runs globally loaded model on the data

    return {"user":prediction[0]}

    return str(prediction[0])

    return {
        'user': "user",
        'user_id': "user.id",
    }


# ################### REGISTER #################################

@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    return {
        # 'user_id': cookie_auth.get_user_id_via_auth_cookie(flask.request),
        'user_id': "cookie_auth.get_user_id_via_auth_cookie(flask.request)",
    }


@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    # data = request_dict.create(default_val='')
    data = {}

    request = flask.request

    # Adding this retro actively. Some folks are experiencing issues where they
    # are getting a list rather than plain dict. I think it's from multiple
    # entries in the multidict. This should fix it.
    args = request.args

    name = data.name
    email = data.email.lower().strip()
    password = data.password.strip()

    if not name or not email or not password:
        return {
            'name': name,
            'email': email,
            'password': password,
            'error': "Some required fields are missing.",
            # 'user_id': cookie_auth.get_user_id_via_auth_cookie(flask.request),
            'user_id': "cookie_auth.get_user_id_via_auth_cookie(flask.request),"
        }

    # user = user_service.create_user(name, email, password)
    user = None
    if not user:
        return {
            'name': name,
            'email': email,
            'password': password,
            'error': "A user with that email already exists.",
            # 'user_id': cookie_auth.get_user_id_via_auth_cookie(flask.request),
            'user_id': "cookie_auth.get_user_id_via_auth_cookie(flask.request)",
        }

    resp = flask.redirect('/account')
    # cookie_auth.set_auth(resp, user.id)

    return resp


# ################### LOGIN #################################

@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    return {}


@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():
    # data = request_dict.create(default_val='')
    request = flask.request
    print("request.form",request.form)

    # Adding this retro actively. Some folks are experiencing issues where they
    # are getting a list rather than plain dict. I think it's from multiple
    # entries in the multidict. This should fix it.
    args = request.args

    data = {'email': 'A@B.C', 'password': "123456"}

    #email = data.email.lower().strip()
    email = data["email"].lower().strip()
    #password = data.password.strip()
    password = data["password"].strip()

    if not email or not password:
        return {
            'email': email,
            'password': password,
            'error': "Some required fields are missing.",
            # 'user_id': cookie_auth.get_user_id_via_auth_cookie(flask.request),
            'user_id': "cookie_auth.get_user_id_via_auth_cookie(flask.request)",
        }

    # user = user_service.login_user(email, password)
    user = None
    #if not user:
    if not True:
        return {
            'email': email,
            'password': password,
            'error': "The account does not exist or the password is wrong.",
            # 'user_id': cookie_auth.get_user_id_via_auth_cookie(flask.request),
            'user_id': "cookie_auth.get_user_id_via_auth_cookie(flask.request)",
        }

    resp = flask.redirect('/account')
    #resp = flask.redirect('/predict')
    # cookie_auth.set_auth(resp, user.id)

    return resp


# ################### LOGOUT #################################

@blueprint.route('/account/logout')
def logout():
    resp = flask.redirect('/')
    # cookie_auth.logout(resp)

    return resp
