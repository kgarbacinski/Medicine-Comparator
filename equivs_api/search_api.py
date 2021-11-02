from flask import Blueprint, request, jsonify, render_template
from . import db
from .models import Medicines, MedicinesSchema
import json

get_reference_drug_blueprint = Blueprint('get_reference_drug', __name__)
livesearch_blueprint = Blueprint('livesearch', __name__)
index_blueprint = Blueprint('search_2', __name__)

reference_drug_schema = MedicinesSchema()


# @get_reference_drug_blueprint.route('/equivalents', methods=['GET'])
# def get_reference_drug() -> str:
#     name = request.json
#     # name = request.args.to_dict()['name']
#     print(name)
#     found_drug = db.engine.execute(f'SELECT * FROM Medicines WHERE Medicines.Name = "ABE (89 mg + 89 mg)/g"').fetchone()
#     return reference_drug_schema.jsonify(found_drug)

@index_blueprint.route('/')
def index():
    return render_template("index.html")

@livesearch_blueprint.route('/livesearch',methods=['GET', 'POST'])
def live_search():
    search_box = request.form.get("text")
    query = f'SELECT Medicines.Name FROM Medicines WHERE Medicines.Name LIKE "{search_box}%" ORDER BY Medicines.Name'
    medicines = db.engine.execute(query).fetchall()
    result = {}
    for i, medicine in enumerate(medicines):
        result.update({i: {'Name': medicine[0]}})
    return jsonify(result)
