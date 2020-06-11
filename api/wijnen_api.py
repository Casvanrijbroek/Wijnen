"""The official WijNen API.

Uses the wijnen client and database to process variant requests send from users anywhere in the world!

This code is officially hosted as part of the wijnen back-end on the scouting server currently located in
Lex's attic, the Netherlands.

Authors: Cas van Rijbroek
         Lex Bosch
Date: 11 June, 2020
"""


import hashlib
import json

from flask import Flask, jsonify, request

from exceptions import VariantNotFoundError
from wijnen_db_client import WijnenClient


app = Flask(__name__)

api_key = "merlot"


@app.route('/process_variations', methods=['POST'])
def gather_data():
    """This route has been developed as part of the assignment given by Bio-Prodict to create an API that can filter
    benign variants from a request.

    The POST request should contain the following attributes:
        - api_key: key that allows access to the wijnen API distributed by the wijnen development team
        - variations: nested list of variations that include chromosome, position, reference nucleotide(s) and mutated
                      nucleotide(s) in this order (format: [[CHROM, POS, REF, ALT], [...]])
        - additional_parameters: (OPTIONAL) list of attributes to include in the output of the request

    :return: JSON response with filtered variants.
    """
    f = json.loads(request.data.decode("UTF-8"))

    if not verify_api_key(f["api_key"]):
        return jsonify({"error_code": "401, Unauthorized"}), 401

    response = {"filtered": [], "not_found": []}
    client = create_wijnen_client(f["additional_parameters"])
    variants = f["variations"]

    for variant in variants:
        try:
            variant = client.get_variant(*variant)

            if client.is_pathogenic(variant):
                del variant["_id"]
                response["filtered"].append(variant)
        except VariantNotFoundError:
            response["not_found"].append(variant)

    return jsonify(response)


@app.route('/attribute_summary', methods=['POST'])
def get_attributes():
    f = json.loads(request.data.decode("UTF-8"))

    if not verify_api_key(f["api_key"]):
        return jsonify({"error_code": "401, Unauthorized"}), 401

    client = create_wijnen_client([])

    return jsonify(client.get_attributes())


def verify_api_key(api_hash):
    """Verifies that the API key is valid.

    :param: api_hash: API key given by user
    :returns True if valid, else False
    """

    hashed_key = hashlib.sha224(str.encode(api_key)).hexdigest()
    if hashed_key == api_hash:
        return True
    else:
        return False


def create_wijnen_client(*args, host="wijnen-db", port=27017):
    """Initialize a wijnen client and return it.

    :param args: additional attributes to visualize on requests
    :param host: host name of database
    :param port: port that database communicates through
    :return: initialized wijnen client
    """
    return WijnenClient(host, port, *args)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
