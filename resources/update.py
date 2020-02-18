"""Update endpoints for applications"""
__author__ = "Vitali Muladze"

from flask import request, current_app
from flask_restful import Resource, abort
from werkzeug.local import LocalProxy
from commons import faiss_index
from source.configuration import messages

logger = LocalProxy(lambda: current_app.logger)


class Update(Resource):
    """
    Update vectors in faiss database
    """

    def post(self):
        token = request.headers.get("Authorization")
        # Check if features vector is specified
        if not request.data or not request.json.get("features_vectors"):
            logger.info(f"token: {token} send update request without vector.")
            abort(http_status_code=400, message=messages.NO_VECTOR_SPECIFIED)
        # Check if image id is specified else image id is None
        image_ids = request.json.get("image_ids", None)
        # Get features vector from request and update in faiss index
        features_vector = request.json.get("features_vectors")
        result_or_status_message = faiss_index.update(features_vectors=features_vector, image_ids=image_ids)
        # Check if message was returned
        if type(result_or_status_message) == str:
            logger.info(f"token: {token} send update request with bad vector: {result_or_status_message}.")
            abort(http_status_code=400, messages=result_or_status_message)
        logger.info(f"token: {token} send update request successfully.")
        return {"indices": result_or_status_message}
