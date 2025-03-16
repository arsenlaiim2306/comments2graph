import os
import json
from io import BytesIO
import numpy as np

from .vectorizers import get_vectorizer
from .clusterizers import get_clusterizer
from .projectors import get_projector


class DataEditor():
	def __init__(self, vectorizer="sentence", clusterizer="dbscan", projectors="umap", conf_path="config.json", logger=None):
		self.logger = logger

		# Загрузка конфигов
		conf = self.load_confing(conf_path)

		self.vectorizer = get_vectorizer(vectorizer)(conf.get(vectorizer, {}), self.logger)
		self.clusterizer = get_clusterizer(clusterizer)(conf.get(clusterizer, {}), self.logger)
		self.projector = get_projector(projectors)(conf.get(projectors, {}), self.logger)
	
	def __call__(self, storage=None, update_vectors=False):
		if storage is not None:
			texts = storage.get_all_texts()
			vectors = self.vectorize(texts, storage, update_vectors)

			projected_vector = self.projecting(vectors)
			clusters = self.clusterize(projected_vector)

			return (texts, projected_vector, clusters)


	# Загрузчик конфига
	def load_confing(self, path):
		if os.path.exists(path):
			try:
				with open(path) as file:
					return json.loads(file.read())
			except (FileNotFoundError, json.JSONDecodeError) as e:
				raise RuntimeError(f"Config error: {e}")

		return {}


	# Обработчики
	def vectorize(self, sentences, storage, update_vectors=False):
		vectors = storage.get_all_vectors()

		if len(sentences) != len(vectors) or update_vectors:
			vectors = self.vectorizer(sentences)

			for id, vector in enumerate(vectors):
				with BytesIO() as buffer:
					np.save(buffer, vector)
					storage.update_vector_by_id(id+1, buffer.getvalue())
		else:
			for id, byte_data in enumerate(vectors):
				with BytesIO(byte_data) as buffer:
					vectors[id] = np.load(buffer)

			vectors = np.array(vectors)

		return vectors

	def clusterize(self, vectors):
		return self.clusterizer(vectors)

	def projecting(self, vectors):
		return self.projector(vectors)