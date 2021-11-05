from medicines_app.equivs_api import ma
from flask_marshmallow import fields


# class Medicines(db.Model):
#     medicineId = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     # powerDescryption = db.Column(db.String)
#     form = db.Column(db.String)
#     contentLength = db.Column(db.Integer)
#
#     def __init__(self, id:int, name:str, form:str, content_length:int):
#         self.id = id
#         self.name = name
#         self.form = form
#         self.content_length = content_length


class MedicinesSchema(ma.Schema):
    medicineId = fields.fields.Integer()
    name = fields.fields.Str()
    # powerDescryption = fields.fields.Str()
    form = fields.fields.Str()
    contentLength = fields.fields.Integer()
