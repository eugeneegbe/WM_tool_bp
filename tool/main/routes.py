import json
from flask import Blueprint, jsonify, render_template 


main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@main.route('/status', methods=['GET'])
def status():
    return jsonify({'message': 'Server Works!'})
