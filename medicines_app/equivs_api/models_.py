from medicines_app.equivs_api import ma
from flask_marshmallow import fields


class MedicinesSchema(ma.Schema):
    id = fields.fields.Integer()
    name = fields.fields.Str()
    form = fields.fields.Str()
    content_length = fields.fields.Integer()
