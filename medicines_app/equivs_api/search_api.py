import os
from flask import Blueprint, request, jsonify, render_template, make_response, Response
from flask_cors import cross_origin
from models.database_setup import MedicineDatabase
from medicinal_product import MedicinalProduct
from models_ import MedicinesSchema
import jwt
from urllib.parse import unquote_to_bytes
import sys

get_equivalents_blueprint = Blueprint('get_reference_drug', __name__)
livesearch_blueprint = Blueprint('livesearch', __name__)
index_blueprint = Blueprint('index', __name__)

medicine_schema = MedicinesSchema(many=True)


@get_equivalents_blueprint.route('/equivalents', methods=['GET', 'POST'])
@cross_origin(origin='172.20.0.2:5000',headers=['Content-Type', 'Medicine-Name', 'X-Access-Token'])
def get_equivalents():
    try:
        jwt_token = request.headers.get("X-Access-Token")
        jwt.decode(jwt_token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return Response("WAF: Access Denied for this Host.", status=403)
    request_medicine = unquote_to_bytes(request.headers.get('Medicine-Name')).decode()
    medicine_id = __get_medicine_id(request_medicine)
    if medicine_id:
        all_medicines = [MedicinalProduct(medicine_id)]
        all_medicines.extend(MedicinalProduct(medicine_id).get_equivalents())
        return medicine_schema.jsonify(all_medicines)

    return make_response(jsonify({'id': '', 'name': '', 'excipents': [], 'content_length': 0, 'form': ''}))


def __get_medicine_id(request_medicine):
    ean_or_name = request_medicine.replace('@', '')
    with MedicineDatabase('models/medicine.db') as db:
        if ean_or_name.isdigit():
            result = db.get_medicine_id_by_ean(ean_or_name)
        else:
            result = db.get_medicine_id_by_name(ean_or_name)
        if not result:
            return None
        return result[0]


@index_blueprint.route('/')
@cross_origin(origin='172.20.0.2:5000', headers=['Content-Type', 'Medicine-Name', 'X-Access-Token'])
def index():
    return render_template("index.html")


@livesearch_blueprint.route('/livesearch', methods=['GET', 'POST'])
@cross_origin(origin='172.20.0.2:5000', headers=['Content-Type', 'Medicine-Name', 'X-Access-Token'])
def live_search():
    try:
        jwt_token = request.headers.get("X-Access-Token")
        jwt.decode(jwt_token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return Response("WAF: Access Denied for this Host.", status=403)
    search_box = unquote_to_bytes(request.headers.get('Medicine-Name')).decode()
    with MedicineDatabase('models/medicine.db') as db:
        medicines = db.get_medicines_by_name_like(search_box)
    result = []
    for medicine in medicines:
        result.append(medicine[0])
    return jsonify(result)
