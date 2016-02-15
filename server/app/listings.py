# -*- coding: utf-8 -*-
import json
from flask import Blueprint
from flask import Response
from flask import request
from flask.ext.restful import Resource
from server.application import db
from server.app.models import Listing
from server.common.http import add_cors_headers


listings_blueprint = Blueprint('listings_blueprint', __name__)


class ListingsAPI(Resource):
    """The Listings API.

    Routes:
        GET   /listings
    """
    def __init__(self):
        super(ListingsAPI, self).__init__()

    def get(self):
        """GET request handler."""
        listings = Listing.query
        response = {
            "type": "FeatureCollection",
            "features": []
        }

        # Handle query parameters
        args = request.args
        if "min_price" in args:
            listings = listings.filter(Listing.price >= args["min_price"])

        if "max_price" in args:
            listings = listings.filter(Listing.price <= args["max_price"])

        if "min_bed" in args:
            listings = listings.filter(Listing.bedrooms >= args["min_bed"])

        if "max_bed" in args:
            listings = listings.filter(Listing.bedrooms <= args["max_bed"])

        if "min_bath" in args:
            listings = listings.filter(Listing.bathrooms >= args["min_bath"])

        if "max_bath" in args:
            listings = listings.filter(Listing.bathrooms <= args["max_bath"])

        listings = listings.all()
        # Make sure we have a list
        if not isinstance(listings, list):
            listings = [listings]

        for listing in listings:
            response["features"].append(listing.marshal_response())

        return Response(json.dumps(response), mimetype="application/json")
