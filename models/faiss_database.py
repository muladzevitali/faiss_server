"""Faiss index class for creating/loading and using the database"""
__author__ = "Vitali Muladze"

import os

import faiss
import numpy
from faiss import IDSelectorBatch

from source.configuration import messages


class FaissIndex:
    def __init__(self, index_path: str = None, dimension: int = 2048):
        """
        Initialize the the faiss database
        :param index_path: Path to the index file,
        :param dimension: Dimension of vector
        :return: None
        """
        # Check if the file is faiss index
        if index_path is not None and os.path.isfile(index_path):
            self.index = faiss.read_index(index_path)
        # Create new index
        else:
            self.index: IDSelectorBatch = faiss.index_factory(dimension,
                                                              'IDMap,Flat')
        self.dimension = dimension

    def __len__(self):
        """Get number of vectors in the database"""
        return self.index.ntotal

    def insert(self, features_vectors: list, image_ids: list or None = None,
               is_updating: bool = False) -> str:
        """
        Insert features vectors with batches
        :param is_updating: If the insertion is due to update an index
        :param features_vectors: features vectors
        :param image_ids: image ids
        :return: status of insertion
        """
        # If image_id is not specified
        if image_ids is None:
            image_ids = list(range(self.index.ntotal,
                                   self.index.ntotal + len(features_vectors)))

        # Check that for each vector there is an image id
        if len(image_ids) != len(features_vectors):
            return messages.DIMENSION_MISMATCH

        # Check if image_id is bigger then index length
        for image_id in image_ids:
            if not is_updating and image_id < self.index.ntotal:
                return messages.SMALLER_LENGTH_ERROR

        # Check that vector dimension is same as index dimension
        for features_vector in features_vectors:
            if len(features_vector) != self.dimension:
                return messages.DIMENSION_ERROR
        # Write the image_id = 17 as [17] of type numpy array
        id_array = numpy.array(image_ids, dtype=numpy.int64)
        # Write the vector array [0.2, 0.12] as [[0.2, 0.12]] of type numpy array
        vector_array = numpy.array(features_vectors).astype('float32')
        # Insert values into the index
        self.index.add_with_ids(vector_array, id_array)

        return image_ids

    def update(self, features_vectors: list, image_ids: list) -> str:
        """
        Update index ids with new values
        :param image_ids: image id to change the value for
        :param features_vectors: features vector
        :return: status of update
        """
        # Check if image IDs specified
        if image_ids is None:
            return messages.NO_IDS_SPECIFIED

        # Check that for each vector there is an image id
        if len(image_ids) != len(features_vectors):
            return messages.DIMENSION_MISMATCH

        # Check that vector dimension is same as index dimension
        for features_vector in features_vectors:
            if len(features_vector) != self.dimension:
                return messages.DIMENSION_ERROR
        # Write the image_id = 17 as [17] of type numpy array
        id_array = numpy.array(image_ids, dtype=numpy.int64)
        # Select the ids from index and remove them
        id_selector = IDSelectorBatch(id_array.shape[0],
                                      faiss.swig_ptr(id_array))
        self.index.remove_ids(id_selector)
        # Insert new values
        _status = self.insert(features_vectors, image_ids, is_updating=True)

        return _status

    def search(self, features_vectors: list,
               n_results: int = 10) -> tuple or str:
        """
        Search similarities for features vectors
        :param features_vectors: features vectors
        :param n_results: number of results
        :return: indices of the results and distances sorted increasingly or error status
        """
        # Check that vector dimension is same as index dimension
        for features_vector in features_vectors:
            if len(features_vector) != self.dimension:
                return messages.DIMENSION_ERROR
        # Write the vector array [[0.2, 0.12], [0.98, 0.34]] as [[0.2, 0.12], [0.98, 0.34]] of type numpy array
        vector_array = numpy.array(features_vectors).astype('float32')
        # Search for similarities
        distances, result_indices = self.index.search(vector_array, n_results)

        return result_indices, distances

    def to_disk(self, index_path: str) -> str:
        """
        Write the index to disk
        :param index_path: Path to the index folder
        :return: status if writing
        """
        # Create path to the index if not exists
        if not os.path.isdir(os.path.dirname(index_path)):
            os.makedirs(os.path.dirname(index_path), exist_ok=True)
        # Write the index to disk
        faiss.write_index(self.index, index_path)

        return messages.OK
