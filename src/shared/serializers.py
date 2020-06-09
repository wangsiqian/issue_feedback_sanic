from marshmallow import Schema, ValidationError, fields, validates


class PagedResourceSerializer(Schema):
    """用于反序列化需要分页的数据
    """
    limit = fields.Integer(missing=10)
    start = fields.Integer(missing=0)

    @validates('limit')
    def validate_limit(self, value):
        if value < 0 or 20 < value:
            raise ValidationError('Only accept between 0 and 20')

    @validates('start')
    def validate_start(self, value):
        if value < 0:
            raise ValidationError('Only accept greater than 0')
