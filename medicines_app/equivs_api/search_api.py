from flask import Blueprint, request, jsonify, render_template
from medicines_app.models.database_setup import MedicineDatabase
from .models_ import MedicinesSchema

get_reference_drug_blueprint = Blueprint('get_reference_drug', __name__)
livesearch_blueprint = Blueprint('livesearch', __name__)
index_blueprint = Blueprint('search_2', __name__)

reference_drug_schema = MedicinesSchema()


@get_reference_drug_blueprint.route('/equivalents', methods=['GET'])
def get_reference_drug() -> str:
    name = request.json['name']
    with MedicineDatabase('medicines_app/models/medicine.db') as db:
        found_drug = db.get_medicine_id_by_name(name)
        print(found_drug)
    return reference_drug_schema.jsonify(found_drug)

@index_blueprint.route('/')
def index():
    return render_template("index.html")

@livesearch_blueprint.route('/livesearch',methods=['GET', 'POST'])
def live_search():
    search_box = request.form.get("text")
    print(search_box)
    with MedicineDatabase('medicines_app/models/medicine.db') as db:
        medicines = db.get_medicines_by_name_like(search_box)
    result = {}
    for i, medicine in enumerate(medicines):
        result.update({i: {'Name': medicine[0]}})
    return jsonify(result)
