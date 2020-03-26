import six
from cassandra.cqlengine import columns

import ujson


class UDTValueManager(columns.UDTValueManager):
    """原来的 udt value manager 有 bug, monkey patch fix
    """
    @property
    def changed(self):
        if self.explicit or self.previous_value is not None:
            return self.value != self.previous_value or \
                   (self.value is not None and self.value.has_changed_fields())

        default_value = self.column.get_default()
        if default_value is not None:
            return self.value != default_value
        return False


class UserDefinedType(columns.UserDefinedType):
    value_manager = UDTValueManager


class JSONField(columns.Column):
    db_type = 'text'

    def to_python(self, value):
        """
        Converts data from the database into python values
        raises a ValidationError if the value can't be converted
        """
        if isinstance(value, (six.string_types, bytearray)):
            return ujson.loads(value)
        return value

    def to_database(self, value):
        """
        Converts python value into database value
        """
        return ujson.dumps(value)
