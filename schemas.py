# Importamos las clases Schema y fields del módulo marshmallow
from marshmallow import Schema, fields, validate

class LinkSchema(Schema):
    link = fields.String(required=True, validate=validate.URL())
    nombre=fields.Str(required=True)