from flask import Blueprint, request, jsonify, render_template
from medicines_app.models.database_setup import MedicineDatabase
from .medicinal_product import MedicinalProduct
from .models_ import MedicinesSchema

get_equivalents_blueprint = Blueprint('get_reference_drug', __name__)
livesearch_blueprint = Blueprint('livesearch', __name__)
index_blueprint = Blueprint('index', __name__)

medicine_schema = MedicinesSchema(many=True)


@get_equivalents_blueprint.route('/equivalents', methods=['GET'])
def get_equivalents() -> dict:
    ean_or_name = request.json['ean_or_name']
    medicine_id = __get_medicine_id(ean_or_name)
    equivs = MedicinalProduct(medicine_id).get_equivalents()
    return medicine_schema.jsonify(equivs)

def __get_medicine_id(ean_or_name):
    ean_or_name = ean_or_name.replace('@', '')
    with MedicineDatabase('medicines_app/models/medicine.db') as db:
        if ean_or_name.isdigit():
            result = db.get_medicine_id_by_ean(ean_or_name)
        else:
            result =  db.get_medicine_id_by_name(ean_or_name)
        if result is None:
            return # pusty json
        return result

@index_blueprint.route('/')
def index():
    return render_template("index.html")

@livesearch_blueprint.route('/livesearch',methods=['GET', 'POST'])
def live_search():
    search_box = request.form.get("text")
    with MedicineDatabase('medicines_app/models/medicine.db') as db:
        medicines = db.get_medicines_by_name_like(search_box)
    result = {}
    for i, medicine in enumerate(medicines):
        result.update({i: {'Name': medicine[0]}})
    return jsonify(result)

