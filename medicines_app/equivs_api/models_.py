from medicines_app.equivs_api import ma
from flask_marshmallow import fields


class MedicinesSchema(ma.Schema):
    medicineId = fields.fields.Integer()
    name = fields.fields.Str()
    form = fields.fields.Str()
    contentLength = fields.fields.Integer()
