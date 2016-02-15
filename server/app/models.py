import datetime
from datetime import date


from flask import current_app
from sqlalchemy.sql.expression import ClauseElement

from server.application import db

class Listing(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(256), index=True)
    status = db.Column(db.String(128))
    price = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    sq_ft = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(),
        onupdate=db.func.now())

    def get_geometry(self):
        """Geometry is a dictionary of the type and the lat and lng coords.

        All listings are only of type "point".

        Returns:
            Dictionary representing the geometry of the model.
        """
        return {
            "type": "Point",
            "coordinates": [self.lat, self.lng]
        }

    def marshal_response(self):
        """Prepares record for an API response."""
        return {
            "type": "Feature",
            "geometry": self.get_geometry(),
            "properties": {
                "id": self.id,
                "price": self.price,
                "street": self.street,
                "bedrooms": self.bedrooms,
                "bathrooms": self.bathrooms,
                "sq_ft": self.sq_ft
            }
        }


def get_or_create(model, defaults=None, **kwargs):
    """Convenience method for getting a record or creating it.

    Args:
        model: {db.Model} The model to get or create a record from.
        defaults: {dict} Dictionary of default key, value pairs.

    Returns:
        instance, False if record exists
        instance, True if not
    """
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(
            v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        db.session.add(instance)
        db.session.commit()
        return instance, True
