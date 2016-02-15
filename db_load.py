import csv
from server.app.models import Listing
from server.app.models import get_or_create
from server.application import create_app
from server.application import db
from config import BaseConfig


app = create_app(BaseConfig)
db.init_app(app)

with app.app_context():
    with open("listing-details.csv", "rb") as csvfile:
        reader = csv.reader(csvfile)
        for listing in reader:
            print("Loading %s" % str(listing))
            try:
                get_or_create(Listing,
                    street=listing[1],  # listing[0] is the id
                    status=listing[2],
                    price=int(listing[3]),
                    bedrooms=int(listing[4]),
                    bathrooms=int(listing[5]),
                    sq_ft=int(listing[6]),
                    lat=float(listing[7]),
                    lng=float(listing[8]))
            except ValueError as err:
                print("Error loading line: %s" % err)
