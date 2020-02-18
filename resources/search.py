"""Search endpoints for applications"""
__author__ = "Vitali Muladze"
import time

from flask import request, current_app
from flask_restful import Resource, abort
from werkzeug.local import LocalProxy

from commons import faiss_index
from source.configuration import messages

logger = LocalProxy(lambda: current_app.logger)


class Search(Resource):
    """
    Search vectors in faiss database
    """

    def post(self):
        token = request.headers.get('Authorization')
        # Check if features vector is specified
        if not request.data or not request.json.get("features_vectors"):
            logger.info(f"token: {token} send search request without vector.")
            abort(http_status_code=400, message=messages.NO_VECTOR_SPECIFIED)
        # Get features vector from request and search in the database
        features_vector = request.json.get("features_vectors")
        # Get number of results from request if any.
        # If not specified then n_results = 10
        n_results = request.json.get("n_results", 10)
        tok = time.time()
        result_or_status_message = faiss_index.search(features_vector,
                                                      n_results=n_results)
        tik = time.time()
        logger.info(f"Time for search: {tik - tok}. Number of images {len(features_vector)}")
        # Check if status code is returned from search
        if type(result_or_status_message) == str:
            logger.info(
                f"token: {token} send search request with bad vector: "
                f"{result_or_status_message}.")
            abort(http_status_code=400, message=result_or_status_message)

        logger.info(f"faiss index length: {len(faiss_index)}")
        return {"indices": result_or_status_message[0].tolist(),
                "distances": result_or_status_message[1].tolist()}
