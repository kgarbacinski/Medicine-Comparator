import os
from flask import Blueprint, request, jsonify, render_template, make_response, Response
from medicines_app.models.database_setup import MedicineDatabase
from .medicinal_product import MedicinalProduct
from .models_ import MedicinesSchema
import jwt

get_equivalents_blueprint = Blueprint('get_reference_drug', __name__)
livesearch_blueprint = Blueprint('livesearch', __name__)
index_blueprint = Blueprint('index', __name__)

medicine_schema = MedicinesSchema(many=True)


@get_equivalents_blueprint.route('/equivalents', methods=['GET', 'POST'])
def get_equivalents():
    try:
        jwt_token = request.headers.get("X-Access-Token")
        jwt.decode(jwt_token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return Response("WAF: Access Denied for this Host.", status=403)

    request_medicine = request.headers.get('Medicine-Name')
    medicine_id = __get_medicine_id(request_medicine)
    if medicine_id:
        all_medicines = [MedicinalProduct(medicine_id)]
        all_medicines.extend(MedicinalProduct(medicine_id).get_equivalents())
        return medicine_schema.jsonify(all_medicines)

    return make_response(jsonify({'id': '', 'name': '', 'excipents': [], 'content_length': 0, 'form': ''}))


def __get_medicine_id(request_medicine):
    ean_or_name = request_medicine.replace('@', '')
    with MedicineDatabase('../models/medicine.db') as db:
        if ean_or_name.isdigit():
            result = db.get_medicine_id_by_ean(ean_or_name)
        else:
            result = db.get_medicine_id_by_name(ean_or_name)
        if not result:
            return None
        return result[0]


@index_blueprint.route('/')
def index():
    return render_template("index.html")


@livesearch_blueprint.route('/livesearch', methods=['GET', 'POST'])
def live_search():
    search_box = request.headers.get('Medicine-Name')
    with MedicineDatabase('../models/medicine.db') as db:
        medicines = db.get_medicines_by_name_like(search_box)
    result = []
    for medicine in medicines:
        result.append(medicine[0])
    return jsonify(result)
