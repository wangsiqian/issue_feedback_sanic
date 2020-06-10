import re

from marshmallow import Schema, ValidationError, fields, validates


class CreateTagSerializer(Schema):
    """反序列化创建标签
    """
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    color = fields.Str(required=True)

    @validates(field_name='color')
    def validate_color(self, value):
        color_regex = re.compile('^#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$',
                                 re.IGNORECASE | re.UNICODE)
        if not color_regex.match(value):
            raise ValidationError('Invalid color!')


class TagSerializer(Schema):
    """序列化标签
    """
    name = fields.Str()
    description = fields.Str()
    color = fields.Str()
