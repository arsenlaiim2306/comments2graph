from sentence_transformers import SentenceTransformer

class VectorBackend():
	def __init__(self, config, logger=None):
		self.logger = logger

		conf = {
			"model_name_or_path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
		}
		for key, val in config.items():
			conf[key] = val

		try:
			self.model = SentenceTransformer(**conf)
		except Exception as e:
			if logger is not None:
				self.logger.error(f"Failed to load model: {e}")
			raise RuntimeError(f"Failed to load model: {e}")

	def __call__(self, sentences):
		return self.model.encode(sentences, show_progress_bar=True, normalize_embeddings=True)