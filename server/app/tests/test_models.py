import json
from datetime import date, datetime

from server.application import db, create_app
from server.app.models import Listing
from server.common.tests import BaseTestCase


class ModelsTest(BaseTestCase):
    """Test case for models."""

    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    ### Tests ###
    def test_listing_geometry_type_is_point(self):
        listing = Listing(
            street="545 2nd Pl",
            status="pending",
            price=299727,
            bedrooms=4,
            bathrooms=1,
            sq_ft=1608,
            lat=33.36944420834164,
            lng=-112.11971469843907)
        db.session.add(listing)
        db.session.commit()

        geometry = listing.get_geometry()

        self.assertEqual("Point", geometry["type"])

    def test_listing_marshal_response(self):
        listing = Listing(
            street="545 2nd Pl",
            status="pending",
            price=299727,
            bedrooms=4,
            bathrooms=1,
            sq_ft=1608,
            lat=33.36944420834164,
            lng=-112.11971469843907)
        db.session.add(listing)
        db.session.commit()

        response = listing.marshal_response()
        expected_response = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    33.36944420834164,
                    -112.11971469843907
                ]
            },
            "properties": {
                "id": 1,
                "price": 299727,
                "street": "545 2nd Pl",
                "bedrooms": 4,
                "bathrooms": 1,
                "sq_ft": 1608
            }
        }
        self.assertEqual(expected_response, response)
