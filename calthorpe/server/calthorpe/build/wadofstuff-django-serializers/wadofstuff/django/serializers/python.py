"""
Full Python serializer for Django.
"""
import base
from django.utils.encoding import smart_unicode, is_protected_type
from django.core.serializers.python import Deserializer as PythonDeserializer

class Serializer(base.Serializer):
    """
    Python serializer for Django modelled after Ruby on Rails.
    Default behaviour is to serialize only model fields with the exception
    of ForeignKey and ManyToMany fields which must be explicitly added in the
    ``relations`` argument.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize instance attributes.
        """
        self._fields = None
        self._extras = None
        self.objects = []
        super(Serializer, self).__init__(*args, **kwargs)

    def start_serialization(self):
        """
        Called when serializing of the queryset starts.
        """
        self._fields = None
        self._extras = None
        self.objects = []

    def end_serialization(self):
        """
        Called when serializing of the queryset ends.
        """
        pass

    def start_object(self, obj):
        """
        Called when serializing of an object starts.
        """
        self._fields = {}
        self._extras = {}

    def end_object(self, obj):
        """
        Called when serializing of an object ends.
        """
        self.objects.append({
            "model"  : smart_unicode(obj._meta),
            "pk"     : smart_unicode(obj._get_pk_val(), strings_only=True),
            "fields" : self._fields
        })
        if self._extras:
            self.objects[-1]["extras"] = self._extras
        self._fields = None
        self._extras = None

    def handle_field(self, obj, field):
        """
        Called to handle each individual (non-relational) field on an object.
        """
        value = field._get_val_from_obj(obj)
        # Protected types (i.e., primitives like None, numbers, dates,
        # and Decimals) are passed through as is. All other values are
        # converted to string first.
        if is_protected_type(value):
            self._fields[field.name] = value
        else:
            self._fields[field.name] = field.value_to_string(obj)

    def handle_fk_field(self, obj, field):
        """
        Called to handle a ForeignKey field.
        Recursively serializes relations specified in the 'relations' option.
        """
        fname = field.name
        related = getattr(obj, fname)
        if related is not None:
            if fname in self.relations:
                # perform full serialization of FK
                serializer = Serializer()
                options = {}
                if isinstance(self.relations, dict):
                    if isinstance(self.relations[fname], dict):
                        options = self.relations[fname]
                self._fields[fname] = serializer.serialize([related],
                    **options)[0]
            else:
                # emulate the original behaviour and serialize the pk value
                if self.use_natural_keys and hasattr(related, 'natural_key'):
                    related = related.natural_key()
                else:
                    if field.rel.field_name == related._meta.pk.name:
                        # Related to remote object via primary key
                        related = related._get_pk_val()
                    else:
                        # Related to remote object via other field
                        related = smart_unicode(getattr(related,
                            field.rel.field_name), strings_only=True)
                self._fields[fname] = related
        else:
            self._fields[fname] = smart_unicode(related, strings_only=True)

    def handle_m2m_field(self, obj, field):
        """
        Called to handle a ManyToManyField.
        Recursively serializes relations specified in the 'relations' option.
        """
        if field.rel.through._meta.auto_created:
            fname = field.name
            if fname in self.relations:
                # perform full serialization of M2M
                serializer = Serializer()
                options = {}
                if isinstance(self.relations, dict):
                    if isinstance(self.relations[fname], dict):
                        options = self.relations[fname]
                self._fields[fname] = [
                    serializer.serialize([related], **options)[0]
                       for related in getattr(obj, fname).iterator()]
            else:
                # emulate the original behaviour and serialize to a list of 
                # primary key values
                if self.use_natural_keys and hasattr(field.rel.to, 'natural_key'):
                    m2m_value = lambda value: value.natural_key()
                else:
                    m2m_value = lambda value: smart_unicode(
                        value._get_pk_val(), strings_only=True)
                self._fields[fname] = [m2m_value(related)
                    for related in getattr(obj, fname).iterator()]

    def getvalue(self):
        """
        Return the fully serialized queryset (or None if the output stream is
        not seekable).
        """
        return self.objects
    
    def handle_extra_field(self, obj, field):
        """
        Return "extra" fields that the user specifies.
        Can be a property or callable that takes no arguments.
        """
        if hasattr(obj, field):
            extra = getattr(obj, field)
            if callable(extra):
                self._extras[field] = smart_unicode(extra(), strings_only=True)
            else:
                self._extras[field] = smart_unicode(extra, strings_only=True)
                

Deserializer = PythonDeserializer
