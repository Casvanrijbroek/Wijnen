import hashlib
import json

from flask import Flask, jsonify, request

from exceptions import VariantNotFoundError
from wijnen_db_client import WijnenClient


app = Flask(__name__)

api_key = "wijn"


@app.route('/process_variations', methods=['POST'])
def gather_data():
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


def verify_api_key(api_hash):
    hashed_key = hashlib.sha224(str.encode(api_key)).hexdigest()
    if hashed_key == api_hash:
        return True
    else:
        return False


def create_wijnen_client(*args, host="wijnen-db", port=27017):
    return WijnenClient(host, port, *args)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
