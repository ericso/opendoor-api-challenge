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
        listings = Listing.query.first()
        response = {
            "type": "FeatureCollection",
            "features": []
        }

        # Make sure we have a list
        if not isinstance(listings, list):
            listings = [listings]

        for listing in listings:
            response["features"].append(listing.marshal_response())

        return Response(json.dumps(response), mimetype="application/json")
