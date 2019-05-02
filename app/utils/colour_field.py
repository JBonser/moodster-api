from colour import Color
from flask_restplus import fields


class ColourField(fields.Raw):
    #: The JSON/Swagger schema type
    __schema_type__ = 'string'
    #: The JSON/Swagger schema format
    __schema_format__ = 'colour'
    #: An optional JSON/Swagger schema example
    __schema_example__ = '#FFD700'

    def format(self, value):
        try:
            return Color(value).get_hex_l()
        except (AttributeError, ValueError):
            raise fields.MarshallingError
